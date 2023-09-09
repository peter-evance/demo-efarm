from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from datetime import timedelta
from dairy.models import *


@receiver(post_save, sender=Pregnancy)
def create_lactation(sender, instance, **kwargs):
    if not instance.date_of_calving and instance.pregnancy_outcome not in [
        PregnancyOutcomeChoices.LIVE,
        PregnancyOutcomeChoices.STILLBORN,
    ]:
        return

    Cow.manager.mark_a_recently_calved_cow(instance.cow)

    try:
        previous_lactation = Lactation.objects.filter(cow=instance.cow).latest()

        if previous_lactation and not previous_lactation.end_date:
            # If the previous lactation doesn't have an end date, set it to one day before the start date of the new
            # lactation
            previous_lactation.end_date = instance.date_of_calving - timedelta(days=1)
            previous_lactation.save()

            Lactation.objects.create(
                start_date=instance.date_of_calving,
                cow=instance.cow,
                pregnancy=instance,
                lactation_number=previous_lactation.lactation_number + 1,
            )
    except Lactation.DoesNotExist:
        Lactation.objects.create(
            start_date=instance.date_of_calving, cow=instance.cow, pregnancy=instance
        )


@receiver(post_save, sender=Insemination)
def create_pregnancy_from_successful_insemination(sender, instance, **kwargs):
    if instance.success and not instance.pregnancy:
        pregnancy = Pregnancy.objects.create(
            cow=instance.cow, start_date=instance.date_of_insemination.date()
        )
        pregnancy.save()

        instance.pregnancy = pregnancy
        instance.save()


@receiver(pre_save, sender=Milk)
def assign_lactation(sender, instance, **kwargs):
    cow = instance.cow
    latest_lactation = cow.lactation_set.latest("start_date")
    instance.lactation = latest_lactation

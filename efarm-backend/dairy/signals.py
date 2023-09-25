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
def set_lactation_for_new_milk(sender, instance, **kwargs):
    if instance.lactation is None:
        # Fetch the most recent lactation for the cow
        most_recent_lactation = instance.cow.lactations.latest()

        if most_recent_lactation:
            instance.lactation = most_recent_lactation


@receiver(post_save, sender=CullingRecord)
def set_cow_production_status_to_culled(sender, instance, **kwargs):
    cow = instance.cow
    cow.current_production_status == CowProductionStatusChoices.CULLED
    cow.save()


@receiver(post_save, sender=QuarantineRecord)
def set_cow_production_status_to_quarantined(sender, instance, **kwargs):
    cow = instance.cow
    if instance.start_date and instance.end_date is None:
        cow.current_production_status == CowProductionStatusChoices.QUARANTINED
        cow.save()

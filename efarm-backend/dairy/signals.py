from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from datetime import timedelta
from . import models


@receiver(pre_save, sender=models.Cow)
def update_cow_status_on_death(sender, instance, **kwargs):
    if instance.date_of_death:
        instance.status = 'Dead'


@receiver(post_save, sender=models.Pregnancy)
def create_lactation(sender, instance, **kwargs):
    if not instance.date_of_calving or not instance.start_date:
        return

    previous_lactation = models.Lactation.objects.filter(cow=instance.cow).order_by('-start_date').first()

    if previous_lactation and not previous_lactation.end_date:
        # If the previous lactation doesn't have an end date, set it to one day before the start date of the new
        # lactation
        previous_lactation.end_date = instance.date_of_calving - timedelta(days=1)
        previous_lactation.save()

    lactation = models.Lactation(
        start_date=instance.date_of_calving,
        cow=instance.cow,
        pregnancy=instance,
        lactation_number=(previous_lactation.lactation_number + 1 if previous_lactation else 1))
    lactation.save()


@receiver(pre_save, sender=models.Milk)
def assign_lactation(sender, instance, **kwargs):
    cow = instance.cow
    latest_lactation = cow.lactation_set.latest('start_date')
    instance.lactation = latest_lactation


@receiver(post_save, sender=models.Insemination)
def create_pregnancy_from_successful_insemination(sender, instance, **kwargs):
    if instance.success and not instance.pregnancy:
        pregnancy = models.Pregnancy.objects.create(cow=instance.cow, start_date=instance.date_of_insemination)
        pregnancy.save()

        instance.pregnancy = pregnancy
        instance.save()

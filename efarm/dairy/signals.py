from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from datetime import timedelta
from . import models


@receiver(pre_save, sender=models.Cow)
def update_cow_status_on_death(sender, instance, **kwargs):
    if instance.date_of_death:
        instance.availability_status = 'D'
        instance.save()


@receiver(post_save, sender=models.Pregnancy)
def update_cow_pregnancy_status(sender, instance, **kwargs):
    if kwargs.get('created', True):
        # Updates cow status as "Pregnant"
        instance.cow.pregnancy_status = 'P'
    else:
        # Updates cow status as "Calved"
        instance.cow.pregnancy_status = 'C'
    instance.cow.save()
    

@receiver(post_save, sender=models.Pregnancy)
def create_lactation(sender, instance, created, **kwargs):
    if not created:
        return  # Don't create a new lactation if the pregnancy was not created just now
        
    if not instance.date_of_calving:
        return  # Don't create a new lactation if the pregnancy doesn't have a date of calving yet
        
    # Check if there's a previous lactation for the cow
    previous_lactation = models.Lactation.objects.filter(cow=instance.cow).order_by('-start_date').first()
    
    if previous_lactation and not previous_lactation.end_date:
        # If the previous lactation doesn't have an end date, set it to one day before the start date of the new lactation
        previous_lactation.end_date = instance.date_of_calving - timedelta(days=1)
        previous_lactation.save()
        
    lactation = models.Lactation(
        start_date=instance.date_of_calving,
        cow=instance.cow,
        pregnancy=instance,
        lactation_number=(previous_lactation.lactation_number + 1 if previous_lactation else 1),
    )
    lactation.save()


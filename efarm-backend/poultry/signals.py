from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import *


@receiver(pre_save, sender=Flock)
def create_flock_history(sender, instance, **kwargs):
    if instance.pk is not None:
        old_instance = Flock.objects.get(pk=instance.pk)

        # Check if 'current_housing_structure' or 'current_rearing_method' has changed
        if (
            instance.current_housing_structure != old_instance.current_housing_structure
            or instance.current_rearing_method != old_instance.current_rearing_method
        ):
            FlockHistory.objects.create(
                flock=instance,
                rearing_method=instance.current_rearing_method,
                current_housing_structure=instance.current_housing_structure,
            )


@receiver(post_save, sender=FlockMovement)
def update_flock_current_housing_structure(sender, instance, **kwargs):
    """
    Signal receiver function to update the current housing structure of the flock
    when a FlockMovement instance is saved.

    Parameters:
    - `sender`: The sender of the signal (FlockMovement model).
    - `instance`: The instance of the FlockMovement model being saved.

    """

    flock = instance.flock
    flock.current_housing_structure = instance.to_structure
    flock.save()

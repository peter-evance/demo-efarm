from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *


@receiver(post_save, sender=FlockMovement)
def update_flock_current_housing_structure(sender, instance, **kwargs):
    """
    Signal receiver function to update the current housing structure of the flock
    when a FlockMovement instance is saved.

    Parameters:
    - `sender`: The sender of the signal (FlockMovement model).
    - `instance`: The instance of the FlockMovement model being saved.

    """

    flock: Flock = instance.flock
    flock.current_housing_structure = instance.to_structure
    flock.save()

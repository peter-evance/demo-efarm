from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import *


@receiver(post_save, sender=Flock)
def create_flock_inventory(sender, instance, created, **kwargs):
    """
    Signal receiver that creates a FlockInventory instance when a Flock is created.

    Parameters:
    - `sender`: The model class that sends the signal.
    - `instance`: The actual instance being saved.
    - `created`: A boolean value indicating if the instance was created or updated.
    - `kwargs`: Additional keyword arguments passed to the receiver.

    """
    if created:
        FlockInventory.objects.create(
            flock=instance,
            number_of_alive_birds=instance.initial_number_of_birds
        )


@receiver(post_save, sender=FlockInspectionRecord)
def update_flock_inventory(sender, instance, **kwargs):
    """
    Signal receiver that updates the FlockInventory instance when a FlockInspectionRecord is created or updated.

    Parameters:
    - `sender`: The model class that sends the signal.
    - `instance`: The actual instance being saved.
    - `kwargs`: Additional keyword arguments passed to the receiver.

    """
    flock_inventory: FlockInventory = FlockInventory.objects.filter(flock=instance.flock).first()
    flock_inventory.number_of_alive_birds -= instance.number_of_dead_birds
    flock_inventory.number_of_dead_birds += instance.number_of_dead_birds
    flock_inventory.save()


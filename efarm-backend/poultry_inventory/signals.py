from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import *


@receiver(post_save, sender=Flock)
def create_flock_inventory(sender, instance, created, **kwargs):
    """
    Signal receiver that creates a FlockInventory instance when a Flock is created.

    Parameters:
    - `sender`: The model class that sends the signal.
    - `instance`: The actual instance of Flock being saved.
    - `created`: A boolean value indicating if the instance was created or updated.
    - `kwargs`: Additional keyword arguments passed to the receiver.

    """
    # Check if the Flock instance was newly created
    if created:
        # Create a FlockInventory instance for the newly created Flock
        FlockInventory.objects.create(
            flock=instance,
            number_of_alive_birds=instance.initial_number_of_birds
        )


@receiver(post_save, sender=FlockInspectionRecord)
def update_flock_inventory_and_flock(sender, instance, **kwargs):
    """
    Signal receiver that updates the FlockInventory instance when a FlockInspectionRecord is created or updated.
    Additionally, it checks if the number of living birds in the flock inventory reaches zero and updates the is_present
    field of the corresponding Flock instance accordingly.

    Parameters:
    - `sender`: The model class that sends the signal.
    - `instance`: The actual instance of FlockInspectionRecord being saved.
    - `kwargs`: Additional keyword arguments passed to the receiver.

    """
    # Retrieve the corresponding FlockInventory instance
    flock_inventory: FlockInventory = FlockInventory.objects.filter(flock=instance.flock).first()

    # Update the number of living birds and number of dead birds in the FlockInventory
    flock_inventory.number_of_alive_birds -= instance.number_of_dead_birds
    flock_inventory.number_of_dead_birds += instance.number_of_dead_birds
    flock_inventory.save()

    # Refresh the FlockInventory from the database to get the latest values
    flock_inventory.refresh_from_db()

    # Check if the number of living birds in the inventory is zero
    if flock_inventory.number_of_alive_birds == 0:
        # Retrieve the corresponding Flock instance
        flock: Flock = flock_inventory.flock

        # Set the is_present field of the Flock instance to False
        flock.is_present = False
        flock.save()


@receiver(post_save, sender=EggCollection)
def update_egg_inventory(instance, **kwargs):
    egg_inventory = EggInventory.objects.first()
    if not egg_inventory:
        egg_inventory = EggInventory.objects.create()
    egg_inventory.total_egg_count += (instance.collected_eggs - instance.broken_eggs)
    egg_inventory.save()


@receiver(post_save, sender=EggInventory)
def create_egg_inventory_history(instance, created, sender, **kwargs):
    if not created:
        EggInventoryHistory.objects.create(egg_inventory=instance, egg_count=instance.total_egg_count)

from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from .models import *


@receiver(pre_save, sender=Milk)
def update_milk_inventory(sender, instance, **kwargs):
    # Update the milk inventory
    milk_inventory, created = MilkInventory.objects.get_or_create(id=1)
    milk_inventory.total_amount_in_kgs += float(instance.amount_in_kgs)
    milk_inventory.save()
    # Create a new milk inventory update history record
    MilkInventoryUpdateHistory.objects.create(amount_in_kgs=milk_inventory.total_amount_in_kgs)


@receiver(post_save, sender=Cow)
def create_and_update_cow_inventory(sender, instance, **kwargs):
    # Retrieve the CowInventory instance, or create a new one if it doesn't exist
    cow_inventory: CowInventory = CowInventory.objects.first()
    if not cow_inventory:
        cow_inventory = CowInventory.objects.create()

    # Update the fields of the CowInventory instance based on the Cow objects
    cow_inventory.total_number_of_cows = Cow.objects.filter(availability_status='Alive').count()
    cow_inventory.number_of_male_cows = Cow.objects.filter(availability_status='Alive', gender='Male').count()
    cow_inventory.number_of_female_cows = Cow.objects.filter(availability_status='Alive', gender='Female').count()
    cow_inventory.number_of_sold_cows = Cow.objects.filter(availability_status='Sold').count()
    cow_inventory.number_of_dead_cows = Cow.objects.filter(availability_status='Dead').count()

    # Save the changes to the CowInventory instance
    cow_inventory.save()
    cow_inventory.refresh_from_db()

    # Create a new history entry in CowInventoryUpdateHistory
    CowInventoryUpdateHistory.objects.create(number_of_cows=cow_inventory.total_number_of_cows)


@receiver(post_save, sender=CowPen)
def create_cow_pen_inventory_and_history(sender, instance, **kwargs):
    # Retrieve or create the CowPenInventory instance associated with the CowPen
    pen_inventory, created = CowPenInventory.objects.get_or_create(pen=instance)

    # Create a new CowPenHistory entry based on the CowPen and CowPenInventory data
    CowPenHistory.objects.create(
        pen=instance,
        barn=instance.barn,
        pen_type=instance.pen_type,
        number_of_cows=pen_inventory.number_of_cows,
    )


@receiver(post_save, sender=Barn)
def create_barn_inventory(sender, instance, created, **kwargs):
    # Create a BarnInventory instance when a new Barn is created
    if created:
        BarnInventory.objects.create(barn=instance)


@receiver(post_save, sender=CowInPenMovement)
def update_cow_pen_inventory_and_barn_inventory(sender, instance, created, **kwargs):

    # Signal receiver function to update cow pen inventory and barn inventory when a new CowInPenMovement instance is created.

    if created:
        # Check if the cow is moving from a previous pen
        if instance.previous_pen:
            # Get the cow pen inventory for the pen the cow is moving from
            old_pen_inventory: CowPenInventory = CowPenInventory.objects.get(pen=instance.previous_pen)
            old_pen_inventory.remove_cow()

            # Check if the previous pen is associated with a barn
            if instance.previous_pen.barn:
                # Get the barn inventory for the barn the cow is moving from
                old_barn_inventory = BarnInventory.objects.get(barn=instance.previous_pen.barn)
                old_barn_inventory.remove_cow()
                old_barn_inventory.refresh_from_db()
                BarnInventoryHistory.objects.create(
                    barn_inventory=old_barn_inventory,
                    number_of_cows=old_barn_inventory.number_of_cows
                )

        # Get the cow pen inventory for the pen the cow is moving to
        new_pen_inventory: CowPenInventory = CowPenInventory.objects.get(pen=instance.new_pen)
        new_pen_inventory.add_cow()

        # Get the barn inventory for the barn the cow is moving to
        new_barn_inventory: BarnInventory = BarnInventory.objects.get(barn=instance.new_pen.barn)
        new_barn_inventory.add_cow()
        new_barn_inventory.refresh_from_db()
        BarnInventoryHistory.objects.create(
            barn_inventory=new_barn_inventory,
            number_of_cows=new_barn_inventory.number_of_cows
        )

        # Check if the cow is moved into a pen that is not within a specific barn
        if instance.previous_pen and instance.new_pen:
            if instance.previous_pen.barn != instance.new_pen.barn:
                # Create a CowInBarnMovement instance
                CowInBarnMovement.objects.create(
                    cow=instance.cow,
                    previous_barn=instance.previous_pen.barn,
                    new_barn=instance.new_pen.barn
                )

        # Create a CowInBarnMovement instance when moving into a pen without a previous pen
        if instance.new_pen.barn:
            CowInBarnMovement.objects.create(
                cow=instance.cow,
                previous_barn=None,
                new_barn=instance.new_pen.barn
            )

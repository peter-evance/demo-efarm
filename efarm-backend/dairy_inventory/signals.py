from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import MilkInventory, MilkInventoryUpdateHistory
from dairy.models import Milk


@receiver(pre_save, sender=Milk)
def update_milk_inventory(sender, instance, **kwargs):
    """
    If a new milk record is created or an existing milk record is updated, the inventory will be adjusted to account for
    the change in the amount of milk produced. If the new amount is less than or greater than the old amount,
    the difference will be added or subtracted from the inventory respectively.
    """
    try:
        old_milk_amount = Milk.objects.get(pk=instance.pk).amount_in_kgs
    except Milk.DoesNotExist:
        # If the milk record doesn't exist yet, set the old milk amount to 0
        old_milk_amount = 0

    milk_difference = instance.amount_in_kgs - old_milk_amount
    if milk_difference >= 0:
        update_type = MilkInventoryUpdateHistory.UpdateType.ADD
    else:
        update_type = MilkInventoryUpdateHistory.UpdateType.REMOVE

    # Update the milk inventory
    milk_inventory, created = MilkInventory.objects.get_or_create(id=1)
    milk_inventory.total_amount_in_kgs += float(milk_difference)
    milk_inventory.save()
    # Create a new milk inventory update history record
    MilkInventoryUpdateHistory.objects.create(amount_in_kgs_change=milk_difference,
                                              update_type=update_type,
                                              amount_in_kgs=milk_inventory.total_amount_in_kgs)

from django.db import models
from django.core.validators import MinValueValidator
from .choices import UpdateType


class MilkInventory(models.Model):
    """
    The model represents the current inventory of milk.

    ### Fields

    - `amount_in_kgs`: The amount of milk currently in stock, in kilograms.
    - `last_update`: The date and time when the inventory was last updated.

    ### Meta options

    - `verbose_name`: The singular name of the model in the Django admin.
    - `verbose_name_plural`: The plural name of the model in the Django admin.
    - `ordering`: A list of fields to use when ordering the model instances.
    """

    class Meta:
        verbose_name = "Milk Inventory"
        verbose_name_plural = "Milk Inventory"
        ordering = ['-last_update']

    total_amount_in_kgs = models.DecimalField(verbose_name="Amount (kg)", default=0.00, max_digits=7, decimal_places=2,
                                              validators=[MinValueValidator(0.00)], editable=False)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.total_amount_in_kgs} kg of milk in inventory (last updated " \
               f"{self.last_update.strftime('%Y-%m-%d %H:%M:%S')})"


class MilkInventoryUpdateHistory(models.Model):
    """
    The model represents the history of milk inventory updates.

    ### Fields

    - `amount_in_kgs`: The amount of milk added or removed from the inventory.
    - `update_type`: Whether the milk was added or removed from the inventory.
    - `date`: The date when the inventory was updated.
    - `total_amount_in_kgs`: The total amount of milk in inventory after the update.

    ### Meta options

    - `verbose_name`: The singular name of the model in the Django admin.
    - `verbose_name_plural`: The plural name of the model in the Django admin.
    - `ordering`: A list of fields to use when ordering the model instances.
    """
    
    class Meta:
        verbose_name = 'Milk Inventory Update History'
        verbose_name_plural = 'Milk Inventory Update History'
        ordering = ['-date']

    amount_in_kgs_change = models.DecimalField(verbose_name=' Change in Amount (Kgs)', max_digits=7, decimal_places=2,
                                               validators=[MinValueValidator(0.00)], editable=False)
    update_type = models.CharField(verbose_name='Update Type', max_length=7, choices=UpdateType.choices, editable=False)
    amount_in_kgs = models.DecimalField(verbose_name="Total Amount (kg)", default=0.00, max_digits=7, decimal_places=2,
                                        validators=[MinValueValidator(0.00)], editable=False)
    date = models.DateField(verbose_name='Date', auto_now_add=True)

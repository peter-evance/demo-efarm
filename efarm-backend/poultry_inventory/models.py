from decimal import Decimal

from poultry.models import *


class FlockInventory(models.Model):
    """
    The model represents the inventory of a flock.

    Fields:
    - `flock`: A one-to-one relationship to the `Flock` model, representing the flock for which the inventory is maintained.
    - `number_of_alive_birds`: A positive integer field representing the number of alive birds in the flock.
    - `number_of_dead_birds`: A positive integer field representing the number of dead birds in the flock.
    - `last_update`: A DateTime field that automatically records the last update time of the inventory.
    - `date_added`: A Date field that automatically records the date when the inventory was added.

    Methods:
    - `calculate_mortality_rate`: Calculates and returns the mortality rate of the flock as a decimal value.
    - `save()`: Overrides the default save method to create a `FlockInventoryHistory` instance after saving the inventory.

    """

    class Meta:
        verbose_name_plural = "Flock Inventories"

    flock = models.OneToOneField(Flock, on_delete=models.CASCADE, related_name='inventory')
    number_of_alive_birds = models.PositiveIntegerField(default=0)
    number_of_dead_birds = models.PositiveIntegerField(default=0)
    last_update = models.DateTimeField(auto_now=True)
    date_added = models.DateField(auto_now_add=True)

    @property
    def calculate_mortality_rate(self):
        """
        Calculates and returns the mortality rate of the flock as a decimal value.

        Returns:
        - Decimal: The calculated mortality rate.

        """
        mortality_rate = (self.number_of_dead_birds / self.flock.initial_number_of_birds) * 100
        return Decimal(mortality_rate).quantize(Decimal('0.00'))

    def __str__(self):
        """
        Returns a string representation of the flock inventory.

        Returns:
        - str: The string representation of the flock inventory.

        """
        return f"Inventory for {self.flock}"

    def save(self, *args, **kwargs):
        """
        Overrides the default save method to create a `FlockInventoryHistory` instance after saving the inventory.

        """
        super().save(*args, **kwargs)

        FlockInventoryHistory.objects.create(
            flock_inventory=self,
            date=self.last_update.date(),
            number_of_birds=self.number_of_alive_birds,
            mortality_rate=self.calculate_mortality_rate
        )


class FlockInventoryHistory(models.Model):
    """
    The model represents the history of a flock's inventory.

    Fields:
    - `flock_inventory`: A foreign key relationship to the `FlockInventory` model, representing the associated flock inventory.
    - `date`: A Date field representing the date of the inventory history.
    - `number_of_birds`: A positive integer field representing the number of birds in the flock at the specified date.
    - `mortality_rate`: A Decimal field representing the mortality rate of the flock at the specified date.

    """

    class Meta:
        verbose_name_plural = "Flock Inventory Histories"

    flock_inventory = models.ForeignKey(FlockInventory, on_delete=models.CASCADE, related_name='history')
    date = models.DateField()
    number_of_birds = models.PositiveIntegerField()
    mortality_rate = models.DecimalField(max_digits=5, decimal_places=2)


class EggInventory(models.Model):
    total_egg_count = models.PositiveIntegerField(default=0, editable=False)


class EggInventoryHistory(models.Model):
    egg_inventory = models.ForeignKey(EggInventory, on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now_add=True)
    egg_count = models.PositiveIntegerField()

    def __str__(self):
        return f"Egg inventory history - {self.egg_count}"

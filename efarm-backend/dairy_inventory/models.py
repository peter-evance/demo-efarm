from dairy.models import *
from .choices import *


class MilkInventory(models.Model):
    """
    The model represents the current dairy_inventory of milk.

    ### Fields

    - `amount_in_kgs`: The amount of milk currently in stock, in kilograms.
    - `last_update`: The date and time when the dairy_inventory was last updated.

    ### Meta options

    - `verbose_name`: The singular name of the model in the Django admin.
    - `verbose_name_plural`: The plural name of the model in the Django admin.
    - `ordering`: A list of fields to use when ordering the model instances.
    """

    class Meta:
        verbose_name = "Milk Inventory"
        verbose_name_plural = "Milk Inventory"
        ordering = ['-last_update']

    total_amount_in_kgs = models.FloatField(verbose_name="Amount (kg)", default=0.00,
                                            validators=[MinValueValidator(0.00)], editable=False)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.total_amount_in_kgs} kg of milk in dairy_inventory (last updated " \
               f"{self.last_update.strftime('%Y-%m-%d %H:%M:%S')})"


class MilkInventoryUpdateHistory(models.Model):
    """
    The model represents the history of milk dairy_inventory updates.
    
    ### Fields
    
    - `amount_in_kgs`: The amount of milk added or removed from the dairy_inventory.
    - `update_type`: Whether the milk was added or removed from the dairy_inventory.
    - `date`: The date when the dairy_inventory was updated.
    - `total_amount_in_kgs`: The total amount of milk in dairy_inventory after the update.
    
    ### Meta options
    
    - `verbose_name`: The singular name of the model in the Django admin.
    - `verbose_name_plural`: The plural name of the model in the Django admin.
    - `ordering`: A list of fields to use when ordering the model instances.
    """

    amount_in_kgs = models.DecimalField(verbose_name="Total Amount (kg)", default=0.00, max_digits=7, decimal_places=2,
                                        validators=[MinValueValidator(0.00)], editable=False)
    date = models.DateField(verbose_name='Date', auto_now_add=True)


class CowInventory(models.Model):
    """
    Model representing the inventory of cows on a dairy farm.

    Fields:
    - `total_number_of_cows`: Total number of cows in the inventory.
    - `number_of_male_cows`: Number of male cows in the inventory.
    - `number_of_female_cows`: Number of female cows in the inventory.
    - `number_of_sold_cows`: Number of cows that have been sold.
    - `number_of_dead_cows`: Number of cows that have died.
    - `last_update`: Date and time of the last update to the inventory.

    """

    total_number_of_cows = models.PositiveIntegerField(verbose_name="Total Number of Cows", default=0, editable=False)
    number_of_male_cows = models.PositiveIntegerField(verbose_name="Number of Male Cows", default=0, editable=False)
    number_of_female_cows = models.PositiveIntegerField(verbose_name="Number of Female Cows", default=0, editable=False)
    number_of_sold_cows = models.PositiveIntegerField(verbose_name="Number of Sold Cows", default=0, editable=False)
    number_of_dead_cows = models.PositiveIntegerField(verbose_name="Number of Dead Cows", default=0, editable=False)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.total_number_of_cows} cows in farm (last updated " \
               f"{self.last_update.strftime('%Y-%m-%d %H:%M:%S')})"


class CowInventoryUpdateHistory(models.Model):
    """
    Model representing the update history of the cow inventory.

    Fields:
    - `number_of_cows`: Total number of cows in the inventory at the time of the update.
    - `date`: Date of the cow inventory update.

    """

    number_of_cows = models.PositiveIntegerField(verbose_name="Total number of cows", default=0, editable=False)
    date = models.DateField(verbose_name='Cow Inventory Update History Date', auto_now_add=True)


class BarnInventory(models.Model):
    """
    Model representing the inventory of a barn.

    Fields:
    - `barn`: One-to-one relationship with the `Barn` model, representing the barn associated with the inventory.
    - `number_of_cows`: The current number of cows in the barn.
    - `number_of_pens`: The number of pens in the barn.
    - `last_update`: Date and time of the last update to the barn inventory.

    Methods:
    - `add_cow()`: Adds a cow to the barn inventory if the barn's capacity has not been exceeded.
    - `remove_cow()`: Removes a cow from the barn inventory.

    """

    barn = models.OneToOneField(Barn, on_delete=models.SET_NULL, null=True)
    number_of_cows = models.PositiveIntegerField(default=0)
    number_of_pens = models.PositiveIntegerField(default=1)
    last_update = models.DateTimeField(auto_now=True)

    def add_cow(self):
        """
        Adds a cow to the barn inventory if the barn's capacity has not been exceeded.

        Raises:
        - ValueError: If the barn capacity has been exceeded and cannot accommodate more cows.

        """
        if self.number_of_cows < self.barn.capacity:
            self.number_of_cows += 1
            self.save()
        else:
            raise ValueError("Barn capacity exceeded. Cannot add more cows.")

    def remove_cow(self):
        """
        Removes a cow from the barn inventory.

        """
        if self.number_of_cows > 0:
            self.number_of_cows -= 1
            self.save()

    def __str__(self):
        return f"{self.barn.name} Inventory (last updated {self.last_update.strftime('%Y-%m-%d %H:%M:%S')})"


class BarnInventoryHistory(models.Model):
    """
    Model representing the history of barn inventory.

    Fields:
    - `barn_inventory`: A foreign key to the `BarnInventory` model, representing the associated barn inventory.
    - `number_of_cows`: The number of cows in the barn inventory at the time of the history record.
    - `timestamp`: Date and time of the barn inventory history record.

    Methods:
    - `__str__()`: Returns a string representation of the barn inventory history record.

    """

    barn_inventory = models.ForeignKey(BarnInventory, on_delete=models.CASCADE)
    number_of_cows = models.PositiveIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.barn_inventory} - {self.timestamp}"


class CowPenInventory(models.Model):
    """
    Model representing the inventory of a cow pen.

    Fields:
    - `pen`: One-to-one relationship with the `CowPen` model, representing the cow pen associated with the inventory.
    - `number_of_cows`: The current number of cows in the cow pen.

    Methods:
    - `add_cow()`: Adds a cow to the cow pen inventory if the pen's capacity has not been exceeded.
    - `remove_cow()`: Removes a cow from the cow pen inventory.

    """

    pen = models.OneToOneField(CowPen, on_delete=models.CASCADE)
    number_of_cows = models.PositiveIntegerField(default=0)

    def add_cow(self):
        """
        Adds a cow to the cow pen inventory if the pen's capacity has not been exceeded.

        Raises:
        - ValueError: If the pen capacity has been exceeded and cannot accommodate more cows.

        """
        if self.number_of_cows < self.pen.capacity:
            self.number_of_cows += 1
            self.save()
        else:
            raise ValueError("Pen capacity exceeded. Cannot add more cows.")

    def remove_cow(self):
        """
        Removes a cow from the cow pen inventory.

        """
        if self.number_of_cows > 0:
            self.number_of_cows -= 1
            self.save()


class CowPenHistory(models.Model):
    pen = models.ForeignKey(CowPen, on_delete=models.CASCADE)
    barn = models.ForeignKey(Barn, on_delete=models.CASCADE)
    pen_type = models.CharField(max_length=15, choices=CowPenTypeChoices.choices)
    number_of_cows = models.PositiveIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

from rest_framework import serializers

from .models import *


class FlockInventorySerializer(serializers.ModelSerializer):
    """
    Serializer for the FlockInventory model.

    Serializes the following fields:
    - `flock`: The associated flock for the inventory.
    - `number_of_alive_birds`: The number of alive birds in the flock inventory.
    - `number_of_dead_birds`: The number of dead birds in the flock inventory.
    - `last_update`: The timestamp of the last update to the inventory.
    - `date_added`: The date when the inventory was added.

    Additional Serialized Fields:
    - `calculate_mortality_rate`: Read-only field that calculates the mortality rate of the flock inventory.

    """

    flock = serializers.PrimaryKeyRelatedField(queryset=Flock.objects.all())
    calculate_mortality_rate = serializers.ReadOnlyField()

    class Meta:
        model = FlockInventory
        fields = '__all__'


class FlockInventoryHistorySerializer(serializers.ModelSerializer):
    """
    Serializer for the FlockInventoryHistory model.

    Serializes the following fields:
    - `flock_inventory`: The associated flock inventory for the history.
    - `date`: The date of the inventory history.
    - `Number_of_birds`: The number of birds in the flock at the specified date.
    - `mortality_rate`: The mortality rate of the flock at the specified date.

    """

    flock_inventory = serializers.PrimaryKeyRelatedField(queryset=FlockInventory.objects.all())
    mortality_rate = serializers.DecimalField(max_digits=4, decimal_places=2, coerce_to_string=False)

    class Meta:
        model = FlockInventoryHistory
        fields = '__all__'

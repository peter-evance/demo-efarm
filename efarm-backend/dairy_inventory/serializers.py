from rest_framework import serializers
from .models import *


class MilkInventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MilkInventory
        fields = ('total_amount_in_kgs', 'last_update')
        read_only_fields = ('total_amount_in_kgs', 'last_update')


class MilkInventoryUpdateHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MilkInventoryUpdateHistory
        fields = '__all__'
        read_only_fields = ('amount_in_kgs', 'date')


class CowInventorySerializer(serializers.ModelSerializer):
    """
    Serializer for the CowInventory model.

    Serializes the following fields:
    - `id`: The unique identifier of the cow inventory.
    - `total_number_of_cows`: Total number of cows in the inventory.
    - `number_of_male_cows`: Number of male cows in the inventory.
    - `number_of_female_cows`: Number of female cows in the inventory.
    - `number_of_sold_cows`: Number of cows that have been sold.
    - `number_of_dead_cows`: Number of cows that have died.
    - `last_update`: Date and time of the last update to the inventory.

    """

    class Meta:
        model = CowInventory
        fields = '__all__'


class CowInventoryUpdateHistorySerializer(serializers.ModelSerializer):
    """
    Serializer for the CowInventoryUpdateHistory model.

    Serializes the following fields:
    - `id`: The unique identifier of the update history.
    - `number_of_cows`: Total number of cows at the time of the update.
    - `date`: The date of the update.

    """

    class Meta:
        model = CowInventoryUpdateHistory
        fields = '__all__'


class CowPenHistorySerializer(serializers.ModelSerializer):
    """
    Serializer for the CowPenHistory model.

    Serializes the following fields:
    - `id`: The unique identifier of the cow pen history.
    - `pen`: The cow pen associated with the history.
    - `barn`: The barn associated with the history.
    - `type`: The type of the cow pen.
    - `number_of_cows`: The number of cows at the time of the history.
    - `timestamp`: The timestamp of the history.

    """

    class Meta:
        model = CowPenHistory
        fields = '__all__'


class BarnInventorySerializer(serializers.ModelSerializer):
    """
    Serializer for the BarnInventory model.

    Serializes the following fields:
    - `id`: The unique identifier of the barn inventory.
    - `barn`: The barn associated with the inventory.
    - `number_of_cows`: The number of cows in the barn.
    - `number_of_pens`: The number of pens in the barn.
    - `last_update`: The timestamp of the last update to the inventory.

    """

    class Meta:
        model = BarnInventory
        fields = '__all__'


class BarnInventoryHistorySerializer(serializers.ModelSerializer):
    """
    Serializer for the BarnInventoryHistory model.

    Serializes the following fields:
    - `id`: The unique identifier of the barn inventory history.
    - `barn_inventory`: The barn inventory associated with the history.
    - `number_of_cows`: The number of cows at the time of the history.
    - `timestamp`: The timestamp of the history.

    """

    class Meta:
        model = BarnInventoryHistory
        fields = '__all__'


class CowPenInventorySerializer(serializers.ModelSerializer):
    """
    Serializer for the CowPenInventory model.

    Serializes the following fields:
    - `id`: The unique identifier of the cow pen inventory.
    - `pen`: The cow pen associated with the inventory.
    - `number_of_cows`: The number of cows in the pen.

    """

    class Meta:
        model = CowPenInventory
        fields = '__all__'

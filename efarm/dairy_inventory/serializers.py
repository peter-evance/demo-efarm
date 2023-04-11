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
        fields = ('amount_in_kgs_change', 'update_type', 'amount_in_kgs', 'date')
        read_only_fields = ('amount_in_kgs_change', 'update_type', 'amount_in_kgs', 'date')

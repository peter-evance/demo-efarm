from rest_framework import serializers
from poultry.models import *


class FlockSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlockSource
        fields = '__all__'


class HousingStructureSerializer(serializers.ModelSerializer):
    class Meta:
        model = HousingStructure
        fields = '__all__'


class FlockSerializer(serializers.ModelSerializer):
    age_in_weeks = serializers.ReadOnlyField()
    age_in_months = serializers.ReadOnlyField()
    age_in_weeks_in_farm = serializers.ReadOnlyField()
    age_in_months_in_farm = serializers.ReadOnlyField()
    current_housing_structure = serializers.PrimaryKeyRelatedField(queryset=HousingStructure.objects.all())
    source = serializers.PrimaryKeyRelatedField(queryset=FlockSource.objects.all())

    class Meta:
        model = Flock
        fields = '__all__'


class FlockHistorySerializer(serializers.ModelSerializer):
    flock = serializers.PrimaryKeyRelatedField(queryset=Flock.objects.all())

    class Meta:
        model = FlockHistory
        fields = '__all__'
        read_only_fields = ('rearing_method', 'current_housing_structure', 'date_changed')

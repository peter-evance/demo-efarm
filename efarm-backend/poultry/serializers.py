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
    class Meta:
        model = FlockHistory
        fields = '__all__'
        read_only_fields = ('flock', 'rearing_method', 'current_housing_structure', 'date_changed')


class FlockMovementSerializer(serializers.ModelSerializer):
    """
    Serializer for the FlockMovement model.

    Serializes the following fields:
    - `flock`: The associated flock for the movement.
    - `from_structure`: The housing structure from which the flock is moved.
    - `to_structure`: The housing structure to which the flock is moved.

    """

    flock = serializers.PrimaryKeyRelatedField(queryset=Flock.objects.all())
    from_structure = serializers.PrimaryKeyRelatedField(queryset=HousingStructure.objects.all())
    to_structure = serializers.PrimaryKeyRelatedField(queryset=HousingStructure.objects.all())

    class Meta:
        model = FlockMovement
        fields = '__all__'


class FlockInspectionRecordSerializer(serializers.ModelSerializer):
    """
    Serializer for the FlockInspectionRecord model.

    Serializes the following fields:
    - `flock`: The associated flock for the inspection record.
    - `date`: The date and time of the inspection.
    - `number_of_dead_birds`: The number of dead birds recorded in the inspection.

    """

    flock = serializers.PrimaryKeyRelatedField(queryset=Flock.objects.all())

    class Meta:
        model = FlockInspectionRecord
        fields = '__all__'

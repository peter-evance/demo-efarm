from rest_framework import serializers
from poultry.models import *


class FlockSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlockSource
        fields = "__all__"


class FlockBreedSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlockBreed
        fields = "__all__"


class HousingStructureSerializer(serializers.ModelSerializer):
    class Meta:
        model = HousingStructure
        fields = "__all__"


class FlockSerializer(serializers.ModelSerializer):
    age_in_weeks = serializers.ReadOnlyField()
    age_in_months = serializers.ReadOnlyField()
    age_in_weeks_in_farm = serializers.ReadOnlyField()
    age_in_months_in_farm = serializers.ReadOnlyField()
    current_housing_structure = serializers.PrimaryKeyRelatedField(
        queryset=HousingStructure.objects.all()
    )
    source = FlockSourceSerializer()
    breed = FlockBreedSerializer()

    class Meta:
        model = Flock
        fields = "__all__"

    def create(self, validated_data):
        flock_source_data = validated_data.pop("source")
        flock_breed_data = validated_data.pop("breed")
        source, _ = FlockSource.objects.get_or_create(**flock_source_data)
        breed, _ = FlockBreed.objects.get_or_create(**flock_breed_data)
        flock = Flock.objects.create(breed=breed, source=source, **validated_data)
        return flock

    def update(self, instance, validated_data):
        fields_to_exclude = [
            "source",
            "breed",
            "date_of_hatching",
            "chicken_type",
            "initial_number_of_birds",
            "current_housing_structure",
            "date_established",
            "is_present",
        ]

        for field in fields_to_exclude:
            validated_data.pop(field, None)
        return super().update(instance, validated_data)


class FlockHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FlockHistory
        fields = "__all__"
        read_only_fields = (
            "flock",
            "rearing_method",
            "current_housing_structure",
            "date_changed",
        )


class FlockMovementSerializer(serializers.ModelSerializer):
    """
    Serializer for the FlockMovement model.

    Serializes the following fields:
    - `flock`: The associated flock for the movement.
    - `from_structure`: The housing structure from which the flock is moved.
    - `to_structure`: The housing structure to which the flock is moved.

    """

    flock = serializers.PrimaryKeyRelatedField(queryset=Flock.objects.all())
    from_structure = serializers.PrimaryKeyRelatedField(
        queryset=HousingStructure.objects.all()
    )
    to_structure = serializers.PrimaryKeyRelatedField(
        queryset=HousingStructure.objects.all()
    )

    class Meta:
        model = FlockMovement
        fields = "__all__"


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
        fields = "__all__"


class FlockBreedInformationSerializer(serializers.ModelSerializer):
    """
    Serializer for the FlockBreedInformation model.

    Serializes the following fields:
    - `breed`: The associated flock breed.
    - `chicken_type`: The type of chicken.
    - `date_added`: The date when the breed information was added.
    - `average_mature_weight_in_kgs`: The average mature weight of the breed in kilograms.
    - `average_egg_production`: The average egg production of the breed.
    - `maturity_age_in_weeks`: The maturity age of the breed in weeks.

    """

    breed = serializers.PrimaryKeyRelatedField(queryset=FlockBreed.objects.all())

    class Meta:
        model = FlockBreedInformation
        fields = "__all__"


class EggCollectionSerializer(serializers.ModelSerializer):
    flock = serializers.PrimaryKeyRelatedField(queryset=Flock.objects.all())

    class Meta:
        model = EggCollection
        fields = "__all__"

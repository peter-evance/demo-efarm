from rest_framework import serializers

from .models import *


class CowBreedSerializer(serializers.ModelSerializer):
    class Meta:
        model = CowBreed
        fields = "__all__"


class CowSerializer(serializers.ModelSerializer):
    breed = CowBreedSerializer()
    tag_number = serializers.ReadOnlyField()
    parity = serializers.ReadOnlyField()
    age = serializers.ReadOnlyField()
    age_in_farm = serializers.ReadOnlyField()

    class Meta:
        model = Cow
        fields = "__all__"

    def create(self, validated_data):
        breed_data = validated_data.pop("breed")
        breed, _ = CowBreed.objects.get_or_create(**breed_data)

        cow = Cow.objects.create(breed=breed, **validated_data)
        return cow

    def update(self, instance, validated_data):
        fields_to_exclude = [
            "breed",
            "gender",
            "sire",
            "dam",
            "is_bought",
            "date_introduced_in_farm",
        ]
        for field in fields_to_exclude:
            validated_data.pop(field, None)
        return super().update(instance, validated_data)


class HeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Heat
        fields = "__all__"


class InseminatorSerializer(serializers.ModelSerializer):
    phone_number = PhoneNumberField()

    class Meta:
        model = Inseminator
        fields = "__all__"


class InseminationSerializer(serializers.ModelSerializer):
    days_since_insemination = serializers.ReadOnlyField()

    class Meta:
        model = Insemination
        fields = "__all__"

    def update(self, instance, validated_data):
        fields_to_exclude = [
            "cow",
            "date_of_insemination",
            "pregnancy",
            "inseminator",
            "semen",
            "days_since_insemination",
        ]
        for field in fields_to_exclude:
            validated_data.pop(field, None)
        return super().update(instance, validated_data)


class PregnancySerializer(serializers.ModelSerializer):
    due_date = serializers.ReadOnlyField()
    pregnancy_duration = serializers.ReadOnlyField()

    class Meta:
        model = Pregnancy
        fields = "__all__"


class LactationSerializer(serializers.ModelSerializer):
    days_in_lactation = serializers.ReadOnlyField()
    lactation_stage = serializers.ReadOnlyField()
    end_date_ = serializers.ReadOnlyField()

    class Meta:
        model = Lactation
        fields = "__all__"

    def create(self, validated_data):
        # Get the cow instance from the validated data
        cow_instance = validated_data["cow"]

        LactationValidator.validate_cow_origin(cow_instance)
        LactationValidator.validate_cow_category(cow_instance.category)

        lactation_instance = Lactation.objects.create(**validated_data)
        return lactation_instance


class MilkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Milk
        fields = "__all__"


class WeightRecordSerializer(serializers.ModelSerializer):
    cow = serializers.PrimaryKeyRelatedField(queryset=Cow.objects.all())

    class Meta:
        model = WeightRecord
        fields = "__all__"


class CullingRecordSerializer(serializers.ModelSerializer):
    cow = serializers.PrimaryKeyRelatedField(queryset=Cow.objects.all())

    class Meta:
        model = CullingRecord
        fields = "__all__"


class QuarantineRecordSerializer(serializers.ModelSerializer):
    cow = serializers.PrimaryKeyRelatedField(queryset=Cow.objects.all())

    class Meta:
        model = QuarantineRecord
        fields = "__all__"


class CowInBarnMovementSerializer(serializers.ModelSerializer):
    """
    Serializer for the CowInBarnMovement model.

    Serializes the following fields:
    - `id`: The unique identifier of the movement.
    - `cow`: The cow associated with the movement.
    - `previous_barn`: The barn from which the cow was previously located (nullable).
    - `new_barn`: The barn to which the cow has been moved.
    - `timestamp`: The timestamp when the movement occurred.

    """

    class Meta:
        model = CowInBarnMovement
        fields = "__all__"


class CowInPenMovementSerializer(serializers.ModelSerializer):
    """
    Serializer for the CowInPenMovement model.

    Serializes the following fields:
    - `id`: The unique identifier of the movement.
    - `cow`: The cow associated with the movement.
    - `previous_pen`: The pen from which the cow was previously located (nullable).
    - `new_pen`: The pen to which the cow has been moved.
    - `timestamp`: The timestamp when the movement occurred.

    """

    class Meta:
        model = CowInPenMovement
        fields = "__all__"


class BarnSerializer(serializers.ModelSerializer):
    """
    Serializer for the Barn model.

    Serializes the following fields:
    - `id`: The unique identifier of the barn.
    - `name`: The name of the barn.
    - `capacity`: The maximum number of cows the barn can hold.

    """

    class Meta:
        model = Barn
        fields = "__all__"


class CowPenSerializer(serializers.ModelSerializer):
    """
    Serializer for the CowPen model.

    Serializes the following fields:
    - `id`: The unique identifier of the cow pen.
    - `barn`: The barn to which the cow pen belongs.
    - `type`: The type of the cow pen (movable or fixed).
    - `category`: The category of the cow pen.
    - `capacity`: The maximum number of cows the pen can hold.

    """

    class Meta:
        model = CowPen
        fields = "__all__"

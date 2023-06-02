from rest_framework import serializers

from .models import *


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
        fields = '__all__'


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
        fields = '__all__'


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
        fields = '__all__'


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
        fields = '__all__'


class CowSerializer(serializers.ModelSerializer):
    """
    Serializer for Cow model instances.

    This serializer includes read-only fields for the cow's tag number, parity, and age.

    #### Attributes:
        - `tag_number (serializers.ReadOnlyField)`: A read-only field representing the tag number of the cow.
        - `parity (serializers.ReadOnlyField)`: A read-only field representing the parity of the cow.
        - `age (serializers.ReadOnlyField)`: A read-only field representing the age of the cow.
    """
    tag_number = serializers.ReadOnlyField()
    parity = serializers.ReadOnlyField()
    age = serializers.ReadOnlyField()

    class Meta:
        model = Cow
        fields = '__all__'


class PregnancySerializer(serializers.ModelSerializer):
    """
    Serializer for Pregnancy model instances.

    This serializer includes read-only fields for due date and pregnancy duration, as well as fields for the cow
    associated with the pregnancy. The cow field is represented by a primary key related field and includes the cow's
    tag number and breed as read-only fields.

    #### Attributes:
        - `due_date (serializers.ReadOnlyField)`: A read-only field representing the due date for the pregnancy.
        - `pregnancy_duration (serializers.ReadOnlyField)`: A read-only field representing the duration of the pregnancy.
        - `cow (serializers.PrimaryKeyRelatedField)`: A field representing the cow associated with the pregnancy.
            This field is represented by a primary key related field.
        - `cow_tag_number (serializers.CharField)`: A read-only field representing the tag number of the cow associated
            with the pregnancy.
        - `cow_breed (serializers.CharField)`: A read-only field representing the breed of the cow associated with the
            pregnancy.
    """
    due_date = serializers.ReadOnlyField()
    pregnancy_duration = serializers.ReadOnlyField()
    cow = serializers.PrimaryKeyRelatedField(queryset=Cow.objects.all())
    cow_tag_number = serializers.CharField(source='cow.tag_number', read_only=True)
    cow_breed = serializers.CharField(source='cow.breed', read_only=True)

    class Meta:
        model = Pregnancy
        fields = '__all__'


class LactationSerializer(serializers.ModelSerializer):
    """
    Serializer for Lactation model instances.

    This serializer includes read-only fields for start date, end date, lactation number, days in lactation, lactation
    stage, and lactation duration, as well as nested serializers for the cow and pregnancy associated with the
    lactation. The cow field is represented by a nested CowSerializer with read-only access, while the pregnancy field
    is represented by a nested PregnancySerializer with read-only access.

    #### Attributes:
        - `start_date (serializers.ReadOnlyField)`: A read-only field representing the start date of the lactation.
        - `end_date (serializers.ReadOnlyField)`: A read-only field representing the end date of the lactation.
        - `cow (CowSerializer)`: A nested serializer representing the cow associated with the lactation. This field has
            read-only access.
        - `lactation_number (serializers.ReadOnlyField)`: A read-only field representing the lactation number.
        - `pregnancy (PregnancySerializer)`: A nested serializer representing the pregnancy associated with the lactation.
            This field has read-only access.
        - `days_in_lactation (serializers.ReadOnlyField)`: A read-only field representing the number of days the cow has
            been in lactation.
        - `lactation_stage (serializers.ReadOnlyField)`: A read-only field representing the stage of lactation the cow is
            in.
        - `lactation_duration (serializers.ReadOnlyField)`: A read-only field representing the duration of the lactation.
    """
    start_date = serializers.ReadOnlyField()
    end_date = serializers.ReadOnlyField()
    cow = CowSerializer(read_only=True)
    lactation_number = serializers.ReadOnlyField()
    pregnancy = PregnancySerializer(read_only=True)
    days_in_lactation = serializers.ReadOnlyField()
    lactation_stage = serializers.ReadOnlyField()
    lactation_duration = serializers.ReadOnlyField()

    class Meta:
        model = Lactation
        fields = "__all__"


class MilkSerializer(serializers.ModelSerializer):
    """
    Serializer for Milk model instances.

    This serializer includes fields for the cow associated with the milk record, as well as a read-only field for the
    lactation associated with the milk record. The cow field is represented by a primary key related field and includes
    the cow's tag number and breed as read-only fields.

    #### Attributes:
        - `lactation (LactationSerializer)`: A read-only field representing the lactation associated with the milk record.
        - `cow (serializers.PrimaryKeyRelatedField)`: A field representing the cow associated with the milk record.
            This field is represented by a primary key related field.
        - `cow_tag_number (serializers.CharField)`: A read-only field representing the tag number of the cow associated
            with the milk record.
        - `cow_breed (serializers.CharField)`: A read-only field representing the breed of the cow associated with the
            milk record.
    """
    lactation = LactationSerializer(read_only=True)
    cow = serializers.PrimaryKeyRelatedField(queryset=Cow.objects.filter(gender='Female'))
    cow_tag_number = serializers.CharField(source='cow.tag_number', read_only=True)
    cow_breed = serializers.CharField(source='cow.breed', read_only=True)

    class Meta:
        model = Milk
        fields = '__all__'


class WeightRecordSerializer(serializers.ModelSerializer):
    """
    Serializer for WeightRecord model instances.

    This serializer includes a field for the cow associated with the weight record. The cow field is represented by a
    primary key related field.

    #### Attributes:
        - `cow (serializers.PrimaryKeyRelatedField)`: A field representing the cow associated with the weight record.
            This field is represented by a primary key related field.
    """
    cow = serializers.PrimaryKeyRelatedField(queryset=Cow.objects.all())

    class Meta:
        model = WeightRecord
        fields = '__all__'


class CullingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Culling
        fields = '__all__'

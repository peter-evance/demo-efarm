from django.db.models import Sum
from rest_framework import serializers

from .models import *

class CowSerializer(serializers.ModelSerializer):
    tag_number = serializers.ReadOnlyField()
    parity = serializers.ReadOnlyField()
    age = serializers.ReadOnlyField()
    class Meta:
        model = Cow
        fields = '__all__'
        
class PregnancySerializer(serializers.ModelSerializer):
    due_date = serializers.ReadOnlyField()
    pregnancy_duration = serializers.ReadOnlyField()
    cow = serializers.PrimaryKeyRelatedField(queryset=Cow.objects.all())
    cow_tag_number = serializers.CharField(source='cow.tag_number', read_only=True)
    cow_breed = serializers.CharField(source='cow.breed', read_only=True)
    class Meta:
        model = Pregnancy
        fields = '__all__'

class LactationSerializer(serializers.ModelSerializer):
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
    lactation = LactationSerializer(read_only=True)
    cow = serializers.PrimaryKeyRelatedField(queryset=Cow.objects.all())
    cow_tag_number = serializers.CharField(source='cow.tag_number', read_only=True)
    cow_breed = serializers.CharField(source='cow.breed', read_only=True)
    class Meta:
        model = Milk
        fields = '__all__'
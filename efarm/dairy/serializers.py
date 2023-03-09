from rest_framework import serializers
from .models import *


class CowSerializer(serializers.ModelSerializer):
    tag_number = serializers.ReadOnlyField()
    parity = serializers.ReadOnlyField()
    age = serializers.ReadOnlyField()
    
    class Meta:
        model = Cow
        fields = '__all__'
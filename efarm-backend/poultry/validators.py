from django.core.exceptions import ValidationError

from poultry.choices import *


class FlockSourceValidator:
    @staticmethod
    def validate_source(name):
        from poultry.models import FlockSource

        if name not in FlockSourceChoices.values:
            raise ValidationError(f"Invalid flock source: '{name}'.")

        if FlockSource.objects.filter(name=name).exists():
            raise ValidationError(f"This flock source '{name}' already exists.")


class FlockBreedValidator:
    @staticmethod
    def validate_breed_name(name):
        from poultry.models import FlockBreed

        if name not in FlockBreedTypeChoices.values:
            raise ValidationError(f"Invalid flock breed: '{name}'.")

        if FlockBreed.objects.filter(name=name).exists():
            raise ValidationError(f"This flock breed '{name}' already exists.")


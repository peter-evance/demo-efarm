
from django.core.exceptions import ValidationError

from dairy.choices import *


class CowBreedValidator:
    @staticmethod
    def validate_unique_name(name):
        """
        Validates that the breed name is unique and belongs to the available choices.

        Args:
        - `name`: The breed name to validate.

        Raises:
        - `ValidationError`: If a breed with the same name already exists or if the breed name is not in the choices.
        """
        from dairy.models import CowBreed

        if name not in CowBreedChoices.values:
            raise ValidationError(f"Invalid cow breed: '{name}'.")

        if CowBreed.objects.filter(name=name).exists():
            raise ValidationError(f"A breed with the name '{name}' already exists.")

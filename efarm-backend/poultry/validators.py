from django.core.exceptions import ValidationError

from poultry.choices import *
from poultry.utils import todays_date


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


class HousingStructureValidator:
    @staticmethod
    def validate_category(category, house_type):
        if category == HousingStructureCategoryChoices.BROODER_CHICK_HOUSE:
            if house_type not in [
                HousingStructureTypeChoices.DEEP_LITTER_HOUSE,
                HousingStructureTypeChoices.CLOSED_SHED,
            ]:
                raise ValidationError(
                    "Brood and chick houses are limited to Deep Litter House or Closed Shed structure types."
                )

        if (
            category == HousingStructureCategoryChoices.BREEDERS_HOUSE
            and house_type == HousingStructureTypeChoices.PASTURE_HOUSING
        ):
            raise ValidationError(
                "Breeder houses are not allowed to have the Pasture Housing structure type."
            )


class FlockValidator:
    @staticmethod
    def validate_chicken_type_update(flock):
        from poultry.models import Flock

        """
        Validates the chicken type of the flock during updates.
        Raises a validation error if the chicken type is being changed.

        """
        if flock.pk:
            old_instance: Flock = Flock.objects.get(pk=flock.pk)
            if old_instance.chicken_type != flock.chicken_type:
                raise ValidationError("Cannot update the chicken type")

    @staticmethod
    def validate_flock_housing(chicken_type, current_housing_structure, age_in_weeks):
        """
        Validates the housing structure assigned to the flock based on its chicken type and age.

        Raises:
        - `ValidationError`: If the assigned housing structure is invalid based on the flock's chicken type and age.

        """
        if (
            chicken_type == ChickenTypeChoices.BROILER
            and current_housing_structure.category
            != HousingStructureCategoryChoices.BROILERS_HOUSE
        ):
            raise ValidationError(
                "Broiler chickens can only be assigned to the Broiler house category."
            )

        if chicken_type == ChickenTypeChoices.LAYERS:
            if 0 <= age_in_weeks <= 8:
                if (
                    current_housing_structure.category
                    != HousingStructureCategoryChoices.BROODER_CHICK_HOUSE
                ):
                    raise ValidationError(
                        "Layers aged 0-8 weeks can only be assigned to the Brooder Chick House."
                    )
            elif 8 < age_in_weeks <= 18:
                if (
                    current_housing_structure.category
                    != HousingStructureCategoryChoices.GROWERS_HOUSE
                ):
                    raise ValidationError(
                        "Layers aged 8-18 weeks can only be assigned to the Growers House."
                    )
            elif 18 < age_in_weeks <= 84:
                if (
                    current_housing_structure.category
                    != HousingStructureCategoryChoices.LAYERS_HOUSE
                ):
                    raise ValidationError(
                        "Layers aged 18-84 weeks can only be assigned to the Layers House."
                    )
            else:
                raise ValidationError("Invalid age range for Layers.")

        if chicken_type == ChickenTypeChoices.MULTI_PURPOSE and age_in_weeks <= 4:
            if (
                current_housing_structure.category
                != HousingStructureCategoryChoices.BROODER_CHICK_HOUSE
            ):
                raise ValidationError(
                    "Multipurpose chickens of 8 weeks and below can only be assigned to the Brooder Chick House."
                )

    @staticmethod
    def validate_flock_date_of_hatching(date_of_hatching):
        if date_of_hatching > todays_date:
            raise ValidationError("Invalid date of hatching, cannot be in future!")


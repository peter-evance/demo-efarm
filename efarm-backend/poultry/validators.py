from datetime import timedelta
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db.models import Sum
from django.utils import timezone

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


class FlockMovementValidator:
    @staticmethod
    def validate_flock_movement(flock, to_structure, from_structure):
        """
        Validates the flock movement based on the rearing method and destination structure.

        Raises:
        - `ValidationError`: If the flock movement is invalid based on the validation rules.

        """
        rearing_method = flock.current_rearing_method
        to_structure_type = to_structure.house_type

        if from_structure == to_structure:
            raise ValidationError(
                "The destination structure cannot be the same as where the flock is removed from."
            )

        if rearing_method == RearingMethodChoices.FREE_RANGE:
            if to_structure_type not in [HousingStructureTypeChoices.PASTURE_HOUSING]:
                raise ValidationError(
                    "Flocks reared under free range can only be assigned to pasture housing."
                )

        if rearing_method == RearingMethodChoices.CAGE_SYSTEM:
            allowed_structures = [
                HousingStructureTypeChoices.OPEN_SIDED_SHED,
                HousingStructureTypeChoices.CLOSED_SHED,
                HousingStructureTypeChoices.BATTERY_CAGE,
                HousingStructureTypeChoices.DEEP_LITTER_HOUSE,
                HousingStructureTypeChoices.SEMI_INTENSIVE_HOUSING,
                HousingStructureTypeChoices.PASTURE_HOUSING,
            ]
            if to_structure_type not in allowed_structures:
                raise ValidationError(
                    "Flocks reared under cage system can only be assigned to specific housing structures."
                )

        if rearing_method == RearingMethodChoices.DEEP_LITTER:
            allowed_structures = [
                HousingStructureTypeChoices.OPEN_SIDED_SHED,
                HousingStructureTypeChoices.CLOSED_SHED,
                HousingStructureTypeChoices.DEEP_LITTER_HOUSE,
            ]
            if to_structure_type not in allowed_structures:
                raise ValidationError(
                    "Flocks reared under deep litter can only be assigned to specific housing structures."
                )

        if rearing_method == RearingMethodChoices.BARN_SYSTEM:
            allowed_structures = [
                HousingStructureTypeChoices.SEMI_INTENSIVE_HOUSING,
                HousingStructureTypeChoices.OPEN_SIDED_SHED,
                HousingStructureTypeChoices.CLOSED_SHED,
                HousingStructureTypeChoices.BATTERY_CAGE,
                HousingStructureTypeChoices.DEEP_LITTER_HOUSE,
                HousingStructureTypeChoices.PASTURE_HOUSING,
            ]
            if to_structure_type not in allowed_structures:
                raise ValidationError(
                    "Flocks reared under barn system can only be assigned to specific housing structures."
                )

        if rearing_method == RearingMethodChoices.PASTURE_BASED:
            allowed_structures = [
                HousingStructureTypeChoices.PASTURE_HOUSING,
                HousingStructureTypeChoices.SEMI_INTENSIVE_HOUSING,
            ]
            if to_structure_type not in allowed_structures:
                raise ValidationError(
                    "Flocks reared under pasture based can only be assigned to specific housing structures."
                )


class FlockInspectionRecordValidator:
    @staticmethod
    def validate_daily_number_of_inspection_records(date_of_inspection):
        from poultry.models import FlockInspectionRecord

        """
        Validates the maximum number of inspection records per day.

        Raises:
        - `ValidationError`: If the maximum number of inspection records per day is exceeded.

        """
        if (
            FlockInspectionRecord.objects.filter(
                date_of_inspection__date=date_of_inspection.date()
            ).count()
            > 3
        ):
            next_day = date_of_inspection + timedelta(days=1)
            next_day_str = next_day.astimezone(
                timezone.get_current_timezone()
            ).strftime("%A, %d %B %Y")
            raise ValidationError(
                f"Only three inspection records are allowed per day. "
                f"The next inspection record can be done on {next_day_str}."
            )

    @staticmethod
    def validate_inspection_record_time_separation(flock, instance):
        from poultry.models import FlockInspectionRecord

        """
        Validates the time separation between inspection records.

        Raises:
        - `ValidationError`: If the time separation between inspection records is less than the threshold.

        """
        time_threshold = timedelta(hours=4)
        existing_records = (
            FlockInspectionRecord.objects.filter(flock=flock)
            .exclude(pk=instance.pk)
            .order_by("date_of_inspection")
        )
        if existing_records:
            last_record = existing_records.last()
            time_difference = (
                instance.date_of_inspection - last_record.date_of_inspection
            )
            if time_difference < time_threshold:
                next_time = last_record.date_of_inspection + time_threshold
                next_time_str = next_time.astimezone(
                    timezone.get_current_timezone()
                ).strftime("%I:%M %p")
                raise ValidationError(
                    f"Minimum 4 hours of separation is required between inspection records. "
                    f"The next inspection record can be done at {next_time_str}."
                )

    @staticmethod
    def validate_number_of_dead_birds(instance):
        """
        Validates that the number of dead birds does not exceed the number of living birds in the flock inventory.

        Raises:
        - `ValidationError`: If the number of dead birds exceeds the number of living birds.

        """
        flock_inventory = instance.flock.inventory
        if instance.number_of_dead_birds > flock_inventory.number_of_alive_birds:
            raise ValidationError(
                f"The number of dead birds cannot exceed the number of alive birds"
                f" in the flock inventory, There is {flock_inventory.number_of_alive_birds} birds, "
                f"You entered {instance.number_of_dead_birds}."
            )
        if instance.number_of_dead_birds < 0:
            raise ValidationError(
                "Invalid entry, The number of dead birds cannot be less than 0"
            )

    @staticmethod
    def validate_flock_availability(flock):
        if not flock.is_present:
            raise ValidationError("This flock is no longer available in the farm.")


class FlockBreedInformationValidator:
    @staticmethod
    def validate_fields(
        chicken_type,
        average_egg_production,
        average_mature_weight_in_kgs,
        maturity_age_in_weeks,
    ):
        if (
            chicken_type == ChickenTypeChoices.BROILER
            and average_egg_production is not None
        ):
            raise ValidationError("Broilers should not have egg production!.")

        if (
            chicken_type != ChickenTypeChoices.BROILER
            and average_egg_production is None
        ):
            raise ValidationError("Average egg production must be provided!.")

        if average_mature_weight_in_kgs < Decimal("1.50"):
            raise ValidationError("Average mature weight should be at least 1.50 Kgs.")

        if chicken_type == ChickenTypeChoices.BROILER and not (
            8 <= maturity_age_in_weeks <= 10
        ):
            raise ValidationError(
                "Broilers should have a maturity age between 8 and 10 weeks."
            )

        if chicken_type == ChickenTypeChoices.LAYERS and not (
            16 <= maturity_age_in_weeks <= 18
        ):
            raise ValidationError(
                "Layers should have a maturity age between 16 and 18 weeks."
            )

        if chicken_type == ChickenTypeChoices.MULTI_PURPOSE and not (
            20 <= maturity_age_in_weeks <= 24
        ):
            raise ValidationError(
                "Multipurpose chickens should have a maturity age between 20 and 24 weeks."
            )


class EggCollectionValidator:
    @staticmethod
    def validate_flock_eligibility(flock):

        if flock.chicken_type not in [ChickenTypeChoices.LAYERS, ChickenTypeChoices.MULTI_PURPOSE]:
            raise ValidationError(f"Egg collection is restricted to layers or multipurpose flocks, "
                                  f"You selected {flock.chicken_type.lower()}.")

        if flock.age_in_weeks < 14:
            raise ValidationError(f"Egg collection is only allowed for flocks of age 14 weeks or older, "
                                  f"This flock is currently {flock.age_in_weeks} weeks old.")
        if not flock.is_present:
            raise ValidationError(f"Egg collection is only allowed for flocks marked as present. This flock was "
                                  f"marked not present on {flock.inventory.last_update.astimezone(timezone.get_current_timezone()).strftime('%A %B %d, %Y')}.")

    @staticmethod
    def validate_egg_collection_records_per_day(flock):
        from poultry.models import EggCollection
        count = EggCollection.objects.filter(flock=flock, date_of_collection=todays_date).count()
        if count >= 3:
            tomorrow = timezone.now().astimezone(timezone.get_current_timezone()).date() + timezone.timedelta(days=1)
            raise ValidationError(f"Data entry for this flock is limited to thrice per day. "
                                  f"Please try again on {tomorrow.strftime('%A %B %d, %Y')}.")

    @staticmethod
    def validate_egg_collection_count(flock, date_of_collection, broken_eggs, collected_eggs, pk):
        from poultry.models import EggCollection

        if broken_eggs > collected_eggs:
            raise ValidationError(
                f"Broken eggs count ({broken_eggs}) cannot be greater than the collected eggs "
                f"count ({collected_eggs})")

        live_bird_count = flock.inventory.number_of_alive_birds
        total_collected_eggs = (
                EggCollection.objects.filter(flock=flock, date_of_collection=date_of_collection).exclude(pk=pk)
                .aggregate(total=Sum('collected_eggs')).get('total') or 0)

        if (total_collected_eggs + collected_eggs) > live_bird_count:
            if live_bird_count - total_collected_eggs <= 0:
                raise ValidationError(
                    f"Collected egg count for the day cannot exceed the count of living birds in the "
                    f"flock, This flock has {live_bird_count} birds. The "
                    f"total collected eggs today is {total_collected_eggs}.")
            raise ValidationError(f"Collected egg count for the day cannot exceed the count of living birds in the "
                                  f"flock, This flock has {live_bird_count} birds, and the collected "
                                  f"eggs today must be {live_bird_count - total_collected_eggs} or lower. The "
                                  f"total collected eggs today is {total_collected_eggs}.")

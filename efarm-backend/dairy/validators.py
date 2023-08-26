from datetime import timedelta

from django.core.exceptions import ValidationError

from dairy.choices import *
from dairy.utils import *


class CowBreedValidator:
    @staticmethod
    def validate_name(name):
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

    @staticmethod
    def validate_update(pk):
        """
        Validates that updates are not allowed for cow breeds.

        Args:
        - `pk` (int or None): The primary key of the cow breed instance.

        Raises:
        - `ValidationError`: Always raised to prevent updates.
        """
        if pk is not None:
            raise ValidationError("Updates are not allowed for cow breeds.")


class CowValidator:
    """
    Provides validation methods for the Cow model.

    Methods:
    - `validate_uniqueness(name)`: Validates the uniqueness of the cow's name.
    - `validate_cow_age(date_of_birth)`: Validates the age of the cow based on the date of birth.
    - `validate_date_of_death(availability_status, date_of_death)`: Validates the date of death for a cow with 'Dead' status.
    - `validate_pregnancy_status(age, pregnancy_status)`: Validates the pregnancy status of the cow based on its age.
    - `validate_pregnancy_status_for_dead_cow(pregnancy_status, availability_status)`: Validates the pregnancy status for a dead cow.
    - `validate_pregnancy_status_for_male_cow(pregnancy_status, gender)`: Validates the pregnancy status for a male cow.
    - `validate_gender_update(pk, gender)`: Validates the update of the cow's gender based on the existence of the primary key.
    - `validate_name(name)`: Validates the name of the cow.
    - `validate_sire_dam_relationship(sire, dam)`: Validates the sire-dam relationship.
    - `validate_introduction_date(date_introduced_in_farm)`: Validates the date of introduction to the farm.
    - `validate_production_status(production_status, gender, category, age, calf_records, is_bought )`: Validates the production status of the cow based on its gender, category, and age.
    - `validate_age_category(age, category, gender, calf_records, is_bought)`: Validates the age category of the cow based on its age, gender, calf records, and whether it was bought.
    """

    @staticmethod
    def validate_uniqueness(name):
        """
        Validates the uniqueness of the cow's name.

        Args:
        - `name`: The name of the cow.

        Raises:
        - `ValidationError`: If a cow with the same name already exists.
        """

        if len(name) < 3:
            raise ValidationError("Cow name should have at least 3 characters.")

        if not name.replace(" ", "").isalpha():
            raise ValidationError("Cow name should only contain alphabetic characters (no numerics allowed).")

        # if Cow.objects.filter(name=name).exists():
        #     raise ValidationError("A cow with this name already exists.")

    @staticmethod
    def validate_cow_age(age, date_of_birth):
        """
        Validates the age of the cow based on the date of birth.

        Args:
        - `date_of_birth`: The date of birth of a cow.

        Raises:
        - `ValidationError`: If the cow's age exceeds 7 years or the date of birth is in the future.
        """

        if age / 365 > 7:
            raise ValidationError(
                f"Cow cannot be older than 7 years! Current age specified: {round((age / 365), 2)} years")
        if date_of_birth > todays_date:
            raise ValidationError(f"Date of birth cannot be in the future. You entered {date_of_birth}")

    @staticmethod
    def validate_date_of_death(availability_status, date_of_death):
        """
        Validates that a date of death is specified if the cow's status is set to 'Dead'.

        Args:
        - `date_of_death`: The date the cow died.

        Raises:
        - `ValidationError`: If the date of death is not provided, is in the future, or exceeds 24 hours from the
                             current date.

        """
        if availability_status == CowAvailabilityChoices.DEAD:
            if not date_of_death:
                raise ValidationError("Sorry, this cow died! Update its status by adding the date of death.")
            if date_of_death > todays_date:
                raise ValidationError(f"Date of death cannot be in the future. You entered {date_of_death}")
            if (todays_date - date_of_death).days > 1:
                raise ValidationError("Date of death entries longer than 24 hours ago are not allowed.")

    @staticmethod
    def validate_pregnancy_status(cow, age, pregnancy_status, availability_status, gender):
        """
        Validates the pregnancy status of the cow based on its age, availability status, and gender.

        Args:
        - `pregnancy_status`: The pregnancy status of the cow.
        - `age`: The age of the cow in days.
        - `availability_status`: The availability status of the cow.
        - `gender`: The gender of the cow.

        Raises:
        - `ValidationError`: If the cow is set as pregnant and its age is less than 12 months,
          or if the cow is dead but has a pregnancy status other than 'Unavailable',
          or if the cow is male and has a pregnancy status other than 'Unavailable'.

        """

        if (age / 30.417) < 12 and pregnancy_status != CowPregnancyChoices.UNAVAILABLE:
            raise ValidationError(
                f"Cows must be 12 months or older to be set as pregnant or open. Current age: {round((age / 30.417), 2)} months old.")

        if availability_status == CowAvailabilityChoices.DEAD and pregnancy_status != CowPregnancyChoices.UNAVAILABLE:
            raise ValidationError(
                f"Dead cows can only have an 'Unavailable' status. You cannot set them as {pregnancy_status}.")

        if gender == SexChoices.MALE and pregnancy_status != CowPregnancyChoices.UNAVAILABLE:
            raise ValidationError(
                f"Male cows can only have an 'Unavailable' status. You cannot set them as {pregnancy_status}.")

        has_pregnancy_records = cow.pregnancies.exists()

        if has_pregnancy_records:
            latest_pregnancy = cow.pregnancies.latest('date_of_calving')
            if cow.current_pregnancy_status != CowPregnancyChoices.CALVED and todays_date - latest_pregnancy.date_of_calving < timedelta(
                    days=60):
                raise ValidationError(
                    f"This cow gave birth recently and must be marked as 'Calved'. Not ({cow.current_pregnancy_status})")
        else:
            if cow.current_pregnancy_status not in [CowPregnancyChoices.OPEN,
                                                    CowPregnancyChoices.UNAVAILABLE]:
                raise ValidationError(f"Invalid pregnancy status, Must be one of the following: "
                                      f"{CowPregnancyChoices.OPEN, CowPregnancyChoices.UNAVAILABLE, CowPregnancyChoices.OPEN}")

    @staticmethod
    def validate_gender_update(pk, gender):
        """
        Validates the update of the cow's gender based on the existence of the primary key.

        Args:
        - `gender`: The updated gender of the cow.
        - `pk`: The primary key of the cow.

        Raises:
        - `ValidationError`: If the gender update is not allowed.

        """
        from dairy.models import Cow
        if pk is not None:
            old_instance: Cow = Cow.objects.get(pk=pk)
            if old_instance.gender != gender:
                raise ValidationError(f"Cannot update the gender of the cow to: {gender} from {old_instance.gender}!.")

    @staticmethod
    def validate_sire_dam_relationship(sire, dam):
        """
        Validates the sire-dam relationship.
        """
        if sire or dam and sire.gender != SexChoices.MALE:
            raise ValidationError("The sire should be a male cow.")
        if dam or sire and dam.gender != SexChoices.FEMALE:
            raise ValidationError("The dam should be a female cow.")

    @staticmethod
    def validate_introduction_date(date_introduced_in_farm):
        """
        Validates the date of introduction to the farm.
        """
        if date_introduced_in_farm > todays_date:
            raise ValidationError(f"Date of introduction cannot be in the future: ({date_introduced_in_farm}).")

    @staticmethod
    def validate_production_status(production_status, gender, category, age, calf_records, is_bought, cow):
        """
        Validates the production status of the cow based on its gender, category, age, and calf records.

        Args:
        - `production_status`: The production status of the cow.
        - `gender`: The gender of the cow.
        - `category`: The category of the cow.
        - `age`: The age of the cow in days.
        - `calf_records`: A list of calf records for the cow.
        - `is_bought`: A boolean indicating if the cow is bought or not.

        Raises:
        - `ValidationError`: If the production status is invalid based on the cow's gender, category, age,
         and calf records.
        """
        from dairy.models import Pregnancy

        if production_status not in CowProductionStatusChoices.values:
            raise ValidationError(f"Invalid cow production status: '{production_status}'.")

        if gender == SexChoices.MALE:
            if age <= 90:
                if production_status != CowProductionStatusChoices.CALF:
                    raise ValidationError(f"Male calves under 90 days old should have the 'Calf' production status, "
                                          f"not '{production_status}'.")
            elif 90 < age <= 180:
                if production_status != CowProductionStatusChoices.WEANER:
                    raise ValidationError(
                        f"Young male cows between 91 and 180 days old should have the 'Weaner' production status, "
                        f"not '{production_status}'.")
            elif 180 < age <= 365:
                if production_status != CowProductionStatusChoices.YOUNG_BULL:
                    raise ValidationError(
                        f"Young male cows between 181 and 365 days old should have the 'Young Bull' production status, "
                        f"not '{production_status}'.")
            elif 365 < age <= 730:
                if production_status != CowProductionStatusChoices.BULL:
                    raise ValidationError(
                        f"Male cows between 1 and 2 years old should have the 'Bull' production status, "
                        f"not '{production_status}'.")
            elif age > 730:
                if production_status != CowProductionStatusChoices.MATURE_BULL:
                    raise ValidationError(
                        f"Male cows over 2 years old should have the 'Mature Bull' production status, "
                        f"not '{production_status}'.")
        else:  # Female cow
            if age <= 90:
                if production_status != CowProductionStatusChoices.CALF:
                    raise ValidationError(f"Female calves under 90 days should have the 'Calf' production status, "
                                          f"not '{production_status}'.")
            elif 90 < age <= 180:
                if production_status != CowProductionStatusChoices.WEANER:
                    raise ValidationError(
                        f"Female calves between 91 and 180 days should have the 'Weaner' production status, "
                        f"not '{production_status}'.")
            elif 180 < age <= 365:
                if production_status != CowProductionStatusChoices.YOUNG_HEIFER:
                    raise ValidationError(
                        f"Young female cows between 181 and 365 days should have the 'Young Heifer' production status, "
                        f"not '{production_status}'.")
            elif age > 365:
                if category == CowCategoryChoices.HEIFER:
                    if is_bought:
                        if production_status not in [CowProductionStatusChoices.OPEN,
                                                     CowProductionStatusChoices.PREGNANT_NOT_LACTATING]:
                            raise ValidationError(
                                f"Bought heifers should have the 'Open' or 'Pregnant not Lactating' production status, "
                                f"not '{production_status}'.")
                    else:
                        if production_status not in [CowProductionStatusChoices.OPEN,
                                                     CowProductionStatusChoices.PREGNANT_NOT_LACTATING,
                                                     CowProductionStatusChoices.CULLED]:
                            raise ValidationError(
                                f"Heifers should have one of the following production statuses: "
                                f"'Open', 'Pregnant not Lactating', or 'Culled', "
                                f"not '{production_status}'.")
                elif category == CowCategoryChoices.MILKING_COW:
                    if is_bought:
                        if production_status not in [CowProductionStatusChoices.OPEN,
                                                     CowProductionStatusChoices.PREGNANT_AND_LACTATING,
                                                     CowProductionStatusChoices.DRY]:
                            raise ValidationError(
                                f"Bought cows categorized as 'Milking Cow' should have the 'Open', 'Pregnant and "
                                f"Lactating', or 'Dry' production status, not '{production_status}'.")
                    else:
                        if any(calf_records) or len(list(Pregnancy.objects.filter(cow=cow))) > 0:
                            if production_status not in [CowProductionStatusChoices.OPEN,
                                                         CowProductionStatusChoices.DRY,
                                                         CowProductionStatusChoices.PREGNANT_NOT_LACTATING,
                                                         CowProductionStatusChoices.PREGNANT_AND_LACTATING,
                                                         CowProductionStatusChoices.CULLED]:
                                raise ValidationError(
                                    f"Female cows with calf records should have one of the following production "
                                    f"statuses: 'Open', 'Dry', 'Pregnant not Lactating', 'Pregnant and Lactating', or "
                                    f"'Culled', not '{production_status}'.")
                        else:
                            raise ValidationError(
                                f"Female cows categorized as 'Milking Cow' over 1 year old must be associated with calf"
                                f" records.")
                else:
                    raise ValidationError(f"Invalid cow category: '{category}'.")

    @staticmethod
    def validate_age_category(age, category, gender, calf_records, is_bought, cow):
        from dairy.models import Pregnancy
        if category not in CowCategoryChoices.values:
            raise ValidationError(f"Invalid cow category: ({category}).")

        if age < 90:
            if category != CowCategoryChoices.CALF:
                raise ValidationError("Cows under 90 days should have the 'Calf' category.")
        elif 90 <= age <= 180:
            if category != CowCategoryChoices.WEANER:
                raise ValidationError("Cows between 90 and 180 days should have the 'Weaner' category.")
        elif age > 180:
            if is_bought and gender == SexChoices.FEMALE:
                if category not in [CowCategoryChoices.HEIFER, CowCategoryChoices.MILKING_COW]:
                    raise ValidationError(
                        f"Bought cows at {round(age / 30.417)} months old should have the 'Heifer' or 'Milking Cow' "
                        f"category, Not: ({category}) ")
            elif is_bought and gender == SexChoices.MALE:
                if category != CowCategoryChoices.BULL:
                    raise ValidationError(
                        f"Bought bulls at {round(age / 30.417)} months old should have the 'Bull' category, Not: ({category}) ")
            else:
                if gender == SexChoices.FEMALE:
                    if any(calf_records) or len(list(Pregnancy.objects.filter(cow=cow))) > 0:
                        if category != CowCategoryChoices.MILKING_COW:
                            raise ValidationError(
                                f"Cows with calf records should have the 'Milking Cow' category, Not: ({category})")
                    else:
                        if category != CowCategoryChoices.HEIFER:
                            raise ValidationError(
                                f"Cows with no calf history should have the 'Heifer' category, Not: ({category})")
                else:
                    if category != CowCategoryChoices.BULL:
                        raise ValidationError(f"Male cows should have the 'Bull' category, Not: ({category})")


class HeatValidator:
    @staticmethod
    def validate_observation_time(observation_time):
        if observation_time > timezone.now():
            raise ValidationError("Observation time cannot be in the future.")

    @staticmethod
    def validate_pregnancy(cow):
        if cow.current_pregnancy_status == CowPregnancyChoices.PREGNANT:
            raise ValidationError("Cow is already pregnant.")

    @staticmethod
    def validate_production_status(cow):
        if cow.current_production_status != CowProductionStatusChoices.OPEN:
            raise ValidationError(
                f"Cow must be open and ready to be served. This cow is marked as {cow.current_production_status}"
            )

    @staticmethod
    def validate_already_in_heat(cow):
        if cow.heat_records.filter(
            observation_time__range=(timezone.now() - timedelta(days=1), timezone.now())
        ).exists():
            raise ValidationError("Cow is already in heat within the past day.")

    @staticmethod
    def validate_dead(cow):
        if cow.availability_status == CowAvailabilityChoices.DEAD:
            raise ValidationError("Cow is dead and cannot be in heat.")

    @staticmethod
    def validate_gender(cow):
        if cow.gender == SexChoices.MALE:
            raise ValidationError("Heat can only be observed in female cows.")

    @staticmethod
    def validate_within_60_days_after_calving(cow, observation_time):
        has_pregnancy_records = cow.pregnancies.exists()

        if has_pregnancy_records:
            latest_pregnancy = cow.pregnancies.latest("-date_of_calving")
            if (
                cow.current_pregnancy_status == CowPregnancyChoices.CALVED
                and observation_time.date() - latest_pregnancy.date_of_calving
                < timedelta(days=60)
            ):
                raise ValidationError(
                    "Cow cannot be in heat within 60 days after calving."
                )

    @staticmethod
    def validate_within_21_days_of_previous_heat(cow, observation_time):
        if cow.heat_records.filter(
            observation_time__range=(
                observation_time - timedelta(days=21),
                observation_time,
            )
        ).exists():
            raise ValidationError(
                "Cow cannot be in heat within 21 days of previous heat observation."
            )

    @staticmethod
    def validate_min_age(cow):
        if cow.age < 365:
            raise ValidationError("Cow must be at least 12 months old to be in heat.")

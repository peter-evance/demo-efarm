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
            raise ValidationError(
                "Cow name should only contain alphabetic characters (no numerics allowed)."
            )

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
                f"Cow cannot be older than 7 years! Current age specified: {round((age / 365), 2)} years"
            )
        if date_of_birth > todays_date:
            raise ValidationError(
                f"Date of birth cannot be in the future. You entered {date_of_birth}"
            )

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
                raise ValidationError(
                    "Sorry, this cow died! Update its status by adding the date of death."
                )
            if date_of_death > todays_date:
                raise ValidationError(
                    f"Date of death cannot be in the future. You entered {date_of_death}"
                )
            if (todays_date - date_of_death).days > 1:
                raise ValidationError(
                    "Date of death entries longer than 24 hours ago are not allowed."
                )

    @staticmethod
    def validate_pregnancy_status(
        cow, age, pregnancy_status, availability_status, gender
    ):
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
                f"Cows must be 12 months or older to be set as pregnant or open. Current age: {round((age / 30.417), 2)} months old."
            )

        if (
            availability_status == CowAvailabilityChoices.DEAD
            and pregnancy_status != CowPregnancyChoices.UNAVAILABLE
        ):
            raise ValidationError(
                f"Dead cows can only have an 'Unavailable' status. You cannot set them as {pregnancy_status}."
            )

        if (
            gender == SexChoices.MALE
            and pregnancy_status != CowPregnancyChoices.UNAVAILABLE
        ):
            raise ValidationError(
                f"Male cows can only have an 'Unavailable' status. You cannot set them as {pregnancy_status}."
            )

        has_pregnancy_records = cow.pregnancies.exists()

        if has_pregnancy_records:
            latest_pregnancy = cow.pregnancies.latest("date_of_calving")
            if (
                cow.current_pregnancy_status != CowPregnancyChoices.CALVED
                and todays_date - latest_pregnancy.date_of_calving < timedelta(days=60)
            ):
                raise ValidationError(
                    f"This cow gave birth recently and must be marked as 'Calved'. Not ({cow.current_pregnancy_status})"
                )
        else:
            if cow.current_pregnancy_status not in [
                CowPregnancyChoices.OPEN,
                CowPregnancyChoices.UNAVAILABLE,
            ]:
                raise ValidationError(
                    f"Invalid pregnancy status, Must be one of the following: "
                    f"{CowPregnancyChoices.OPEN, CowPregnancyChoices.UNAVAILABLE, CowPregnancyChoices.OPEN}"
                )

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
                raise ValidationError(
                    f"Cannot update the gender of the cow to: {gender} from {old_instance.gender}!."
                )

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
            raise ValidationError(
                f"Date of introduction cannot be in the future: ({date_introduced_in_farm})."
            )

    @staticmethod
    def validate_production_status(
        production_status, gender, category, age, calf_records, is_bought, cow
    ):
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
            raise ValidationError(
                f"Invalid cow production status: '{production_status}'."
            )

        if gender == SexChoices.MALE:
            if age <= 90:
                if production_status != CowProductionStatusChoices.CALF:
                    raise ValidationError(
                        f"Male calves under 90 days old should have the 'Calf' production status, "
                        f"not '{production_status}'."
                    )
            elif 90 < age <= 180:
                if production_status != CowProductionStatusChoices.WEANER:
                    raise ValidationError(
                        f"Young male cows between 91 and 180 days old should have the 'Weaner' production status, "
                        f"not '{production_status}'."
                    )
            elif 180 < age <= 365:
                if production_status != CowProductionStatusChoices.YOUNG_BULL:
                    raise ValidationError(
                        f"Young male cows between 181 and 365 days old should have the 'Young Bull' production status, "
                        f"not '{production_status}'."
                    )
            elif 365 < age <= 730:
                if production_status != CowProductionStatusChoices.BULL:
                    raise ValidationError(
                        f"Male cows between 1 and 2 years old should have the 'Bull' production status, "
                        f"not '{production_status}'."
                    )
            elif age > 730:
                if production_status != CowProductionStatusChoices.MATURE_BULL:
                    raise ValidationError(
                        f"Male cows over 2 years old should have the 'Mature Bull' production status, "
                        f"not '{production_status}'."
                    )
        else:  # Female cow
            if age <= 90:
                if production_status != CowProductionStatusChoices.CALF:
                    raise ValidationError(
                        f"Female calves under 90 days should have the 'Calf' production status, "
                        f"not '{production_status}'."
                    )
            elif 90 < age <= 180:
                if production_status != CowProductionStatusChoices.WEANER:
                    raise ValidationError(
                        f"Female calves between 91 and 180 days should have the 'Weaner' production status, "
                        f"not '{production_status}'."
                    )
            elif 180 < age <= 365:
                if production_status != CowProductionStatusChoices.YOUNG_HEIFER:
                    raise ValidationError(
                        f"Young female cows between 181 and 365 days should have the 'Young Heifer' production status, "
                        f"not '{production_status}'."
                    )
            elif age > 365:
                if category == CowCategoryChoices.HEIFER:
                    if is_bought:
                        if production_status not in [
                            CowProductionStatusChoices.OPEN,
                            CowProductionStatusChoices.PREGNANT_NOT_LACTATING,
                        ]:
                            raise ValidationError(
                                f"Bought heifers should have the 'Open' or 'Pregnant not Lactating' production status, "
                                f"not '{production_status}'."
                            )
                    else:
                        if production_status not in [
                            CowProductionStatusChoices.OPEN,
                            CowProductionStatusChoices.PREGNANT_NOT_LACTATING,
                            CowProductionStatusChoices.CULLED,
                        ]:
                            raise ValidationError(
                                f"Heifers should have one of the following production statuses: "
                                f"'Open', 'Pregnant not Lactating', or 'Culled', "
                                f"not '{production_status}'."
                            )
                elif category == CowCategoryChoices.MILKING_COW:
                    if is_bought:
                        if production_status not in [
                            CowProductionStatusChoices.OPEN,
                            CowProductionStatusChoices.PREGNANT_AND_LACTATING,
                            CowProductionStatusChoices.DRY,
                        ]:
                            raise ValidationError(
                                f"Bought cows categorized as 'Milking Cow' should have the 'Open', 'Pregnant and "
                                f"Lactating', or 'Dry' production status, not '{production_status}'."
                            )
                    else:
                        if (
                            any(calf_records)
                            or len(list(Pregnancy.objects.filter(cow=cow))) > 0
                        ):
                            if production_status not in [
                                CowProductionStatusChoices.OPEN,
                                CowProductionStatusChoices.DRY,
                                CowProductionStatusChoices.PREGNANT_NOT_LACTATING,
                                CowProductionStatusChoices.PREGNANT_AND_LACTATING,
                                CowProductionStatusChoices.CULLED,
                            ]:
                                raise ValidationError(
                                    f"Female cows with calf records should have one of the following production "
                                    f"statuses: 'Open', 'Dry', 'Pregnant not Lactating', 'Pregnant and Lactating', or "
                                    f"'Culled', not '{production_status}'."
                                )
                        else:
                            raise ValidationError(
                                f"Female cows categorized as 'Milking Cow' over 1 year old must be associated with calf"
                                f" records."
                            )
                else:
                    raise ValidationError(f"Invalid cow category: '{category}'.")

    @staticmethod
    def validate_age_category(age, category, gender, calf_records, is_bought, cow):
        from dairy.models import Pregnancy

        if category not in CowCategoryChoices.values:
            raise ValidationError(f"Invalid cow category: ({category}).")

        if age < 90:
            if category != CowCategoryChoices.CALF:
                raise ValidationError(
                    "Cows under 90 days should have the 'Calf' category."
                )
        elif 90 <= age <= 180:
            if category != CowCategoryChoices.WEANER:
                raise ValidationError(
                    "Cows between 90 and 180 days should have the 'Weaner' category."
                )
        elif age > 180:
            if is_bought and gender == SexChoices.FEMALE:
                if category not in [
                    CowCategoryChoices.HEIFER,
                    CowCategoryChoices.MILKING_COW,
                ]:
                    raise ValidationError(
                        f"Bought cows at {round(age / 30.417)} months old should have the 'Heifer' or 'Milking Cow' "
                        f"category, Not: ({category}) "
                    )
            elif is_bought and gender == SexChoices.MALE:
                if category != CowCategoryChoices.BULL:
                    raise ValidationError(
                        f"Bought bulls at {round(age / 30.417)} months old should have the 'Bull' category, Not: ({category}) "
                    )
            else:
                if gender == SexChoices.FEMALE:
                    if (
                        any(calf_records)
                        or len(list(Pregnancy.objects.filter(cow=cow))) > 0
                    ):
                        if category != CowCategoryChoices.MILKING_COW:
                            raise ValidationError(
                                f"Cows with calf records should have the 'Milking Cow' category, Not: ({category})"
                            )
                    else:
                        if category != CowCategoryChoices.HEIFER:
                            raise ValidationError(
                                f"Cows with no calf history should have the 'Heifer' category, Not: ({category})"
                            )
                else:
                    if category != CowCategoryChoices.BULL:
                        raise ValidationError(
                            f"Male cows should have the 'Bull' category, Not: ({category})"
                        )


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


class InseminationValidator:
    @staticmethod
    def validate_already_in_heat(cow, date_of_insemination):
        from dairy.models import Heat

        if not Heat.objects.filter(
            cow=cow,
            observation_time__range=(
                date_of_insemination - timedelta(hours=12),
                date_of_insemination,
            ),
        ).exists():
            raise ValidationError("Cow must be in heat at the time of insemination.")

    @staticmethod
    def validate_within_21_days_of_previous_insemination(pk, cow):
        if pk is None:
            if cow.inseminations.filter(
                date_of_insemination__range=(
                    timezone.now() - timedelta(days=21),
                    timezone.now(),
                )
            ).exists():
                raise ValidationError(
                    "Cow cannot be inseminated within 21 days of a previous insemination."
                )


class PregnancyValidator:
    @staticmethod
    def validate_age(age, start_date, cow):
        if age < 365:
            raise ValidationError(
                "This cow must have a pregnancy threshold age of 1 year. "
                f"This cow is {round(age / 30.417, 2)} months old."
            )
        if not start_date:
            raise ValidationError(f"Provide pregnancy start date.")

        if (start_date - cow.date_of_birth).days < 0:
            raise ValidationError(f"Invalid start date.")

        if (start_date - cow.date_of_birth).days < 365:
            raise ValidationError(
                f"Invalid start date. Cow can not be pregnant at "
                f"{round((start_date - cow.date_of_birth).days / 30.417, 2)} months of age."
            )

    @staticmethod
    def validate_cow_current_pregnancy_status(cow):
        if cow.current_pregnancy_status == CowPregnancyChoices.PREGNANT:
            raise ValidationError("This cow is already pregnant!")
        if cow.current_pregnancy_status == CowPregnancyChoices.CALVED:
            raise ValidationError("This cow just gave birth recently!")
        if cow.current_pregnancy_status == CowPregnancyChoices.UNAVAILABLE:
            raise ValidationError("This cow is not ready!")

    @staticmethod
    def validate_cow_availability_status(cow):
        if cow.availability_status == CowAvailabilityChoices.DEAD:
            raise ValidationError("Cannot add pregnancy record for a dead cow.")

        if cow.availability_status == CowAvailabilityChoices.SOLD:
            raise ValidationError("Cannot add pregnancy record for a sold cow.")

    @staticmethod
    def validate_pregnancy_status(pregnancy_status, start_sate, pregnancy_failed_date):
        if pregnancy_status not in PregnancyStatusChoices.values:
            raise ValidationError(f"Invalid pregnancy status: '{pregnancy_status}'.")

        if (
            pregnancy_status == PregnancyStatusChoices.FAILED
            and not pregnancy_failed_date
        ):
            raise ValidationError(
                "Pregnancy is marked as failed, provide the date of failure"
            )

        if (todays_date - start_sate) < timedelta(
            days=21
        ) and pregnancy_status != PregnancyStatusChoices.UNCONFIRMED:
            raise ValidationError(
                f"Confirm the pregnancy status on {start_sate + timedelta(days=21)}"
            )

    @staticmethod
    def validate_dates(
        start_date,
        pregnancy_status,
        date_of_calving,
        pregnancy_scan_date,
        pregnancy_failed_date,
    ):
        if start_date > todays_date:
            raise ValidationError("Start date cannot be in the future.")

        if date_of_calving and start_date:
            if date_of_calving < start_date:
                raise ValidationError("Date of calving must be after the start date.")

            if date_of_calving > todays_date:
                raise ValidationError("Calving date cannot be in the future.")

            min_days_between_calving_and_start = 270
            max_days_between_calving_and_start = 295
            days_difference = (date_of_calving - start_date).days
            if not (
                min_days_between_calving_and_start
                <= days_difference
                <= max_days_between_calving_and_start
            ):
                raise ValidationError(
                    f"Difference between calving date and start date should be between 270 and 295 days. "
                    f"Current difference {days_difference} day(s)"
                )

        if pregnancy_scan_date and start_date:
            if pregnancy_scan_date < start_date:
                raise ValidationError(
                    "Pregnancy scan date must be after the start date."
                )

            if pregnancy_scan_date.date() > todays_date:
                raise ValidationError("Pregnancy scan date cannot be in the future.")

            min_days_after_start_date_for_scan = 21
            max_days_after_start_date_for_scan = 60
            days_after_start_date_for_scan = (pregnancy_scan_date - start_date).days
            if not (
                min_days_after_start_date_for_scan
                <= days_after_start_date_for_scan
                <= max_days_after_start_date_for_scan
            ):
                raise ValidationError(
                    f"Scan date should be between 21 and 60 days from the start date."
                    f"Currently {days_after_start_date_for_scan} elapsed."
                )

        if pregnancy_failed_date and start_date:
            if pregnancy_failed_date > todays_date:
                raise ValidationError("Pregnancy failed date cannot be in the future.")

            if pregnancy_failed_date < start_date:
                raise ValidationError(
                    "Pregnancy failed date cannot be before the start date."
                )

            if (
                pregnancy_failed_date
                and pregnancy_status != PregnancyStatusChoices.FAILED
            ):
                raise ValidationError(
                    "Pregnancy status must be 'Failed' if pregnancy failed date is provided."
                )

            min_days_after_start_date_for_failure = 21
            max_days_after_start_date_for_failure = 295
            days_after_start_date_for_failure = (
                pregnancy_failed_date - start_date
            ).days
            if not (
                min_days_after_start_date_for_failure
                <= days_after_start_date_for_failure
                <= max_days_after_start_date_for_failure
            ):
                raise ValidationError(
                    "Pregnancy failed date must be between 21 and 295 days from the start date."
                )

    @staticmethod
    def validate_outcome(pregnancy_outcome, pregnancy_status, date_of_calving):
        if pregnancy_outcome:
            if pregnancy_outcome not in PregnancyOutcomeChoices.values:
                raise ValidationError(
                    f"Invalid pregnancy outcome: '{pregnancy_outcome}'."
                )

            if (
                pregnancy_outcome
                in [PregnancyOutcomeChoices.LIVE, PregnancyOutcomeChoices.STILLBORN]
                and pregnancy_status != PregnancyStatusChoices.CONFIRMED
            ):
                raise ValidationError(
                    f"Pregnancy status must be 'Confirmed' if the pregnancy outcome is '{pregnancy_outcome}'."
                )

            if (
                pregnancy_outcome == PregnancyOutcomeChoices.LIVE
                and not date_of_calving
            ):
                raise ValidationError(
                    f"Date of calving must be provided if the pregnancy outcome is '{pregnancy_outcome}'."
                )

            if (
                pregnancy_outcome == PregnancyOutcomeChoices.MISCARRIAGE
                and pregnancy_status != PregnancyStatusChoices.FAILED
            ):
                raise ValidationError(
                    f"Pregnancy status must be 'Failed' if the pregnancy outcome is 'Miscarriage'. "
                    f"Currently its {pregnancy_status}"
                )

        if date_of_calving and pregnancy_outcome not in [
            PregnancyOutcomeChoices.LIVE,
            PregnancyOutcomeChoices.STILLBORN,
        ]:
            raise ValidationError(f"Provide the pregnancy outcome")


class LactationValidator:
    @staticmethod
    def validate_age(start_date, cow):
        if start_date < cow.date_of_birth + timedelta(
            days=635
        ):  # Literally, this is the one-year age plus the pregnancy duration of 270 days
            raise ValidationError(
                f"Invalid start date. Lactation of this Cow must have started/yet to around {cow.date_of_birth + timedelta(days=635)} and thus can"
                f"not be {start_date}."
            )

    @staticmethod
    def validate_cow_origin(cow):
        if not cow.is_bought:
            raise ValidationError("Manual entry must be only on bought cows.")

    @staticmethod
    def validate_cow_category(category):
        if category not in CowCategoryChoices.values:
            raise ValidationError(f"Invalid cow category: ({category}).")
        if category != CowCategoryChoices.MILKING_COW:
            raise ValidationError(
                f"Only bought cows which have calved down are allowed. This cow is categorised as ({category}). "
                f"Manual entry forbidden"
            )

    @staticmethod
    def validate_fields(start_date, pregnancy, lactation_number, cow, lactation):
        if start_date > todays_date:
            raise ValidationError("Start date cannot be in the future.")

        if lactation.end_date and lactation.end_date > todays_date:
            raise ValidationError("Start date cannot be in the future.")

        if cow.is_bought and pregnancy is not None:
            raise ValidationError(
                f"Pregnancy must be NULL for this lactation record No.({lactation_number}), This cow ({cow.tag_number}) never gave birth in this farm! "
                f"It was brought to the farm on {cow.date_introduced_in_farm}"
            )

        if ((cow.age - 635) / 305) < 1 and lactation_number != 1:
            raise ValidationError("Invalid lactation number")


class MilkValidator:
    @staticmethod
    def validate_amount_in_kgs(amount_in_kgs):
        if amount_in_kgs < 0:
            raise ValidationError("Invalid amount!")
        if amount_in_kgs > 35:
            raise ValidationError(
                f"Amount {amount_in_kgs} Kgs exceeds the maximum expected capacity of 35 kgs!"
            )

    @staticmethod
    def validate_cow_eligibility(cow):
        from dairy.models import Lactation

        if cow.availability_status == CowAvailabilityChoices.DEAD:
            raise ValidationError("Cannot add milk record for a dead cow.")

        if cow.availability_status == CowAvailabilityChoices.SOLD:
            raise ValidationError("Cannot add milk record for sold cow.")

        if cow.gender != SexChoices.FEMALE:
            raise ValidationError("This cow is a Bull and cannot produce milk!")

        if round((cow.age / 30.417), 2) < 20.88:
            raise ValidationError(
                f"Cow is less than 21 months old and should not have a milk record. It is currently: {round((cow.age / 30.417), 2)} months old"
            )

        lactation = Lactation.objects.filter(cow=cow).latest()
        if lactation is None:
            raise ValidationError("Cannot add milk entry, cow has no active lactation")

        if lactation and lactation.lactation_stage == LactationStageChoices.DRY:
            raise ValidationError("Cannot add milk entry, Cow has been dried off")

        if lactation and lactation.lactation_stage == LactationStageChoices.ENDED:
            raise ValidationError("Cannot add milk entry, Previous Lactation Ended!")


class WeightRecordValidator:
    @staticmethod
    def validate_weight(weight_in_kgs):
        if weight_in_kgs < 10:
            raise ValidationError(f"A cow can not be less than 10kgs")
        if weight_in_kgs > 1500:
            raise ValidationError(f"A cows weight can not exceed 1500 kgs")

    @staticmethod
    def validate_cow_availability_status(cow):
        if cow.availability_status != CowAvailabilityChoices.ALIVE:
            raise ValidationError(
                f"Weight records only allowed for cows present in the farm. "
                f"This cow is marked as: {cow.availability_status}"
            )

    @staticmethod
    def validate_frequency_of_weight_records(date, cow):
        from dairy.models import WeightRecord

        if WeightRecord.objects.filter(cow=cow, date=date).count() > 1:
            raise ValidationError("This cow is already weighed on this date")


class CullingValidator:
    @staticmethod
    def validate_single_culling(cow):
        existing_culling_record = cow.culling_record.all()
        if existing_culling_record:
            raise ValidationError("A cow can only be tied to one culling record.")


class QuarantineValidator:
    @staticmethod
    def validate_reason(reason, cow):
        if reason == QuarantineReasonChoices.BOUGHT_COW and not cow.is_bought:
            raise ValidationError(
                "Invalid reason, this cow was not bought therefore, that can not be the reason"
            )

    @staticmethod
    def validate_date(start_date, end_date, pk):
        if end_date and start_date > end_date:
            raise ValidationError(
                "Invalid date entry, End dates must be later than start date"
            )

        if pk is None and end_date:
            raise ValidationError(
                "Invalid entry, new quarantine records must not have end dates "
            )


class CowPenValidator:
    @staticmethod
    def validate_cow_pen_type(barn, pen_type, pk):
        from dairy.models import CowPen

        if pen_type == CowPenTypeChoices.FIXED and pk:
            old_barn = CowPen.objects.get(pk=pk).barn
            if barn != old_barn:
                raise ValidationError("A pen of type 'Fixed' cannot change its barn.")

    @staticmethod
    def validate_cow_pen_capacity(barn, pen_capacity, pk):
        from dairy.models import CowPen

        if pk:
            barn_pens = list(CowPen.objects.filter(barn=barn).exclude(id=pk))
            occupied_capacity = 0
            for pen in barn_pens:
                occupied_capacity += pen.capacity
            if (barn.capacity - occupied_capacity) - pen_capacity < 0:
                raise ValidationError(
                    f"This barn has unoccupied capacity of {barn.capacity - occupied_capacity}, you specified {pen_capacity}"
                    f", which is above the limit by {pen_capacity - (barn.capacity - occupied_capacity)}"
                )

        else:
            barn_pens = list(CowPen.objects.filter(barn=barn))
            occupied_capacity = 0
            for pen in barn_pens:
                occupied_capacity += pen.capacity
            if (barn.capacity - occupied_capacity) - pen_capacity < 0:
                raise ValidationError(
                    f"This barn has unoccupied capacity of {barn.capacity - occupied_capacity}, you specified {pen_capacity}"
                    f", which is above the limit by {pen_capacity - (barn.capacity - occupied_capacity)}"
                )

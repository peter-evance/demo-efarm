from django.db import models
from .choices import *
from dairy.utils import *


class CowManager(models.Manager):
    """
    Custom manager for the Cow model.

    Methods:
    - `get_tag_number(cow)`: Generates and returns the tag number for a cow.
    - `calculate_age(cow)`: Calculates and returns the age of a cow in days.
    - `calculate_age_in_farm(cow)`: Calculates and returns the age of a cow in days since introduction to the farm.
    - `get_available_cows()`: Returns a queryset of available (alive) cows.
    - `get_pregnant_cows()`: Returns a queryset of pregnant cows.
    - `get_male_cows()`: Returns a queryset of available (alive) male cows.
    - `get_female_cows()`: Returns a queryset of available (alive) female cows.
    - `get_sold_cows()`: Returns a queryset of sold cows.
    - `get_dead_cows()`: Returns a queryset of dead cows.
    - `get_calf_records(cow)`: Returns a list of calf records associated with the cow.

    """

    @staticmethod
    def get_tag_number(cow):
        """
        Generates and returns the tag number for a cow.

        Args:
        - `cow`: The cow object.

        Returns:
        - The tag number of the cow in the format "XX-YYYY-ID".

        """
        year_of_birth = cow.date_of_birth.strftime('%Y')
        first_letters_of_breed = cow.breed.name[:2].upper()
        counter = cow.id
        return f"{first_letters_of_breed}-{year_of_birth}-{counter}"

    @staticmethod
    def calculate_age(cow):
        """
        Calculates and returns the age of a cow in days.

        Args:
        - `cow`: The cow object.

        Returns:
        - The age of the cow in days.

        """
        age_in_days = (todays_date - cow.date_of_birth).days
        return age_in_days

    @staticmethod
    def calculate_age_in_farm(cow):
        """
        Calculates and returns the age of a cow in days since introduction to the farm.

        Args:
        - `cow`: The cow object.

        Returns:
        - The age of the cow in days since introduction to the farm.

        """
        age_in_days = (todays_date - cow.date_introduced_in_farm).days
        return age_in_days

    def get_calf_records(self, cow):
        """
        Returns a list of calf records associated with the cow.

        Args:
        - `cow`: The cow object.

        Returns:
        - A list of calf records associated with the cow.

        """
        if cow.gender == SexChoices.FEMALE:
            calf_records = self.filter(dam=cow)
        else:
            calf_records = self.filter(sire=cow)
        return list(calf_records)

    @staticmethod
    def calculate_parity(cow):
        """
        Calculates the parity of a female cow based on its calf records.

        Args:
        - `cow`: The cow object.

        Returns:
        - The parity of the cow.
        """
        if cow.gender == SexChoices.FEMALE:
            calf_records = cow.calf_records
            return len(calf_records)
        else:
            return 0

    def get_available_cows(self):
        """
        Returns a queryset of available (alive) cows.

        Returns:
        - A queryset of available (alive) cows.

        """
        return self.filter(availability_status=CowAvailabilityChoices.ALIVE)

    def get_pregnant_cows(self):
        """
        Returns a queryset of pregnant cows.

        Returns:
        - A queryset of pregnant cows.

        """
        return self.filter(pregnancy_status=CowPregnancyChoices.PREGNANT)

    def get_male_cows(self):
        """
        Returns a queryset of available (alive) male cows.

        Returns:
        - A queryset of available (alive) male cows.

        """
        return self.filter(availability_status=CowAvailabilityChoices.ALIVE, gender=SexChoices.MALE)

    def get_female_cows(self):
        """
        Returns a queryset of available (alive) female cows.

        Returns:
        - A queryset of available (alive) female cows.

        """
        return self.filter(availability_status=CowAvailabilityChoices.ALIVE, gender=SexChoices.FEMALE)

    def get_sold_cows(self):
        """
        Returns a queryset of sold cows.

        Returns:
        - A queryset of sold cows.

        """
        return self.filter(availability_status=CowAvailabilityChoices.SOLD)

    def get_dead_cows(self):
        """
        Returns a queryset of dead cows.

        Returns:
        - A queryset of dead cows.

        """
        return self.filter(availability_status=CowAvailabilityChoices.DEAD)

from datetime import datetime, date

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

from .choices import *


class FlockSource(models.Model):
    """
    The model represents the source of a flock in a poultry farm.

    Fields:
    - `source`: A character field representing the source of the flock.
                It is limited to a maximum length of 13 characters.
                The available choices are defined in the `FlockSourceChoices` enum.

    """

    source = models.CharField(max_length=13, choices=FlockSourceChoices.choices)


class HousingStructure(models.Model):
    """
    The model represents a housing structure for poultry in a farm.

    Fields:
    - `type`: A character field representing the type of the housing structure.
              It is limited to a maximum length of 22 characters.
              The available choices are defined in the `HousingStructureTypeChoices` enum.
    - `category`: A character field representing the category of the housing structure.
                  It is limited to a maximum length of 21 characters.
                  The available choices are defined in the `HousingStructureCategoryChoices` enum.

    Methods:
    - `clean()`: This method performs validation on the model instance.
                 It ensures that specific combinations of `type` and `category` are valid.
                 For example, if the category is "Brooder Chick House", only "Deep Litter House" and "Closed Shed"
                 structure types are allowed, and an error is raised if an invalid type is chosen.
                 Similarly, if the category is "Breeders House", the "Pasture Housing" structure type is not allowed,
                 and a validation error is raised.
    - `save(*args, **kwargs)`: This overridden method calls `clean()` to perform validation before saving the instance.

    """

    type = models.CharField(max_length=22, choices=HousingStructureTypeChoices.choices)
    category = models.CharField(max_length=21, choices=HousingStructureCategoryChoices.choices)

    def clean(self):
        """
        Performs validation on the model instance.

        Raises:
        - `ValidationError`: If the combination of `type` and `category` is invalid.

        """
        if self.category == HousingStructureCategoryChoices.Brooder_Chick_House:
            if self.type not in [
                HousingStructureTypeChoices.Deep_Litter_House,
                HousingStructureTypeChoices.Closed_Shed
            ]:
                raise ValidationError(
                    "Brood and chick houses are limited to Deep Litter House or Closed Shed structure types."
                )

        if self.category == HousingStructureCategoryChoices.Breeders_House \
                and self.type == HousingStructureTypeChoices.Pasture_Housing:
            raise ValidationError("Breeder houses are not allowed to have the Pasture Housing structure type.")

    def save(self, *args, **kwargs):
        """
        Overrides the default save method to perform validation before saving.

        """
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        """
        Returns a string representation of the housing structure.

        """
        return f'Housing Structure #{self.id}'


class Flock(models.Model):
    """
    The model represents a flock in a poultry farm.

    Fields:
    - `source`: A foreign key to the `FlockSource` model, representing the source of the flock.
    - `date_of_hatching`: A date field representing the date when the flock hatched.
                          It is validated to ensure it falls within a specific range.
    - `chicken_type`: A character field representing the type of chickens in the flock.
                      It is limited to a maximum length of 15 characters.
                      The available choices are defined in the `ChickenTypeChoices` enum.
    - `initial_number_of_birds`: A positive integer field representing the initial number of birds in the flock.
                                 It is validated to ensure it is at least 2.
    - `current_rearing_method`: A character field representing the current rearing method of the flock.
                                It is limited to a maximum length of 50 characters.
                                The available choices are defined in the `RearingMethodChoices` enum.
    - `current_housing_structure`: A foreign key to the `HousingStructure` model, representing the current housing
                                  structure for the flock.
    - `date_established`: A date field that automatically records the date when the flock was established.

    Properties:
    - `name`: Returns a string representing the name of the flock, including its ID and the date of establishment.
    - `age_in_weeks`: Calculates and returns the age of the flock in weeks.
    - `age_in_months`: Calculates and returns the age of the flock in months.
    - `age_in_weeks_in_farm`: Calculates and returns the age of the flock in weeks since establishment.
    - `age_in_months_in_farm`: Calculates and returns the age of the flock in months since establishment.

    Methods:
    - `chicken_type_update_validator()`: Validates the chicken type of the flock during updates.
    - `flock_housing_validator()`: Validates the housing structure assigned to the flock based on its chicken type and age.

    """

    source = models.ForeignKey(FlockSource, on_delete=models.CASCADE)
    date_of_hatching = models.DateField(
        validators=[MinValueValidator(date.today() - timezone.timedelta(weeks=8)),
                    MaxValueValidator(date.today())]
    )
    chicken_type = models.CharField(max_length=15, choices=ChickenTypeChoices.choices)
    initial_number_of_birds = models.PositiveIntegerField(validators=[MinValueValidator(2)])
    current_rearing_method = models.CharField(max_length=50, choices=RearingMethodChoices.choices)
    current_housing_structure = models.ForeignKey(HousingStructure, on_delete=models.CASCADE)
    date_established = models.DateField(auto_now_add=True)

    @property
    def name(self):
        """
        Returns the name of the flock, including its ID and the date of establishment.

        """
        return f'Flock {self.id} - {self.date_established.strftime("%B %d, %Y")}'

    @property
    def age_in_weeks(self):
        """
        Calculates and returns the age of the flock in weeks.

        """
        today = timezone.now().date()
        age_in_days = (today - self.date_of_hatching).days
        age_in_weeks = age_in_days // 7
        return age_in_weeks

    @property
    def age_in_months(self):
        """
        Calculates and returns the age of the flock in months.

        """
        today = timezone.now().date()
        age_in_days = (today - self.date_of_hatching).days
        age_in_months = age_in_days // 30
        return age_in_months

    @property
    def age_in_weeks_in_farm(self):
        """
        Calculates and returns the age of the flock in weeks since establishment.

        """
        today = timezone.now().date()
        age_in_days = (today - self.date_established).days
        age_in_weeks_in_farm = age_in_days // 7
        return age_in_weeks_in_farm

    @property
    def age_in_months_in_farm(self):
        """
        Calculates and returns the age of the flock in months since establishment.

        """
        today = timezone.now().date()
        age_in_days = (today - self.date_established).days
        age_in_months_in_farm = age_in_days // 30
        return age_in_months_in_farm

    def __str__(self):
        """
        Returns a string representation of the flock.

        """
        return self.name

    def chicken_type_update_validator(self):
        """
        Validates the chicken type of the flock during updates.
        Raises a validation error if the chicken type is being changed.

        """
        if self.pk:
            old_instance: Flock = Flock.objects.get(pk=self.pk)
            if old_instance.chicken_type != self.chicken_type:
                raise ValidationError("Cannot update the chicken type")

    def flock_housing_validator(self):
        """
        Validates the housing structure assigned to the flock based on its chicken type and age.

        Raises:
        - `ValidationError`: If the assigned housing structure is invalid based on the flock's chicken type and age.

        """
        if self.chicken_type == ChickenTypeChoices.Broiler and \
                self.current_housing_structure.category != HousingStructureCategoryChoices.Broilers_House:
            raise ValidationError("Broiler chickens can only be assigned to the broiler house category.")

        if self.chicken_type == ChickenTypeChoices.Layers:
            if 0 <= self.age_in_weeks <= 8:
                if self.current_housing_structure.category != HousingStructureCategoryChoices.Brooder_Chick_House:
                    raise ValidationError("Layers between 0-8 weeks can only be assigned to the Brooder Chick House.")
            elif 8 < self.age_in_weeks <= 18:
                if self.current_housing_structure.category != HousingStructureCategoryChoices.Growers_House:
                    raise ValidationError("Layers between 8-18 weeks can only be assigned to the Growers House.")
            elif 18 < self.age_in_weeks <= 84:
                if self.current_housing_structure.category != HousingStructureCategoryChoices.Layers_House:
                    raise ValidationError("Layers between 18-84 weeks can only be assigned to the Layers House.")
            else:
                raise ValidationError("Invalid age range for layers.")

        if self.chicken_type == ChickenTypeChoices.Multi_Purpose and self.age_in_weeks <= 4:
            if self.current_housing_structure.category != HousingStructureCategoryChoices.Brooder_Chick_House:
                raise ValidationError(
                    "Multipurpose chickens of 8 weeks and below can only be assigned to the Brooder Chick House."
                )

    def save(self, *args, **kwargs):
        """
        Overrides the default save method to perform custom validations before saving the instance.
        Creates a `FlockHistory` object to track the flock's rearing method and housing structure changes.

        """
        self.chicken_type_update_validator()
        self.flock_housing_validator()
        super().save(*args, **kwargs)

        FlockHistory.objects.create(
            flock=self,
            rearing_method=self.current_rearing_method,
            current_housing_structure=self.current_housing_structure
        )


class FlockHistory(models.Model):
    """
    The model represents the history of a flock in terms of its rearing method and housing structure changes.

    Fields:
    - `flock`: A foreign key to the `Flock` model, representing the flock associated with the history entry.
    - `rearing_method`: A character field representing the rearing method of the flock at a specific point in time.
                        It is limited to a maximum length of 50 characters.
                        The available choices are defined in the `RearingMethodChoices`.
    - `current_housing_structure`: A foreign key to the `HousingStructure` model, representing the housing structure
                                  of the flock at a specific point in time.
    - `date_changed`: A datetime field that automatically records the date and time when the history entry was created.

    """

    flock = models.ForeignKey(Flock, on_delete=models.CASCADE)
    rearing_method = models.CharField(max_length=50, choices=RearingMethodChoices.choices)
    current_housing_structure = models.ForeignKey(HousingStructure, on_delete=models.CASCADE)
    date_changed = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Returns a string representation of the flock history entry.

        """
        return f'History for {self.flock}'

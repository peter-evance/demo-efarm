from datetime import date

from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

from poultry.utils import todays_date
from poultry.validators import *


class FlockSource(models.Model):
    """
    The model represents the source of a flock in a poultry farm.

    Fields:
    - `source`: A character field representing the source of the flock.
                It is limited to a maximum length of 13 characters.
                The available choices are defined in the `FlockSourceChoices` enum.

    """

    name = models.CharField(max_length=13, choices=FlockSourceChoices.choices)

    def clean(self):
        FlockSourceValidator.validate_source(self.name)

    def save(self, *args, **kwargs):
        """
        Overrides the save method to ensure validation before saving.
        """
        self.clean()
        super().save(*args, **kwargs)


class FlockBreed(models.Model):
    """
    Model representing a breed.

    Fields:
    - `name`: A CharField representing the name of the breed.

    """

    name = models.CharField(max_length=20, choices=FlockBreedTypeChoices.choices)

    def __str__(self):
        return self.name

    def clean(self):
        FlockBreedValidator.validate_breed_name(self.name)

    def save(self, *args, **kwargs):
        """
        Overrides the save method to ensure validation before saving.
        """
        self.clean()
        super().save(*args, **kwargs)


class HousingStructure(models.Model):
    """
    The model represents a housing structure for poultry in a farm.

    Fields:
    - `house_type`: A character field representing the type of the housing structure.
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

    house_type = models.CharField(
        max_length=22, choices=HousingStructureTypeChoices.choices
    )
    category = models.CharField(
        max_length=21, choices=HousingStructureCategoryChoices.choices
    )

    def __str__(self):
        """
        Returns a string representation of the housing structure.

        """
        return f"Housing Structure #{self.id}"

    def clean(self):
        """
        Performs validation on the model instance.

        Raises:
        - `ValidationError`: If the combination of `house_type` and `category` is invalid.

        """
        HousingStructureValidator.validate_category(self.category, self.house_type)

    def save(self, *args, **kwargs):
        """
        Overrides the default save method to perform validation before saving.

        """
        self.clean()
        super().save(*args, **kwargs)


class Flock(models.Model):
    """
    The model represents a flock in a poultry farm.

    Fields:
    - `source`: A foreign key to the `FlockSource` model, representing the source of the flock.
    - `breed`: A foreign key to the `FlockBreed` model, representing the breed of the flock.
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
    - `is_present`: A boolean field indicating if the flock is currently present. It is set to True by default.

    Properties:
    - `name`: Returns a string representing the name of the flock, including its ID and the date of establishment.
    - `age_in_weeks`: Calculates and returns the age of the flock in weeks.
    - `age_in_months`: Calculates and returns the age of the flock in months.
    - `age_in_weeks_in_farm`: Calculates and returns the age of the flock in weeks since establishment.
    - `age_in_months_in_farm`: Calculates and returns the age of the flock in months since establishment.

    """

    source = models.ForeignKey(FlockSource, on_delete=models.PROTECT, related_name="flocks")
    breed = models.ForeignKey(FlockBreed, on_delete=models.PROTECT, related_name="flocks")
    date_of_hatching = models.DateField()
    chicken_type = models.CharField(max_length=15, choices=ChickenTypeChoices.choices)
    initial_number_of_birds = models.PositiveIntegerField(validators=[MinValueValidator(2)])
    current_rearing_method = models.CharField(max_length=50, choices=RearingMethodChoices.choices)
    current_housing_structure = models.ForeignKey(HousingStructure, on_delete=models.PROTECT, related_name="flocks")
    date_established = models.DateField(auto_now_add=True)
    is_present = models.BooleanField(default=True, editable=False)

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
        age_in_days = (todays_date - self.date_of_hatching).days
        age_in_weeks = age_in_days // 7
        return age_in_weeks

    @property
    def age_in_months(self):
        """
        Calculates and returns the age of the flock in months.

        """
        age_in_days = (todays_date - self.date_of_hatching).days
        age_in_months = age_in_days // 30
        return age_in_months

    @property
    def age_in_weeks_in_farm(self):
        """
        Calculates and returns the age of the flock in weeks since establishment.

        """
        age_in_days = (todays_date - self.date_established).days
        age_in_weeks_in_farm = age_in_days // 7
        return age_in_weeks_in_farm

    @property
    def age_in_months_in_farm(self):
        """
        Calculates and returns the age of the flock in months since establishment.

        """
        age_in_days = (todays_date - self.date_established).days
        age_in_months_in_farm = age_in_days // 30
        return age_in_months_in_farm

    def __str__(self):
        """
        Returns a string representation of the flock.

        """
        return self.name

    def clean(self):
        FlockValidator.validate_chicken_type_update(self)
        FlockValidator.validate_flock_date_of_hatching(self.date_of_hatching)
        FlockValidator.validate_flock_housing(self.chicken_type, self.current_housing_structure, self.age_in_weeks)

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class FlockHistory(models.Model):
    flock = models.ForeignKey(Flock, on_delete=models.CASCADE)
    rearing_method = models.CharField(
        max_length=50, choices=RearingMethodChoices.choices
    )
    current_housing_structure = models.ForeignKey(
        HousingStructure, on_delete=models.CASCADE
    )
    date_changed = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"History for {self.flock}"


class FlockMovement(models.Model):
    flock = models.ForeignKey(Flock, on_delete=models.CASCADE)
    from_structure = models.ForeignKey(HousingStructure, on_delete=models.CASCADE, related_name='outgoing_movements')
    to_structure = models.ForeignKey(HousingStructure, on_delete=models.CASCADE, related_name='incoming_movements')
    movement_date = models.DateField(auto_now_add=True)

    def clean(self):
        FlockMovementValidator.validate_flock_movement(self.flock, self.to_structure, self.from_structure)

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Movement of Flock {self.flock.id} ({self.from_structure} -> {self.to_structure})'


class FlockInspectionRecord(models.Model):
    flock = models.ForeignKey(Flock, on_delete=models.CASCADE)
    date_of_inspection = models.DateTimeField(auto_now_add=True)
    number_of_dead_birds = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.flock} Inspection Report on: {self.date_of_inspection}"

    def save(self, *args, **kwargs):
        FlockInspectionRecordValidator.validate_flock_availability(self.flock)
        FlockInspectionRecordValidator.validate_number_of_dead_birds(self)
        super().save(*args, **kwargs)
        FlockInspectionRecordValidator.validate_daily_number_of_inspection_records(self.date_of_inspection)
        FlockInspectionRecordValidator.validate_inspection_record_time_separation(self.flock, self)


class FlockBreedInformation(models.Model):
    """
    Model representing the information about a flock breed.

    The FlockBreedInformation model contains details such as the breed,
    chicken type, average mature weight, average egg production, and maturity age.

    Fields:
    - breed: ForeignKey to the FlockBreed model, specifying the breed of the flock.
    - chicken_type: CharField specifying the type of chicken, chosen from a set of choices.
    - date_added: DateField automatically set to the date of creation.
    - average_mature_weight_in_kgs: DecimalField specifying the average mature weight of the flock in kilograms,
      with no specific minimum value.
    - average_egg_production: PositiveIntegerField specifying the average egg production of the flock,
      with the option to be null.
    - maturity_age_in_weeks: PositiveIntegerField specifying the maturity age of the flock in weeks,
      with a minimum value of 6."""

    breed = models.ForeignKey(FlockBreed, on_delete=models.CASCADE)
    chicken_type = models.CharField(max_length=15, choices=ChickenTypeChoices.choices)
    date_added = models.DateField(auto_now_add=True)
    average_mature_weight_in_kgs = models.DecimalField(max_digits=3, decimal_places=2)
    average_egg_production = models.PositiveIntegerField(null=True)
    maturity_age_in_weeks = models.PositiveIntegerField(validators=[MinValueValidator(8), MaxValueValidator(24)])

    def clean(self):
        FlockBreedInformationValidator.validate_fields(self.chicken_type, self.average_egg_production,
                                                       self.average_mature_weight_in_kgs, self.maturity_age_in_weeks)

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class EggCollection(models.Model):
    """
    Model representing the collection of eggs from a flock.

    Fields:
    - `flock`: A foreign key relationship to the `Flock` model, representing the flock from which the eggs are collected.
    - `date`: A DateField automatically set to the current date when the egg collection is added.
    - `time`: A TimeField automatically set to the current time when the egg collection is added.
    - `collected_eggs`: A PositiveIntegerField representing the number of eggs collected.
    - `broken_eggs`: A PositiveIntegerField representing the number of broken eggs.

    Methods:
    - `picking_time`: Returns a string indicating whether the egg collection was done in the morning or afternoon.
    - `validator()`: Validates the data before saving, ensuring the broken egg count is not greater than the collected egg count,
      the collected egg count does not exceed the count of living birds in the flock for the day, limits data entry to thrice per day,
      restricts the flock type to layers or multipurpose, the flock is marked as present, and the flock is 14 weeks or older.

    """

    class Meta:
        verbose_name_plural = "Egg Collections"

    flock = models.ForeignKey(Flock, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    collected_eggs = models.PositiveIntegerField(default=0)
    broken_eggs = models.PositiveIntegerField(default=0)

    @property
    def picking_time(self):
        """
        Returns a string indicating whether the egg collection was done in the morning or afternoon.

        Returns:
        - str: The picking time, either 'Morning' or 'Afternoon'.

        """
        hour = self.time.hour
        if hour < 12:
            return "Morning"
        else:
            return "Afternoon"

    def validator(
        self,
    ):  # This is just a custom validator, it is not inherited from django
        """
        Validates the data before saving the egg collection.

        Raises:
        - ValidationError: If the broken egg count is greater than the collected egg count,
          the collected egg count exceeds the count of living birds in the flock for the day,
          the data entry for the flock exceeds thrice per day, the flock type is not layers or multipurpose,
          the flock is not marked as present, or the flock is younger than 14 weeks.

        """
        if not self.flock.is_present:
            raise ValidationError(
                f"Egg collection is only allowed for flocks marked as present. This flock was "
                f"marked not present on {self.flock.inventory.last_update.astimezone(timezone.get_current_timezone()).strftime('%A %B %d, %Y')}."
            )

        count: int = EggCollection.objects.filter(
            flock=self.flock, date=self.date
        ).count()
        if count > 3:
            tomorrow = timezone.now().astimezone(
                timezone.get_current_timezone()
            ).date() + timezone.timedelta(days=1)
            raise ValidationError(
                f"Data entry for this flock is limited to thrice per day. "
                f"Please try again on {tomorrow.strftime('%A %B %d, %Y')}."
            )

        if self.broken_eggs > self.collected_eggs:
            raise ValidationError(
                f"Broken eggs count ({self.broken_eggs}) cannot be greater than the collected eggs "
                f"count ({self.collected_eggs})"
            )

        live_bird_count: int = self.flock.inventory.number_of_alive_birds
        total_collected_eggs: int = (
            EggCollection.objects.filter(flock=self.flock, date=self.date)
            .exclude(pk=self.pk)
            .aggregate(total=Sum("collected_eggs"))
            .get("total")
            or 0
        )

        if total_collected_eggs + self.collected_eggs > live_bird_count:
            if live_bird_count - total_collected_eggs <= 0:
                raise ValidationError(
                    f"Collected egg count for the day cannot exceed the count of living birds in the "
                    f"flock, This flock has {live_bird_count} birds. The "
                    f"total collected eggs today is {total_collected_eggs}."
                )

            raise ValidationError(
                f"Collected egg count for the day cannot exceed the count of living birds in the "
                f"flock, This flock has {live_bird_count} birds, and the collected "
                f"eggs today must be {live_bird_count - total_collected_eggs} or lower. The "
                f"total collected eggs today is {total_collected_eggs}."
            )

        if self.flock.chicken_type not in [
            ChickenTypeChoices.LAYERS,
            ChickenTypeChoices.MULTI_PURPOSE,
        ]:
            raise ValidationError(
                f"Egg collection is restricted to layers or multipurpose flocks, "
                f"You selected {self.flock.chicken_type.lower()}."
            )

        if self.flock.age_in_weeks < 14:
            raise ValidationError(
                f"Egg collection is only allowed for flocks of age 14 weeks or older, "
                f"This flock is currently {self.flock.age_in_weeks} weeks old."
            )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.validator()

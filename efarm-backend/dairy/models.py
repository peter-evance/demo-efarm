from datetime import date, datetime, timedelta

from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField

from dairy.managers import *
from dairy.validators import *


class CowBreed(models.Model):
    """
    Represents a breed of cow.

    Attributes:
    - `name` (str): The name of the cow breed.
    """
    name = models.CharField(max_length=20, choices=CowBreedChoices.choices)

    def __str__(self):
        """
        Returns a string representation of the cow breed.
        """
        return str(self.name)

    def clean(self):
        """
        Performs validation checks before saving the cow breed.

        Raises:
        - `ValidationError`: If breed validation fails.
        """
        CowBreedValidator.validate_update(self.pk)
        CowBreedValidator.validate_name(self.name)

    def save(self, *args, **kwargs):
        """
        Overrides the save method to ensure validation before saving.
        """
        self.clean()
        super().save(*args, **kwargs)


class Cow(models.Model):
    """
    Represents an individual cow in the dairy farm.

    Attributes:
    - `name` (str): The name of the cow.
    - `breed` (CowBreed): The breed of the cow.
    - `date_of_birth` (date): The birthdate of the cow.
    - `gender` (str): The gender of the cow.
    - `availability_status` (str): The availability status of the cow.
    - `sire` (Cow or None): The sire (father) of the cow.
    - `dam` (Cow or None): The dam (mother) of the cow.
    - `current_pregnancy_status` (str): The current pregnancy status of the cow.
    - `category` (str): The category of the cow.
    - `current_production_status` (str): The current production status of the cow.
    - `date_introduced_in_farm` (date): The date the cow was introduced to the farm.
    - `is_bought` (bool): Indicates whether the cow was bought or not.
    - `date_of_death` (date or None): The date of death of the cow, if applicable.
    """
    name = models.CharField(max_length=35)
    breed = models.ForeignKey(CowBreed, on_delete=models.PROTECT, db_index=True, related_name='cows')
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=6, choices=SexChoices.choices)
    availability_status = models.CharField(choices=CowAvailabilityChoices.choices, default=CowAvailabilityChoices.ALIVE,
                                           max_length=5)
    sire = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, related_name='offspring')
    dam = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, related_name='calves')
    current_pregnancy_status = models.CharField(choices=CowPregnancyChoices.choices,
                                                default=CowPregnancyChoices.UNAVAILABLE, max_length=12)
    category = models.CharField(choices=CowCategoryChoices.choices, default=CowCategoryChoices.CALF, max_length=11)
    current_production_status = models.CharField(choices=CowProductionStatusChoices.choices, max_length=22,
                                                 default=CowProductionStatusChoices.CALF)
    date_introduced_in_farm = models.DateField(auto_now_add=True)
    is_bought = models.BooleanField(default=False)
    date_of_death = models.DateField(null=True)

    objects = models.Manager()
    manager = CowManager()

    @property
    def tag_number(self):
        """
        Returns the tag number of the cow.
        """
        return Cow.manager.get_tag_number(self)

    @property
    def parity(self):
        """
        Calculates and returns the parity of the cow.
        """
        return Cow.manager.calculate_parity(self)

    @property
    def age(self):
        """
        Calculates and returns the age of the cow in days.
        """
        return Cow.manager.calculate_age(self)

    @property
    def age_in_farm(self):
        """
        Calculates and returns the age of the cow in days since introduction to the farm.
        """
        return Cow.manager.calculate_age_in_farm(self)

    @property
    def calf_records(self):
        return Cow.manager.get_calf_records(self)

    def clean(self):
        """
        Performs validation checks before saving the cow.

        Raises:
        - `ValidationError`: If cow validation fails.
        """
        CowValidator.validate_cow_age(self.age, self.date_of_birth)
        CowValidator.validate_uniqueness(self.name)
        CowValidator.validate_date_of_death(self.availability_status, self.date_of_death)
        CowValidator.validate_gender_update(self.pk, self.gender)
        CowValidator.validate_sire_dam_relationship(self.sire, self.dam)

    def __str__(self):
        """
        Returns a string representation of the cow.
        """
        return self.tag_number

    def save(self, *args, **kwargs):
        """
        Overrides the save method to ensure validation before saving.
        """
        self.clean()
        super().save(*args, **kwargs)
        CowValidator.validate_introduction_date(self.date_introduced_in_farm)
        CowValidator.validate_age_category(self.age, self.category, self.gender, self.calf_records, self.is_bought,
                                           self)
        CowValidator.validate_pregnancy_status(self, self.age, self.current_pregnancy_status, self.availability_status,
                                               self.gender)
        CowValidator.validate_production_status(self.current_production_status, self.gender, self.category, self.age,
                                                self.calf_records, self.is_bought, self)


class Inseminator(models.Model):
    """
    Represents an inseminator responsible for cow insemination.

    Attributes:
    - `first_name` (str): The first name of the inseminator.
    - `last_name` (str): The last name of the inseminator.
    - `phone_number` (PhoneNumber): The phone number of the inseminator.
    - `sex` (str): The sex of the inseminator.
    - `company` (str): The company associated with the inseminator (optional).
    - `license_number` (str): The unique license number of the inseminator.
    """

    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    phone_number = PhoneNumberField(max_length=13, unique=True)
    sex = models.CharField(choices=SexChoices.choices, max_length=6)
    company = models.CharField(max_length=50, blank=True, null=True)
    license_number = models.CharField(max_length=25, unique=True)

    def __str__(self):
        """
        Returns a string representation of the inseminator.
        """
        return f"{self.first_name} {self.last_name}"


class Heat(models.Model):
    """
    Represents a record of heat observation in a cow.

    Attributes:
    - `observation_time` (datetime): The time of heat observation.
    - `cow` (Cow): The cow associated with the heat observation.
    """

    observation_time = models.DateTimeField()
    cow = models.ForeignKey(Cow, on_delete=models.CASCADE, related_name="heat_records")

    def __str__(self):
        """
        Returns a string representation of the heat record.
        """
        return f"Heat record for cow {self.cow.tag_number} on {self.observation_time}"

    def clean(self):
        """
        Performs validation checks before saving the heat record.

        Raises:
        - `ValidationError`: If heat record validation fails.
        """
        HeatValidator.validate_observation_time(self.observation_time)
        HeatValidator.validate_pregnancy(self.cow)
        HeatValidator.validate_production_status(self.cow)
        HeatValidator.validate_dead(self.cow)
        HeatValidator.validate_gender(self.cow)
        HeatValidator.validate_within_60_days_after_calving(self.cow, self.observation_time)
        HeatValidator.validate_within_21_days_of_previous_heat(self.cow, self.observation_time)
        HeatValidator.validate_min_age(self.cow)
        HeatValidator.validate_already_in_heat(self.cow)

    def save(self, *args, **kwargs):
        """
        Overrides the save method to ensure validation before saving.
        """
        self.clean()
        super().save(*args, **kwargs)


class Pregnancy(models.Model):
    """
    Represents a pregnancy record for a cow.

    Attributes:
    - `cow` (Cow): The cow associated with the pregnancy.
    - `start_date` (date): The start date of the pregnancy.
    - `date_of_calving` (date or None): The date of calving if the pregnancy resulted in a calving.
    - `pregnancy_status` (str): The status of the pregnancy.
    - `pregnancy_notes` (str): Additional notes related to the pregnancy.
    - `calving_notes` (str): Additional notes related to the calving.
    - `pregnancy_scan_date` (date or None): The date of pregnancy scan.
    - `pregnancy_failed_date` (date or None): The date when the pregnancy failed, if applicable.
    - `pregnancy_outcome` (str or None): The outcome of the pregnancy, if known.

    Note: The terms "calving" and "scan" are related to cattle reproduction.
"""
    cow = models.ForeignKey(Cow, on_delete=models.PROTECT, related_name='pregnancies')
    start_date = models.DateField()
    date_of_calving = models.DateField(null=True, blank=True)
    pregnancy_status = models.CharField(max_length=11, choices=PregnancyStatusChoices.choices,
                                        default=PregnancyStatusChoices.UNCONFIRMED)
    pregnancy_notes = models.TextField(blank=True)
    calving_notes = models.TextField(blank=True)
    pregnancy_scan_date = models.DateField(null=True, blank=True)
    pregnancy_failed_date = models.DateField(null=True, blank=True)
    pregnancy_outcome = models.CharField(max_length=11, choices=PregnancyOutcomeChoices.choices, blank=True, null=True)

    objects = models.Manager()
    manager = PregnancyManager()

    @property
    def pregnancy_duration(self):
        """
        Returns: Number of days since inception of pregnancy.
        """
        return PregnancyManager.pregnancy_duration(self)

    @property
    def latest_lactation_stage(self):
        """
        Returns: Most recent lactation stage for the cow
        """
        return PregnancyManager.latest_lactation_stage(self)

    def clean(self):
        """
        Performs validation checks before saving the pregnancy record.

        Raises:
        - `ValidationError`: If pregnancy record validation fails.
        """
        PregnancyValidator.validate_age(self.cow.age, self.start_date, self.cow)
        PregnancyValidator.validate_cow_current_pregnancy_status(self.cow)
        PregnancyValidator.validate_cow_availability_status(self.cow)
        PregnancyValidator.validate_dates(self.start_date, self.pregnancy_status, self.date_of_calving,
                                          self.pregnancy_scan_date, self.pregnancy_failed_date)
        PregnancyValidator.validate_pregnancy_status(self.pregnancy_status, self.start_date, self.pregnancy_failed_date)
        PregnancyValidator.validate_outcome(self.pregnancy_outcome, self.pregnancy_status, self.date_of_calving)

    def save(self, *args, **kwargs):
        """
        Overrides the save method to ensure validation before saving.
        """
        self.clean()
        super().save(*args, **kwargs)


class Insemination(models.Model):
    """
   Represents a record of cow insemination.

   Attributes:
   - `date_of_insemination` (datetime): The date and time of the insemination.
   - `cow` (Cow): The cow that underwent the insemination.
   - `pregnancy` (Pregnancy or None): The associated pregnancy record, if insemination is successful.
   - `success` (bool): Indicates whether the insemination was successful or not.
   - `notes` (str): Additional notes related to the insemination.
   - `inseminator` (Inseminator): The inseminator responsible for the procedure.
   - `semen` (Semen or None): The type of semen used for the insemination.

   Note: The term "insemination" refers to the process of introducing semen into the reproductive tract of a female animal.
    """

    class Meta:
        ordering = ['-date_of_insemination']

    date_of_insemination = models.DateTimeField(auto_now_add=True)
    cow = models.ForeignKey(Cow, on_delete=models.PROTECT, related_name='inseminations')
    pregnancy = models.OneToOneField(Pregnancy, on_delete=models.PROTECT, editable=False, blank=True, null=True)
    success = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    inseminator = models.ForeignKey(Inseminator, on_delete=models.PROTECT, related_name='inseminations_done')
    semen = models.ForeignKey('Semen', on_delete=models.PROTECT, blank=True, null=True)

    objects = models.Manager()
    manager = InseminationManager()

    @property
    def days_since_insemination(self):
        """
        Returns: Days since the cow was last inseminated
        """
        return InseminationManager.days_since_insemination(self)

    def __str__(self):
        return f"Insemination record for cow {self.cow.tag_number} on {self.date_of_insemination}"

    def clean(self):
        """
        Performs validation checks before saving the insemination record.

        Raises:
        - `ValidationError`: If insemination record validation fails.
        """
        InseminationValidator.validate_within_21_days_of_previous_insemination(self.pk, self.cow)

    def save(self, *args, **kwargs):
        """
        Overrides the save method to ensure validation before saving.
        """
        self.clean()
        super().save(*args, **kwargs)
        InseminationValidator.validate_already_in_heat(self.cow, self.date_of_insemination)


class Lactation(models.Model):
    """

    A model representing a lactation period of a cow.

    ### Fields

    - `start_date` - a `DateField` representing the start date of the lactation period
    - `end_date` - a `DateField` representing the end date of the lactation period
    - `cow` - a foreign key to the `Cow` model representing the cow associated with this lactation period
    - `lactation_number` - a `PositiveSmallIntegerField` representing the lactation number for this period
    - `pregnancy` - a foreign key to the `Pregnancy` model representing the pregnancy associated with this lactation period

    ### Meta

    - `verbose_name` - a string representing the singular name of the model in the Django admin interface
    - `verbose_name_plural` - a string representing the plural name of the model in the Django admin interface
    - `unique_together` - a tuple of field names that must be unique together
    - `get_latest_by` - a string representing the field to use for retrieving the latest record

    ### Properties

    - `lactation_stage` - a string representing the current stage of the lactation period based on the number of days in lactation
    - `lactation_duration` - a string representing the duration of the lactation period in days
    - `end_date_` - a string representing the end date of the lactation period formatted as YYYY-MM-DD, or "Ongoing" if the lactation period is ongoing

    ### Methods

    - `days_in_lactation()` - returns the number of days in the lactation period
    """

    class Meta:
        verbose_name = "Lactation \U0001F37C"
        verbose_name_plural = "Lactations \U0001F37C"
        # unique_together = ('start_date', 'cow')
        get_latest_by = "start_date"

    start_date = models.DateField()
    end_date = models.DateField(null=True, editable=False)
    cow = models.ForeignKey(Cow, on_delete=models.PROTECT, editable=False)
    lactation_number = models.PositiveSmallIntegerField(default=1, editable=False)
    pregnancy = models.OneToOneField(
        Pregnancy, on_delete=models.CASCADE, editable=False
    )

    def days_in_lactation(self):
        """Returns the days in lactation for this lactation instance."""
        today = datetime.today().date()
        if self.end_date:
            end_date = self.end_date
        else:
            end_date = today
        days = (end_date - self.start_date).days
        return days

    @property
    def lactation_stage(self):
        """
        Returns a string representing the current stage of the lactation period based on the number of days in lactation.
        """
        days = self.days_in_lactation()

        if self.end_date:
            return "Ended"
        elif days <= 100:
            return "Early"
        elif days <= 200:
            return "Mid"
        elif days <= 260:
            return "Late"
        else:
            return "Dry"

    @property
    def lactation_duration(self):
        """
        Returns a string representing the duration of the lactation period in days.
        """
        if self.end_date and self.start_date:
            return f"{(self.end_date - self.start_date).days} days"
        else:
            return f"{self.days_in_lactation()} days"

    @property
    def end_date_(self):
        if self.end_date:
            return self.end_date.strftime("%Y-%m-%d")
        else:
            return "Ongoing"

    def __str__(self):
        return f"Lactation record {self.lactation_number} for {self.cow}"


class Milk(models.Model):
    """
    The model is a representation of a cow's milk production.

    ### Fields

    - `milking_date`: The date and time the milk was collected.
    - `cow`: The cow that produced the milk.
    - `amount_in_kgs`: The amount of milk produced, in kilograms.
    - `lactation`: The lactation stage of the cow at the time of milking.

    ### Meta options

    - `verbose_name`: The singular name of the model in the Django admin.
    - `verbose_name_plural`: The plural name of the model in the Django admin.
    - `constraints`: A list of database constraints for the model.

    ### Methods

        - `__str__()` : returns a string representation of the `Milk` object, showing the name of the cow and the milking date.
        - `clean()` :  performs validation on the model fields to ensure data integrity. The following validations are performed:
            - The cow is not dead or sold.
            - The cow is female and old enough to produce milk.
            - The cow is currently in a stage of lactation (early, mid, or late).
            - The amount of milk is greater than 0 and less than or equal to 35 kilograms.

    """

    class Meta:
        verbose_name = "Milk \U0001F95B"
        verbose_name_plural = "Milk \U0001F95B"
        constraints = [
            models.UniqueConstraint(
                fields=["cow", "milking_date"], name="unique_milk_record"
            ),
        ]

    milking_date = models.DateTimeField(auto_now_add=True)
    cow = models.ForeignKey(Cow, on_delete=models.CASCADE, related_name="milk")
    amount_in_kgs = models.DecimalField(
        verbose_name="Amount (kg)",
        default=0.00,
        max_digits=5,
        decimal_places=2,
        validators=[
            MinValueValidator(0, message="Amount of milk can not be less than 0 Kgs."),
            MaxValueValidator(35, message="Amount of milk cannot exceed 35 Kgs."),
        ],
    )
    lactation = models.ForeignKey(
        Lactation, on_delete=models.CASCADE, editable=False, null=True
    )

    def __str__(self):
        """
        Returns:
            `str`: A string representation of the milk record.
        """
        return f"Milk record of cow {self.cow.name} on {self.milking_date.strftime('%Y-%m-%d %H:%M:%S')}"

    def clean(self):
        cow = self.cow
        latest_lactation_record = self.cow.lactation_set.last()

        if latest_lactation_record is None:
            raise ValidationError("Cannot add milk entry, cow has no active lactation")

        elif latest_lactation_record.lactation_stage == "Dry":
            raise ValidationError("Cannot add milk entry, Cow has been dried off")

        elif latest_lactation_record.lactation_stage not in ["Early", "Mid", "Late"]:
            raise ValidationError(
                "Cannot add milk entry, cow's active lactation is not in stages Early, Mid, or Late"
            )

        if cow.availability_status == "Dead":
            raise ValidationError("Cannot add milk record for a dead cow.")

        if cow.availability_status == "Sold":
            raise ValidationError("Cannot add milk record for sold cow.")

        if cow.get_cow_age() < 21 * 30:
            raise ValidationError(
                "Cow is less than 21 months old and should not have a milk record"
            )

        if cow.gender != "Female":
            raise ValidationError("This cow is not female and cannot produce milk.")

        if self.amount_in_kgs <= 0:
            raise ValidationError("Amount in kgs should be greater than 0")


class Semen(models.Model):
    inseminator = models.ForeignKey(Inseminator, on_delete=models.PROTECT)
    producer = models.CharField(
        max_length=64,
        choices=SemenSourceChoices.choices)
    semen_batch = models.CharField(max_length=64)
    date_of_production = models.DateField(
        validators=[MaxValueValidator(date.today())],
        error_messages={
            "max_value": "Invalid date entry, Dates of production must not be in future"
        },
    )
    date_of_expiry = models.DateField(
        validators=[MinValueValidator(date.today())],
        error_messages={
            "min_value": "Invalid date entry, Date of expiry must be in future"
        },
    )
    notes = models.TextField(blank=True)

    def __str__(self):
        """Returns a string representation of the model instance."""
        return f"Semen batch {self.semen_batch} produced by {self.producer} on {self.date_of_production}"


class Symptoms(models.Model):
    """
    A model representing symptoms observed in an animal.

    ### Fields

    - `name` - a `CharField` representing the name of the symptom
    - `type` - a `CharField` representing the type of symptom (choices: Respiratory, Digestive, Reproductive, Musculoskeletal, Metabolic, Other)
    - `description` - a `TextField` representing the description of the symptom
    - `date_observed` - a `DateField` representing the date when the symptom was observed (cannot be in the future)
    - `severity` - a `CharField` representing the severity of the symptom (choices: Mild, Moderate, Severe)
    - `location` - a `CharField` representing the location of the symptom (choices: Head, Neck, Chest, Abdomen, Back, Legs, Tail, Whole body, Other)

    ### Meta

    - `verbose_name` - a string representing the singular name of the model in the Django admin interface
    - `verbose_name_plural` - a string representing the plural name of the model in the Django admin interface

    ### Methods

    - `__str__()` - returns a string representing the symptom's name
    """

    class Meta:
        verbose_name = "Symptom \U0001F912"
        verbose_name_plural = "Symptoms \U0001F912"

    symptom_types = (
        ("Respiratory", "Respiratory"),
        ("Digestive", "Digestive"),
        ("Reproductive", "Reproductive"),
        ("Musculoskeletal", "Musculoskeletal"),
        ("Metabolic", "Metabolic"),
        ("Other", "Other"),
    )

    SEVERITY_CHOICES = (
        ("Mild", "Mild"),
        ("Moderate", "Moderate"),
        ("Severe", "Severe"),
    )
    LOCATION_CHOICES = (
        ("head", "Head"),
        ("Neck", "Neck"),
        ("Chest", "Chest"),
        ("Abdomen", "Abdomen"),
        ("Back", "Back"),
        ("Legs", "Legs"),
        ("Tail", "Tail"),
        ("Whole body", "Whole body"),
        ("Other", "Other"),
    )

    name = models.CharField(max_length=255)
    type = models.CharField(max_length=20, choices=symptom_types)
    description = models.TextField()
    date_observed = models.DateField(
        validators=[MaxValueValidator(date.today())],
        error_messages={
            "max_value": "The date of observation cannot be in the future!."
        },
    )
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES)
    location = models.CharField(max_length=20, choices=LOCATION_CHOICES)

    def __str__(self):
        return self.name


class Pathogen(models.Model):
    """
    A model representing a pathogen.

    ### Fields

    - `name` - a `CharField` representing the name of the pathogen

    ### Meta

    - `verbose_name` - a string representing the singular name of the model in the Django admin interface
    - `verbose_name_plural` - a string representing the plural name of the model in the Django admin interface

    ### Methods

    - `__str__()` - returns the name of the pathogen
    """

    class Meta:
        verbose_name = "Pathogen"
        verbose_name_plural = "Pathogens"

    name = models.CharField(
        max_length=50,
        unique=True,
        choices=(("Virus", "Virus"), ("Bacteria", "Bacteria"), ("Fungi", "Fungi")),
    )

    def __str__(self):
        return self.name


class DiseaseCategory(models.Model):
    """
    A model representing the category of a disease in the farm.

    ### Fields

    - `name` - a `CharField` representing the name of the disease category (unique)

    ### Meta

    - `verbose_name` - a string representing the singular name of the model in the Django admin interface
    - `verbose_name_plural` - a string representing the plural name of the model in the Django admin interface

    ### Methods

    - `__str__()` - returns the name of the disease category

    """

    class Meta:
        verbose_name = "Disease category"
        verbose_name_plural = "Disease categories"

    name = models.CharField(
        max_length=50,
        unique=True,
        choices=(
            ("Nutrition", "Nutrition"),
            ("Infectious", "Infectious"),
            ("Physiological", "Physiological"),
            ("Genetic", "Genetic"),
        ),
    )

    def __str__(self):
        return self.name


class Treatment(models.Model):
    """
    A model representing a treatment given to a cow for a specific disease.

    ### Fields

    - `disease` - a `ForeignKey` representing the disease the cow is being treated for
    - `cow` - a `ForeignKey` representing the cow receiving the treatment
    - `date_of_treatment` - a `DateTimeField` representing the date and time the treatment was given
    - `treatment_method` - a `TextField` representing the method used to treat the cow
    - `duration` - an `IntegerField` representing the duration of the treatment in days (optional)
    - `notes` - a `TextField` representing any notes related to the treatment (optional)
    - `treatment_status` - a `CharField` representing the status of the treatment, with choices: 'Scheduled', 'In progress', 'Completed', 'Cancelled', 'Postponed'
    - `cost` - a `DecimalField` representing the cost of the treatment in dollars (optional)

    ### Meta

    - `verbose_name` - a string representing the singular name of the model in the Django admin interface
    - `verbose_name_plural` - a string representing the plural name of the model in the Django admin interface

    ### Methods

    - `clean()` - ensures that:
        -   `cost` is zero or more
        -   `duration` is greater than zero (if provided),
        -   `duration` is provided if the `treatment_status` is 'Completed'
        -   `notes` are provided if the treatment_status is postponed or cancelled
        -   `cow` has to be available in the farm(not sold or dead)

    """

    class Meta:
        verbose_name = "Treatment \U0001F48E"
        verbose_name_plural = "Treatments \U0001F48E"

    TREATMENT_STATUS_CHOICES = (
        ("Scheduled", "Scheduled"),
        ("In progress", "In Progress"),
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled"),
        ("Postponed", "Postponed"),
    )

    disease = models.ForeignKey("dairy.Disease", on_delete=models.CASCADE)
    cow = models.ForeignKey(Cow, on_delete=models.PROTECT)
    date_of_treatment = models.DateTimeField(auto_now_add=True)
    treatment_method = models.TextField(max_length=200)
    duration = models.IntegerField(blank=True, null=True)
    notes = models.TextField(blank=True)
    treatment_method = models.TextField(max_length=200)
    treatment_status = models.CharField(
        max_length=15, choices=TREATMENT_STATUS_CHOICES, default="Scheduled"
    )
    cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def clean(self):
        if self.cost and self.cost < 0:
            raise ValidationError("The cost should be zero or more")

        if self.duration and self.duration <= 0:
            raise ValidationError("The duration should be greater than zero.")

        if self.treatment_status == "Completed" and not self.duration:
            raise ValidationError(
                "Duration is required when treatment status is completed."
            )

        if self.treatment_status == "Cancelled" and not self.notes:
            raise ValidationError(
                "A note is required when treatment status is cancelled."
            )

        if self.treatment_status == "Postponed" and not self.notes:
            raise ValidationError(
                "A note is required when treatment status is postponed."
            )

        if self.cow.availability_status == "Dead":
            raise ValidationError("Treatment cannot be given to a dead cow.")

        if self.cow.availability_status == "Sold":
            raise ValidationError("Unavailable cow, This cow had been sold")

        if self.duration and self.duration <= 0:
            raise ValidationError("Duration of treatment should be a positive number.")

        if not self.treatment_method:
            raise ValidationError("Treatment method should not be left blank.")


class Disease(models.Model):
    """

    A model representing a disease that affects cows.

    ### Fields

    - `name` - a `CharField` representing the name of the disease (unique)
    - `pathogen` - a `ForeignKey` to the `Pathogen` model representing the pathogen that causes the disease (optional)
    - `categories` - a `ForeignKey` to the `DiseaseCategory` model representing the category the disease belongs to
    - `occurrence_date` - a `DateField` representing the date the disease was first discovered
    - `is_recovered` - a `BooleanField` representing whether or not the cow has recovered from the disease (default=False)
    - `recovered_date` - a `DateField` representing the date the cow recovered from the disease (optional)
    - `notes` - a `TextField` representing any notes related to the disease (optional)
    - `cows` - a `ManyToManyField` to the `Cow` model representing the cows affected by the disease
    - `date_created` - a `DateTimeField` representing the date the disease was recorded
    - `symptoms` - a `ManyToManyField` to the `Symptoms` model representing the symptoms of the disease
    - `treatments` - a `ManyToManyField` to the `Treatment` model representing the treatments for the disease (optional)

    ### Meta

    - `verbose_name` - a string representing the singular name of the model in the Django admin interface
    - `verbose_name_plural` - a string representing the plural name of the model in the Django admin interface

    ### Methods

    - `__str__()` - returns a string representing the disease in the format "name (pathogen) occurred on occurrence_date"
    - `clean()` - validates the data entered for the model, ensuring that the recovered date is provided if the disease is marked as recovered, and that the occurrence date is before the recovered date (if provided).

    ### Rules

    - If the `is_recovered` field is `True`, the `recovered_date` field must not be empty.
    - If the `recovered_date` field is not empty, the `is_recovered` field must be `True`.
    - If the `recovered_date` field is provided, it must be after the `occurrence_date` field.
    """

    name = models.CharField(max_length=50, unique=True)
    pathogen = models.ForeignKey(Pathogen, on_delete=models.CASCADE, null=True)
    categories = models.ForeignKey(
        DiseaseCategory, on_delete=models.PROTECT, related_name="diseases"
    )
    occurrence_date = models.DateField()
    is_recovered = models.BooleanField(default=False)
    recovered_date = models.DateField(blank=True, null=True)
    notes = models.TextField(blank=True)
    cows = models.ManyToManyField(Cow, related_name="diseases")
    date_created = models.DateTimeField(auto_now_add=True)
    symptoms = models.ManyToManyField(Symptoms, related_name="diseases")
    treatments = models.ManyToManyField(Treatment, related_name="diseases", blank=True)

    class Meta:
        verbose_name = "Disease \U0001F48A"
        verbose_name_plural = "Diseases \U0001F48A"

    def __str__(self):
        return "{} ({}) occurred on {}".format(
            self.name, self.pathogen.name, self.occurrence_date
        )

    def clean(self):
        if self.is_recovered and not self.recovered_date:
            raise ValidationError(
                "Recovered date is required if the disease is marked as recovered."
            )

        if self.recovered_date and not self.is_recovered:
            raise ValidationError(
                "Recovered must be set to True if a recovered date is provided."
            )

        if self.recovered_date and self.occurrence_date > self.recovered_date:
            raise ValidationError("Recovered date must be after the occurrence date.")

        if self.occurrence_date > datetime.now().date():
            raise ValidationError("Occurrence date cannot be in the future.")

        if not self.name:
            raise ValidationError("Disease name is required.")

        if not self.pathogen:
            raise ValidationError("Pathogen is required.")

        if self.is_recovered and self.treatments.all().count() == 0:
            raise ValidationError(
                "At least one treatment is required for a recovered disease."
            )


class WeightRecord(models.Model):
    """
    A model representing a weight record of a cow on a particular date.

    ### Fields

    - `cow` - a `ForeignKey` representing the cow whose weight record is being recorded
    - `date` - a `DateField` representing the date on which the weight was recorded (auto-generated)
    - `weight` - a `DecimalField` representing the weight of the cow on the given date

    ### Meta

    - `verbose_name` - a string representing the singular name of the model in the Django admin interface
    - `verbose_name_plural` - a string representing the plural name of the model in the Django admin interface
    - `unique_together` - a tuple specifying that each weight record must have a unique combination of cow and date

    ### Methods

    - `clean()` - validates that weight can only be recorded for cows with availability status 'Alive'
    - `__str__()` - returns a string representing the weight record in the format "cow name - Weight: weight kgs - Date: date"

    """

    class Meta:
        verbose_name = "Weight \U00002696"
        verbose_name_plural = "Weight \U00002696"
        unique_together = ("cow", "date")

    cow = models.ForeignKey(Cow, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    weight = models.DecimalField(
        default=1,
        max_digits=6,
        decimal_places=2,
        validators=[
            MinValueValidator(
                1,
                message="Invalid weight. A cow's minimum weight record can not be less than 1 Kgs.",
            ),
            MaxValueValidator(
                1500,
                message="Invalid weight. A cow's maximum weight can not exceed 1500 Kgs.",
            ),
        ],
    )

    def clean(self):
        if self.cow.availability_status == "Dead":
            raise ValidationError("Weight cannot be recorded for a dead cow.")

        if self.cow.availability_status == "Sold":
            raise ValidationError("Weight cannot be recorded for a sold cow.")

    def __str__(self):
        return f"{self.cow} - Weight: {self.weight} kgs - Date: {self.date}"


class Culling(models.Model):
    """
    ### Fields

    - `cow`: A foreign key to the `Cow` model, which represents the cow being culled. This field is required.
    - `reason`: A string representing the reason for culling the cow. The choices for this field are defined in several tuples, including
        - MEDICAL_REASONS,
        - FINANCIAL_REASONS,
        - PRODUCTION_REASONS,
        - GENETIC_REASONS,
        - ENVIRONMENTAL_REASONS
        - LEGAL_REASONS. The CULLING_REASONS tuple is created by concatenating all of these tuples. This field is required and can be at most 100 characters long.
    - `date`: A date field that is automatically set to the current date when the object is created. This field is required.
    - `notes`: A text field for any additional notes about the culling. This field is optional.

    ### Meta options
    - `verbose_name`: A string representing the human-readable name for a single instance of the model. In this case, it is set to "Culling 🗡️".
    - `verbose_name_plural`: A string representing the human-readable name for multiple instances of the model. In this case, it is set to "Cullings 🗡️".
    - `ordering`: A list or tuple of fields to use when ordering the Culling objects. In this case, the objects are ordered by date in descending order.


    ### Methods
    - `__str__(self)`: A string representation of the Culling object that returns the name of the culled cow and the date of the culling.
    """

    MEDICAL_REASONS = [
        ("disease", "Disease"),
        ("illness", "Illness"),
        ("injuries", "Injuries"),
        ("chronic_health", "Chronic Health Issues"),
    ]
    FINANCIAL_REASONS = [
        ("cost_of_care", "Cost of Care"),
        ("unprofitable", "Unprofitable"),
        ("low_market_demand", "Low Market Demand"),
    ]
    PRODUCTION_REASONS = [
        ("low_production", "Low Production"),
        ("poor_quality", "Poor Quality"),
        ("inefficient_feed", "Inefficient Feed Conversion"),
    ]
    GENETIC_REASONS = [
        ("inherited_diseases", "Inherited Diseases"),
        ("inbreeding", "Inbreeding"),
        ("unwanted_traits", "Unwanted Traits"),
    ]
    ENVIRONMENTAL_REASONS = [
        ("climate_change", "Climate Change"),
        ("natural_disasters", "Natural Disasters"),
        ("overpopulation", "Overpopulation"),
    ]
    LEGAL_REASONS = [
        ("government_regulations", "Government Regulations"),
        ("animal_welfare", "Animal Welfare Standards"),
        ("environmental_protection", "Environmental Protection Laws"),
    ]
    CULLING_REASONS = (
        MEDICAL_REASONS
        + FINANCIAL_REASONS
        + PRODUCTION_REASONS
        + GENETIC_REASONS
        + ENVIRONMENTAL_REASONS
        + LEGAL_REASONS
    )

    cow = models.ForeignKey(Cow, on_delete=models.CASCADE, related_name="cullings")
    reason = models.CharField(max_length=100, choices=CULLING_REASONS)
    date = models.DateField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Culling \U0001F5E1"
        verbose_name_plural = "Cullings \U0001F5E1"
        ordering = ["-date"]

    def __str__(self):
        return f"Culling of {self.cow.name} on {self.date}"


class Vaccination(models.Model):
    DOSE_UNIT_CHOICES = [
        ("ml", "ml"),
        ("cc", "cc"),
        ("mg", "mg"),
        ("g", "g"),
    ]

    class Meta:
        ordering = ["-date_given"]
        unique_together = ("cow", "vaccine_name")

    cow = models.ForeignKey("Cow", on_delete=models.CASCADE)
    vaccine_name = models.CharField(max_length=100)
    date_given = models.DateField(auto_now_add=True)
    dose_amount = models.DecimalField(
        max_digits=7, decimal_places=2, validators=[MinValueValidator(0)]
    )
    dose_unit = models.CharField(max_length=3, choices=DOSE_UNIT_CHOICES, default="ml")

    def __str__(self):
        return f"{self.cow.name} - {self.vaccine_name}"


class Barn(models.Model):
    """
    The `Barn` model represents a barn in a dairy farm.

    Fields:
    - `name`: A character field for the name of the barn.
    - `capacity`: An integer field for the maximum number of cows the barn can hold.

    Meta options:
    - `verbose_name`: The singular name of the model in the Django admin.
    - `verbose_name_plural`: The plural name of the model in the Django admin.
    """

    name = models.CharField(max_length=32)
    capacity = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    class Meta:
        verbose_name = "Barn"
        verbose_name_plural = "Barns"

    def __str__(self):
        return self.name


class CowPen(models.Model):
    """
    The model represents a cow pen in a dairy farm.

    Fields:
    - `barn`: A foreign key to the `Barn` model, representing the barn to which the pen belongs.
    - `type`: A character field for the type of the pen, chosen from the available choices in `CowPenTypeChoices`.
    - `category`: A character field for the category of the pen, chosen from the available choices in `CowPenCategoriesChoices`.
    - `capacity`: An integer field for the maximum number of cows the pen can hold. It must be a positive integer value greater than or equal to 1.

    Methods:
    - `clean()`: A method used for model validation. It checks if a pen of type 'Fixed' is changing its barn, raising a validation error if so.

    """

    barn = models.ForeignKey(Barn, on_delete=models.CASCADE, related_name="pens")
    type = models.CharField(max_length=15, choices=CowPenTypeChoices.choices)
    category = models.CharField(max_length=15, choices=CowPenCategoriesChoices.choices)
    capacity = models.PositiveIntegerField(validators=[MinValueValidator(1)], default=1)

    def clean(self):
        super().clean()
        if self.type == CowPenTypeChoices.Fixed and self.pk:
            old_barn: Barn = CowPen.objects.get(pk=self.pk).barn
            if self.barn != old_barn:
                raise ValidationError("A pen of type 'Fixed' cannot change its barn.")

    def __str__(self):
        return f"Cow Pen {self.type}, {self.category}"


class CowInPenMovement(models.Model):
    """
    The model represents the movement of a cow from one pen to another in a dairy farm.

    Fields:
    - `cow`: A foreign key to the `Cow` model, representing the cow being moved.
    - `previous_pen`: A foreign key to the `CowPen` model, representing the pen from which the cow is being moved.
                      It can be nullable and blank since a cow can be initially placed directly into a new pen.
    - `new_pen`: A foreign key to the `CowPen` model, representing the pen to which the cow is being moved.
    - `timestamp`: A datetime field that automatically records the date and time of the movement.

    """

    cow = models.ForeignKey(Cow, on_delete=models.CASCADE)
    previous_pen = models.ForeignKey(
        CowPen,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="cows_previous_pen",
    )
    new_pen = models.ForeignKey(
        CowPen, on_delete=models.CASCADE, related_name="cows_new_pen"
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.previous_pen:
            return f"Cow {self.cow.id} - From {self.previous_pen} to {self.new_pen}"
        else:
            return f"Cow {self.cow.id} - Newly introduced to {self.new_pen}"


class CowInBarnMovement(models.Model):
    """
    The model represents the movement of a cow from one barn to another in a dairy farm.

    Fields:
    - `cow`: A foreign key to the `Cow` model, representing the cow being moved.
    - `previous_barn`: A foreign key to the `Barn` model, representing the barn from which the cow is being moved.
                       It can be nullable and blank since a cow can be initially introduced directly to a new barn.
    - `new_barn`: A foreign key to the `Barn` model, representing the barn to which the cow is being moved.
    - `timestamp`: A datetime field that automatically records the date and time of the movement.

    """

    cow = models.ForeignKey(Cow, on_delete=models.CASCADE)
    previous_barn = models.ForeignKey(
        Barn, on_delete=models.CASCADE, null=True, blank=True, related_name="moved_cows"
    )
    new_barn = models.ForeignKey(
        Barn, on_delete=models.CASCADE, related_name="received_cows"
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.previous_barn:
            return f"Cow {self.cow.id} - From {self.previous_barn} to {self.new_barn}"
        else:
            return f"Cow {self.cow.id} - Newly introduced to {self.new_barn}"

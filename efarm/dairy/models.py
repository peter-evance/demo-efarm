from django.db import models
from django.utils import timezone
from datetime import date, datetime, timedelta
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator


class Cow(models.Model):
    """
    The `Cow` model represents a single cow in a dairy farm. It contains the following fields:
    
    ### Fields:

    - `name`: A character field for the name of the cow.
    - `breed`: A choice field for the breed of the cow.
    - `date_of_birth`: A date field for the date of birth of the cow.
    - `sire`: A foreign key field that links to the `Cow` model to represent the sire of the cow.
    - `dam`: A foreign key field that links to the `Cow` model to represent the dam of the cow.
    - `calf`: A foreign key field that links to the `Cow` model to represent the calf of the cow.
    - `gender`: A choice field for the gender of the cow.
    - `availability_status`: A choice field for the availability status of the cow.
    - `pregnancy_status`: A choice field for the pregnancy status of the cow.
    - `date_of_death`: A date field for the date of death of the cow.

    ### Properties:

    - `tag_number`: A read-only property that generates a unique tag number for the cow based on its breed, year of birth, and ID.
    - `parity`: A read-only property that returns the number of calves the cow has had.
    - `age`: A read-only property that returns the age of the cow in years, months, and weeks.
    
    ### Methods:
        - `get_cow_age()`: returns the age of the cow in days
        - `clean()`: performs validation on the model fields to ensure data integrity. The following validations are performed:

            - Ensuring that the cow's age is less than 7 years.
            - Ensuring that the cow is not already pregnant.
            - Ensuring that a date of death is specified if the cow's status is set to "Dead".
            - Ensuring that cows must be 21 months or older to be set as pregnant.
            - Ensuring that a young cow cannot have a calf.
            - Ensuring that dead cows can only have a "Not Pregnant" status.

    """
    GENDER_CHOICES = (('Male', 'Male'), ('Female', 'Female'))
    STATUS_CHOICES = (('Alive', 'Alive'), ('Dead', 'Dead'), ('Sold', 'Sold'))
    PREGNANCY_STATUS = (('Pregnant', 'Pregnant'),('Calved', 'Calved'),('Not Pregnant', 'Not Pregnant'))
    BREED_CHOICES = (('Friesian', 'Friesian'),('Ayrshire', 'Ayrshire'),('Sahiwal', 'Sahiwal'),
                     ('Jersey', 'Jersey'),('Crossbreed', 'Crossbreed'),('Guernsey', 'Guernsey'))
    
    class Meta:
        verbose_name = "Cow \U0001F404"
        verbose_name_plural = "Cows \U0001F404"
    
    name = models.CharField(max_length=64, blank=True, null=True)
    breed = models.CharField(max_length=32, choices=BREED_CHOICES, db_index=True)
    date_of_birth = models.DateField(validators=[MaxValueValidator(date.today())],error_messages={'max_value': 'The date of birth cannot be in the future!.'})
    sire = models.ForeignKey('self', on_delete=models.PROTECT, related_name='offspring',blank=True, null=True)
    dam = models.ForeignKey('self', on_delete=models.PROTECT, related_name='calves',blank=True, null=True)
    calf = models.ForeignKey('self', on_delete=models.PROTECT, related_name='dams', blank=True, null=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, db_index=True)
    availability_status = models.CharField(max_length=5, choices=STATUS_CHOICES, default='Alive')
    pregnancy_status = models.CharField(max_length=12, choices=PREGNANCY_STATUS, default='Not Pregnant')
    date_of_death = models.DateField(validators=[MaxValueValidator(date.today())],
                                     error_messages={'max_value': 'The date of death cannot be in the future!.'}, blank=True, null=True)
    
    @property
    def tag_number(self):
        """Returns the Cow's tag number"""
        year_of_birth = self.date_of_birth.strftime('%Y')
        first_letter_of_breed = self.breed[:2].upper()
        counter = self.id
        return f'{first_letter_of_breed}-{year_of_birth}-{counter}'
   
    @property
    def parity(self):
        """Returns the number of times a cow has calved down"""
        return self.calves.count()

    @property
    def age(self):
        """Returns the age of the cow dynamically"""
        age_in_days = self.get_cow_age()
        if age_in_days < 30:
            weeks = int(age_in_days / 7)
            days = age_in_days % 7
            return f"{weeks}wk, {days}d"
        
        elif age_in_days < 365:
            months = int(age_in_days / 30)
            weeks = int((age_in_days % 30) / 7)
            return f"{months}m, {weeks}wk"
        
        else:
            years = int(age_in_days / 365)
            months = int((age_in_days % 365) / 30)
            return f"{years}y, {months}m"
    
    def get_cow_age(self):
        """Calculates the age of a cow in days."""
        return ((timezone.now().date()) - self.date_of_birth).days
    
    def clean(self):
        """Perfoms several validations before saving the cow."""
        
        cow_age = (self.get_cow_age())/365
        if cow_age > 7:
            raise ValidationError('Cow cannot be older than 7 years!')

        if self.availability_status == 'Dead':
            if not self.date_of_death:
                raise ValidationError("Sorry, this cow died! Update it's status by adding the date of death.")
            if (timezone.now().date() - self.date_of_death).days > 1:
                raise ValidationError("Date of death entries longer than 24 hours ago are not allowed.")

        if (self.get_cow_age()/12) < 21 and self.pregnancy_status == 'Pregnant':
            raise ValidationError({'pregnancy_status': 'Cows must be 21 months or older to be set as pregnant'})
        
        if self.get_cow_age()/12 < 21 and self.calf != None:
            raise ValidationError("This cow is still young and cannot have a calf")

        if self.availability_status == 'Dead' and self.pregnancy_status != 'Not Pregnant':
            raise ValidationError({'pregnancy_status': 'Dead cows can only have a "Not Pregnant" status'})
        
    def __str__(self):
        return self.name

class Pregnancy(models.Model):
    """
    This model represents a pregnancy record for a cow.

    ### Fields:

    - `cow`: a foreign key to the Cow model, representing the cow that is pregnant
    - `start_date`: a date field representing the start date of the pregnancy
    - `date_of_calving`: a date field representing the date of calving (i.e., when the cow gives birth)
    - `pregnancy_status`: a character field with a max length of 11, representing the pregnancy status. 
    - `pregnancy_notes`: a text field representing any notes related to the pregnancy
    - `calving_notes`: a text field representing any notes related to the calving process
    - `pregnancy_scan_date`: a date field representing the date of the pregnancy scan (if any)
    - `pregnancy_failed_date`: a date field representing the date when the pregnancy failed (if applicable)
    - `pregnancy_outcome`: a character field with a max length of 11, representing the outcome of the pregnancy. 
    ### Properties:

     - `pregnancy_duration`: returns the duration of the pregnancy in days (if the date of calving is known).
     - `due_date`: returns the due date of the pregnancy (if the start date is known).
    ### Methods:

        - `latest_lactation_stage()`: returns the lactation stage of the cow's latest lactation (if any).
        - `clean()`: performs validation on the model fields to ensure data integrity. The following validations are performed:

            - The cow must be at least 1 year old to be pregnant.
            - The pregnancy status must be 'Confirmed' if a date of calving is provided.
            - The date of calving cannot be in the future.
            - Cannot add a pregnancy record for a dead or sold cow.
            - This cow cannot already be pregnant.
            - This is a female cow.
            - The date of calving must be after the start date.
            - A pregnancy scan date must be after the start date.
            - A pregnancy scan date must be before the due date.
            - Pregnancy status must be 'Confirmed' if the pregnancy outcome is provided.
            - Date of calving must be provided if pregnancy outcome is 'Live'.
            - Start date cannot be in the future.
            - Pregnancy scan date cannot be in the future.
            - A pregnancy failed date must be provided when pregnancy status is 'Failed'.
            - Pregnancy failed date cannot be in the future.
            - Pregnancy failed date cannot be before the start date.
            - Pregnancy status must be 'Failed' if the pregnancy outcome is 'Miscarriage'.
            - Pregnancy status must be 'Confirmed' if the pregnancy outcome is 'Live'.
            - Date of calving must be provided if the pregnancy outcome is 'Live'.
    """
    class Meta:
        verbose_name = "Pregnancies \U0001F930"
        verbose_name_plural = "Pregnancies \U0001F930"
        
    cow = models.ForeignKey(Cow, on_delete=models.PROTECT, related_name='pregnancies')
    start_date = models.DateField()
    date_of_calving = models.DateField(null=True, blank=True)
    pregnancy_status = models.CharField(max_length=11, choices=(('Confirmed', 'Confirmed'), 
                                                                ('Unconfirmed', 'Unconfirmed'),
                                                                ('Failed', 'Failed')), default='Unconfirmed')
    pregnancy_notes = models.TextField(blank=True)
    calving_notes = models.TextField(blank=True)
    pregnancy_scan_date = models.DateField(null=True, blank=True)
    pregnancy_failed_date = models.DateField(validators=[MaxValueValidator(date.today())], 
                                             error_messages={'max_value': 'Future records not allowed!.'}, blank=True, null=True)
    pregnancy_outcome = models.CharField(max_length=11, choices=(('Live', 'Live'), 
                                                                 ('Stillborn', 'Stillborn'), 
                                                                 ('Miscarriage', 'Miscarriage')), blank=True, null=True)
    
    @property
    def pregnancy_duration(self):
        if self.date_of_calving and self.date_of_calving:
            return f"{(self.date_of_calving - self.start_date).days} days"
        else:
            return None
    
    @property
    def due_date(self):
        if self.date_of_calving and self.start_date:
            return "Ended"
        elif self.start_date:
            return self.start_date + timedelta(days=260)
             
    def latest_lactation_stage(self):
        latest_lactation = self.cow.lactation_set.order_by('-start_date').first()
        if latest_lactation:
            return latest_lactation.lactation_stage
        else:
            return "No lactation"

    latest_lactation_stage.short_description = 'Lactation stage'

    def clean(self):
        cow = self.cow
        if cow.get_cow_age() < 350:
            raise ValidationError("This cow must have the pregnancy threshold age of 1 year")
        
        if self.date_of_calving and self.pregnancy_status != 'Confirmed':
            raise ValidationError("Pregnancy status must be 'Confirmed' if a date of calving is provided.")
        
        if self.date_of_calving and self.date_of_calving > timezone.now().date():
            raise ValidationError("Date of calving can not be in the future.")
        
        if cow.availability_status == "Dead":
            raise ValidationError("Cannot add pregnancy record for a dead cow.")
        
        if cow.availability_status == "Sold":
            raise ValidationError("Cannot add pregnancy record for sold cow.")
        
        if cow.pregnancy_status == "Pregnant":
            raise ValidationError("This cow is already pregnant!")
        
        if cow.gender == "Male":
            raise ValidationError("This is a male cow!")
        
        if self.date_of_calving and self.start_date and self.date_of_calving < self.start_date:
            raise ValidationError("Date of calving must be after start date.")
        
        if self.pregnancy_scan_date and self.start_date and self.pregnancy_scan_date < self.start_date:
            raise ValidationError("Pregnancy scan date must be after start date.")
        
        if self.pregnancy_outcome == 'Live' and self.pregnancy_status != 'Confirmed':
            raise ValidationError("Pregnancy status must be 'Confirmed' if pregnancy outcome is provided.")
        
        if self.pregnancy_outcome == 'Live' and not self.date_of_calving:
            raise ValidationError("Date of calving must be provided if pregnancy outcome is 'Live'.")
        
        if self.start_date and self.start_date > timezone.now().date():
            raise ValidationError("Start date cannot be in the future.")
        
        if self.pregnancy_scan_date and self.pregnancy_scan_date > timezone.now().date():
            raise ValidationError("Pregnancy scan date cannot be in the future.")
        
        if self.pregnancy_status == 'Failed' and not self.pregnancy_failed_date:
            raise ValidationError("A pregnancy failed date must be provided when pregnancy status is 'Failed'.")
        
        if self.pregnancy_failed_date and self.pregnancy_failed_date > timezone.now().date():
            raise ValidationError("Pregnancy failed date cannot be in the future.")
        
        if self.pregnancy_failed_date and self.pregnancy_failed_date < self.start_date:
            raise ValidationError("Pregnancy failed date cannot be before start date.")
        
        if self.pregnancy_outcome == 'Miscarriage' and self.pregnancy_status != 'Failed':
            raise ValidationError("Pregnancy status must be 'Failed' if pregnancy outcome is a 'Miscarriage'.")


    def save(self, *args, **kwargs):
        if self.pk is None:
            self.cow.pregnancy_status = 'Pregnant'
        elif self.date_of_calving is not None and self.cow.pregnancy_status == 'Pregnant':
            self.cow.pregnancy_status = 'Calved'
        
        super().save(*args, **kwargs)

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
        get_latest_by = 'start_date'

    start_date = models.DateField()
    end_date = models.DateField(null=True, editable=False)
    cow = models.ForeignKey(Cow, on_delete=models.PROTECT, editable=False)
    lactation_number = models.PositiveSmallIntegerField(default=1, editable=False)
    pregnancy = models.OneToOneField(Pregnancy, on_delete=models.CASCADE, editable=False)


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
            return self.end_date.strftime('%Y-%m-%d')
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
        constraints = [models.UniqueConstraint(
            fields=['cow', 'milking_date'], name='unique_milk_record'),]
        
    milking_date = models.DateTimeField(auto_now_add=True)
    cow = models.ForeignKey(Cow, on_delete=models.CASCADE, related_name='milk')
    amount_in_kgs = models.DecimalField(verbose_name="Amount (kg)", default=0.00 ,max_digits=5,decimal_places=2, 
                                        validators=[MinValueValidator(0, message="Amount of milk can not be less than 0 Kgs."),
                                                    MaxValueValidator(35, message="Amount of milk cannot be more than 35.0 Kgs.")])
    lactation = models.ForeignKey(Lactation, on_delete=models.CASCADE, editable=False, null=True)
         
    def __str__(self):
        """
        Returns:
            `str`: A string representation of the milk record.
        """
        return f"Milk record of cow {self.cow.name} on {self.milking_date.strftime('%Y-%m-%d %H:%M:%S')}"

    def clean(self):
        """
        Validates the data before saving.

        Raises:
            `ValidationError`: If the data is not valid.
        """
        cow = self.cow
        latest_lactation_record = self.cow.lactation_set.last()
        
        if latest_lactation_record is None:
            raise ValidationError("Cannot add milk entry, cow has no active lactation")
        
        elif latest_lactation_record.lactation_stage == "Dry":
            raise ValidationError("Cannot add milk entry, Cow has been dried off")
        
        elif latest_lactation_record.lactation_stage not in ["Early", "Mid", "Late"]:
            raise ValidationError("Cannot add milk entry, cow's active lactation is not in stages Early, Mid, or Late")
        
        if cow.availability_status == "Dead":
            raise ValidationError("Cannot add milk record for a dead cow.")
        
        if cow.availability_status == "Sold":
            raise ValidationError("Cannot add milk record for sold cow.")
        
        if cow.get_cow_age() < 21*30:
            raise ValidationError('Cow is less than 21 months old and should not have a milk record')

        if cow.gender != "Female":
            raise ValidationError("This cow is not female and cannot produce milk.")

        if self.amount_in_kgs <= 0:
            raise ValidationError("Amount in kgs should be greater than 0")

class Heat(models.Model):
    """
    A model representing a heat record for a cow.

    #### Fields:
    - observation_time: The date and time the heat was observed.
    - cow: The cow that the heat record is associated with.

    #### Methods:
    - __str__: Returns a string representation of the heat record.

    #### Validations:
    - observation_time must be in the past.
    - cow must not be pregnant.
    - cow must not already be in heat within the past 2 days.
    - cow must not be dead.
    - cow must be female.
    - cow must not be in heat within 21 days of previous heat observation.
    - cow must be at least 6 months old to be in heat.
    - cow must not be in heat within 60 days after calving.
    """
    class Meta:
        verbose_name = "Heat \U0001F525"
        verbose_name_plural = "Heat \U0001F525"
    observation_time = models.DateTimeField()
    cow = models.ForeignKey(Cow, on_delete=models.CASCADE)   
    
    def __str__(self):
        return f"Heat record for cow {self.cow.tag_number} on {self.observation_time}"
    
    def clean(self):
        if self.observation_time > timezone.now():
            raise ValidationError('Observation time cannot be in the future.')
        
        if self.cow.pregnancy_status == 'Pregnant':
            raise ValidationError('Cow is already pregnant.')
        
        if self.cow.heat_set.filter(observation_time__range=(timezone.now() - timedelta(days=2), timezone.now() + timedelta(days=2))).exists():
            raise ValidationError('Cow is already in heat.')
        
        if self.cow.availability_status == 'Dead':
            raise ValidationError('Cow is dead and cannot be in heat.')

        if self.cow.gender == 'Male':
            raise ValidationError('Heat can only be observed in female cows.')
        
        if self.cow.pregnancy_status == 'Calved' and self.observation_time - self.cow.pregnancy.calving_date < timedelta(days=60):
            raise ValidationError('Cow cannot be in heat within 60 days after calving.')
        
        if self.cow.heat_set.filter(observation_time__range=(timezone.now() - timedelta(days=21), timezone.now())).exists():
            raise ValidationError('Cow cannot be in heat within 21 days of previous heat observation.')  
        
        if self.cow.get_cow_age() < 300:
            raise ValidationError('Cow must be at least 6 months old to be in heat.')
        
class Inseminator(models.Model):
    """
    A model representing an inseminator used in the farm.

    ### Fields

    - `name` - a `CharField` representing the name of the inseminator
    - `company` - a `CharField` representing the company name of the inseminator (optional)
    - `license_number` - a `CharField` representing the license number of the inseminator (unique)
    - `phone_number` - a `CharField` representing the phone number of the inseminator (optional)
    - `email` - an `EmailField` representing the email of the inseminator
    - `address` - a `CharField` representing the address of the inseminator (optional)
    - `notes` - a `TextField` representing any notes related to the inseminator (optional)

    ### Meta

    - `verbose_name` - a string representing the singular name of the model in the Django admin interface
    - `verbose_name_plural` - a string representing the plural name of the model in the Django admin interface

    ### Methods

    - `__str__()` - returns a string representing the inseminator in the format "name (company)"

    """
    class Meta:
        verbose_name = "AI Technician \U0001F3AF"
        verbose_name_plural = "AI Technicians \U0001F3AF"
            
    name = models.CharField(max_length=64)
    company = models.CharField(max_length=64, blank=True, null=True)
    license_number = models.CharField(max_length=32, unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField()
    address = models.CharField(max_length=256, blank=True, null=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        """ Returns a string representing the inseminator in the format "name (company)" """
        return f'{self.name} ({self.company})'
         
class Semen(models.Model):
    """
    A model representing the semen records of a cow.

    ### Fields

    - `inseminator` - a foreign key to the `Inseminator` model representing the inseminator who produced the semen
    - `producer` - a string representing the producer of the semen
    - `semen_batch` - a string representing the semen batch number
    - `date_of_production` - a `DateField` representing the date of production of the semen
    - `date_of_expiry` - a `DateField` representing the date of expiry of the semen
    - `notes` - a `TextField` for adding notes to the record

    ### Meta

    - `verbose_name` - a string representing the singular name of the model in the Django admin interface
    - `verbose_name_plural` - a string representing the plural name of the model in the Django admin interface

    ### Validations

    - `date_of_production` - a validator ensuring that the date is not in the future
    - `date_of_expiry` - a validator ensuring that the date is in the future

    ### Methods

    - `__str__()` - returns a string representation of the model instance

    """
    class Meta:
        verbose_name = "Semen \U0001F4A5"
        verbose_name_plural = "Semen \U0001F4A5"
        
    inseminator = models.ForeignKey(Inseminator, on_delete=models.PROTECT)
    producer = models.CharField(max_length=64, choices=(('KALRO', 'Kenya Agricultural and Livestock Research Organization'), 
                                                        ('KAGRIC', 'Kenya Agricultural and Livestock Research Institute')))
    semen_batch = models.CharField(max_length=64)
    date_of_production = models.DateField(validators=[MaxValueValidator(date.today())], 
                                          error_messages={"max_value":"Invalid date entry, Dates of production must not be in future"})
    date_of_expiry = models.DateField(validators=[MinValueValidator(date.today())],
                                      error_messages={"min_value":"Invalid date entry, Date of expiry must be in future"})
    notes = models.TextField(blank=True)
    
    def __str__(self):
        """Returns a string representation of the model instance."""
        return f"Semen batch {self.semen_batch} produced by {self.producer} on {self.date_of_production}"

class Insemination(models.Model):
    """
    This model represents a record of an insemination event for a cow. 

    ### Fields
        - `date_of_insemination` - A DateField that represents the date on which the insemination was performed. This field is required and is validated to ensure that the date is not in the future.
        - `cow` - A ForeignKey to the Cow model that represents the cow that was inseminated. This field is required and is protected against deletion.
        - `pregnancy` - A ForeignKey to the Pregnancy model that represents the pregnancy resulting from the insemination (if successful). This field is not editable, blank and null is allowed.
        - `success` - A BooleanField that represents whether the insemination was successful or not. This field is optional and defaults to False.
        - `notes` - A TextField that allows the user to add any additional notes about the insemination. This field is optional.
        - `inseminator` - A ForeignKey to the Inseminator model that represents the person who performed the insemination. This field is optional and is protected against deletion.
        - `semen` - A ForeignKey to the Semen model that represents the semen used for the insemination. This field is optional and is protected against deletion.
    
    ### Properties
    `days_since_insemination` - A read-only property that calculates the number of days elapsed since the insemination event.
    
    ### Methods
        - `__str__()` - returns a string representation of the model instance
        - `clean` - A method that is automatically called by Django when the model is validated. It checks that:
            - The cow is alive.
            - The cow is not already pregnant.
            - The cow has been in heat within the last 31 days.
            - The cow is not less than 12 months old.
            - The cow is not inseminated within 21 days.

    """
    class Meta:
        verbose_name = "AI Record \U0001F4C6"
        verbose_name_plural = "AI Records \U0001F4C6"
        ordering = ['-date_of_insemination']
        unique_together = ('cow', 'date_of_insemination')
        
    date_of_insemination = models.DateField(validators=[MaxValueValidator(date.today())],
                                            error_messages={"max_value": "Invalid date entry, Dates must not be in future"})
    cow = models.ForeignKey(Cow, on_delete=models.PROTECT)
    pregnancy = models.ForeignKey(Pregnancy, on_delete=models.PROTECT,editable=False, blank=True, null=True)
    success = models.BooleanField(default=False)
    notes = models.TextField(blank=True)  
    inseminator = models.ForeignKey(Inseminator, on_delete=models.PROTECT, blank=True, null=True)
    semen = models.ForeignKey(Semen, on_delete=models.PROTECT, blank=True, null=True)
    
    @property
    def days_since_insemination(self):
        """Calculates the number of days elapsed since the insemination event. """
        elapsed_time = timezone.now().date() - self.date_of_insemination
        return f"{elapsed_time.days} days"
    
    def __str__(self):
        return f"Insemination record for cow {self.cow.tag_number} on {self.date_of_insemination}"

    def clean(self):
        """
        Validates the model instance before saving it.
        """
        if self.cow.availability_status == 'Dead':
            raise ValidationError('Cannot inseminate a dead cow.')
        
        if self.cow.pregnancy_status == 'Pregnant':
            raise ValidationError('Cannot inseminate a cow that is already pregnant.')

        if not Heat.objects.filter(cow=self.cow, observation_time__range=(self.date_of_insemination - timedelta(days=3), self.date_of_insemination + timedelta(days=3))).exists():
            raise ValidationError('Cow must be in heat at the time of insemination.')
        
        if self.cow.get_cow_age() < 350:
            raise ValidationError('Cow must be at least 12 months old to be inseminated.')
        
        if self.cow.insemination_set.filter(date_of_insemination__range=(timezone.now() - timedelta(days=21), timezone.now())).exists():
            raise ValidationError('Cow cannot be inseminated within 21 days of a previous insemination.')

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
    
    symptom_types = (('Respiratory','Respiratory'), ('Digestive','Digestive'),
                     ('Reproductive','Reproductive'), ('Musculoskeletal','Musculoskeletal'), 
                     ('Metabolic','Metabolic'), ('Other','Other'))
    
    SEVERITY_CHOICES = (('Mild', 'Mild'), ('Moderate', 'Moderate'), ('Severe', 'Severe'),)
    LOCATION_CHOICES = (('head', 'Head'), ('Neck', 'Neck'), ('Chest', 'Chest'),
    ('Abdomen', 'Abdomen'), ('Back', 'Back'), ('Legs', 'Legs'), ('Tail', 'Tail'),
    ('Whole body', 'Whole body'), ('Other', 'Other'),)
    
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=20, choices=symptom_types)
    description = models.TextField()
    date_observed = models.DateField(validators=[MaxValueValidator(date.today())],
                                     error_messages={'max_value': 'The date of observation cannot be in the future!.'})
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
    name = models.CharField(max_length=50, unique=True, choices=(("Virus","Virus"),
                                                                 ("Bacteria","Bacteria"),
                                                                 ("Fungi","Fungi")),)

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
    name = models.CharField(max_length=50, unique=True, choices=(("Nutrition","Nutrition"),("Infectious","Infectious"),
                                                                 ("Physiological","Physiological"),("Genetic","Genetic")),)

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
    
    TREATMENT_STATUS_CHOICES = (('Scheduled', 'Scheduled'),('In progress', 'In Progress'),
                                ('Completed', 'Completed'),('Cancelled', 'Cancelled'),('Postponed', 'Postponed'),)
   
    disease = models.ForeignKey("dairy.Disease", on_delete=models.CASCADE)
    cow = models.ForeignKey(Cow, on_delete=models.PROTECT)
    date_of_treatment = models.DateTimeField(auto_now_add=True)
    treatment_method = models.TextField(max_length=200)
    duration = models.IntegerField(blank=True, null=True)
    notes = models.TextField(blank=True)
    treatment_method = models.TextField(max_length=200)
    treatment_status = models.CharField(max_length=15, choices=TREATMENT_STATUS_CHOICES, default='Scheduled')
    cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    
    def clean(self):
        if self.cost and self.cost < 0:
            raise ValidationError('The cost should be zero or more')
        
        if self.duration and self.duration <= 0:
            raise ValidationError('The duration should be greater than zero.')
        
        if self.treatment_status == 'Completed' and not self.duration:
            raise ValidationError('Duration is required when treatment status is completed.')
        
        if self.treatment_status == 'Cancelled' and not self.notes:
            raise ValidationError('A note is required when treatment status is cancelled.')
        
        if self.treatment_status == 'Postponed' and not self.notes:
            raise ValidationError('A note is required when treatment status is postponed.')
        
        if self.cow.availability_status == 'Dead':
            raise ValidationError('Treatment cannot be given to a dead cow.')
        
        if self.cow.availability_status == 'Sold':
            raise ValidationError('Unavailable cow, This cow had been sold')
        
        if self.duration and self.duration <= 0:
            raise ValidationError('Duration of treatment should be a positive number.')
        
        if not self.treatment_method:
            raise ValidationError('Treatment method should not be left blank.')

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
    categories = models.ForeignKey(DiseaseCategory, on_delete=models.PROTECT,related_name="diseases")
    occurrence_date = models.DateField()
    is_recovered = models.BooleanField(default=False)
    recovered_date = models.DateField(blank=True, null=True)
    notes = models.TextField(blank=True)
    cows = models.ManyToManyField(Cow, related_name="diseases")
    date_created = models.DateTimeField(auto_now_add=True)
    symptoms = models.ManyToManyField(Symptoms, related_name='diseases')
    treatments = models.ManyToManyField(Treatment, related_name='diseases', blank=True, null=True)

    class Meta:
        verbose_name = "Disease \U0001F48A"
        verbose_name_plural = "Diseases \U0001F48A"

    def __str__(self):
        return "{} ({}) occurred on {}".format(self.name, self.pathogen.name, self.occurrence_date)

    def clean(self):
        if self.is_recovered and not self.recovered_date:
            raise ValidationError("Recovered date is required if the disease is marked as recovered.")

        if self.recovered_date and not self.is_recovered:
            raise ValidationError("Recovered must be set to True if a recovered date is provided.")

        if self.recovered_date and self.occurrence_date > self.recovered_date:
            raise ValidationError("Recovered date must be after the occurrence date.")

        if self.occurrence_date > datetime.now().date():
            raise ValidationError("Occurrence date cannot be in the future.")

        if not self.name:
            raise ValidationError("Disease name is required.")

        if not self.pathogen:
            raise ValidationError("Pathogen is required.")

        if self.is_recovered and self.treatments.all().count() == 0:
            raise ValidationError("At least one treatment is required for a recovered disease.")

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
        unique_together = ('cow', 'date')

    cow = models.ForeignKey(Cow, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    weight = models.DecimalField(default = 1, max_digits=6, decimal_places=2,validators=[MinValueValidator(1, 
                                                                                                           message="Invalid weight. A cow's minimum weight record can not be less than 1 Kgs."),
                                                                                         MaxValueValidator(1500, 
                                                                                                           message="Invalid weight. A cow's maximum weight can not exceed 1500 Kgs.")])
   
    def clean(self):
        if self.cow.availability_status == 'Dead':
            raise ValidationError("Weight cannot be recorded for a dead cow.")
        
        if self.cow.availability_status == 'Sold':
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
    
    MEDICAL_REASONS = [('disease', 'Disease'), ('illness', 'Illness'), ('injuries', 'Injuries'), ('chronic_health', 'Chronic Health Issues'),]
    FINANCIAL_REASONS = [('cost_of_care', 'Cost of Care'),('unprofitable', 'Unprofitable'), ('low_market_demand', 'Low Market Demand'),]
    PRODUCTION_REASONS = [('low_production', 'Low Production'),('poor_quality', 'Poor Quality'), ('inefficient_feed', 'Inefficient Feed Conversion'),]
    GENETIC_REASONS = [('inherited_diseases', 'Inherited Diseases'), ('inbreeding', 'Inbreeding'), ('unwanted_traits', 'Unwanted Traits'),]
    ENVIRONMENTAL_REASONS = [('climate_change', 'Climate Change'), ('natural_disasters', 'Natural Disasters'), ('overpopulation', 'Overpopulation'),]
    LEGAL_REASONS = [('government_regulations', 'Government Regulations'), ('animal_welfare', 'Animal Welfare Standards'), ('environmental_protection', 'Environmental Protection Laws'),]
    CULLING_REASONS = MEDICAL_REASONS + FINANCIAL_REASONS + PRODUCTION_REASONS + GENETIC_REASONS + ENVIRONMENTAL_REASONS + LEGAL_REASONS
    
    cow = models.ForeignKey(Cow, on_delete=models.CASCADE, related_name='cullings')
    reason = models.CharField(max_length=100, choices=CULLING_REASONS)
    date = models.DateField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name = "Culling \U0001F5E1"
        verbose_name_plural = "Cullings \U0001F5E1"
        ordering = ['-date']
        
    def __str__(self):
        return f"Culling of {self.cow.name} on {self.date}"

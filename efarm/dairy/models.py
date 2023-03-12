from django.db import models
from datetime import date, datetime, timedelta
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone

class Cow(models.Model):
    """
    The Cow model represents a single cow in a dairy farm.
    It contains information about the cow's breed, date of birth, sire, dam,
    calf, gender, availability status, pregnancy status, and date of death (if applicable).
    It also contains several properties, such as tag_number, parity,
    age, and disease_count, that provide useful information about the cow
    without needing to perform additional database queries.

    Additionally, the Cow model includes several validation checks in the clean method
    to ensure data consistency and prevent errors, 
    such as ensuring that the cow's age is less than 7 years, that the cow is not already pregnant,
    and that a date of death is specified if the cow's status is set to "Dead".

    Overall, this model is an essential part of any dairy farm management system,
    providing crucial information about each cow in the herd and helping to ensure
    that the herd is well-maintained and productive.
    """
    GENDER_CHOICES = (('Male', 'Male'), ('Female', 'Female'))
    STATUS_CHOICES = (('Alive', 'Alive'), ('Dead', 'Dead'), ('Sold', 'Sold'))
    PREGNANCY_STATUS = (('Pregnant', 'Pregnant'),('Calved', 'Calved'),('Not Pregnant', 'Not Pregnant'))
    BREED_CHOICES = (('Friesian', 'Friesian'),('Ayrshire', 'Ayrshire'),
                     ('Jersey', 'Jersey'),('Crossbreed', 'Crossbreed'),('Guernsey', 'Guernsey'),)
    
    # Restriction of duplicate fields need to be:
    # Tweaking the on delete instances of the breed and foreign fields
    
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
    date_of_death = models.DateField(validators=[MaxValueValidator(date.today())],error_messages={'max_value': 'The date of death cannot be in the future!.'}, blank=True, null=True)
    
    @property
    def tag_number(self):  
        year_of_birth = self.date_of_birth.strftime('%Y')
        first_letter_of_breed = self.breed[:2].upper()
        counter = self.id  # The ID is auto-incremented and unique as django uniquely save objects by internal ids
        return f'{first_letter_of_breed}-{year_of_birth}-{counter}'
   
    @property
    def parity(self):
        return self.calves.count()

    @property
    def age(self):
        age_in_days = self.get_cow_age()
        if age_in_days < 30:
            # cow is less than one month old
            weeks = int(age_in_days / 7)
            days = age_in_days % 7
            return f"{weeks}wk, {days}d"
        elif age_in_days < 365:
            # cow is less than one year old
            months = int(age_in_days / 30)
            weeks = int((age_in_days % 30) / 7)
            return f"{months}m, {weeks}wk"
        else:
            # cow is one year or older
            years = int(age_in_days / 365)
            months = int((age_in_days % 365) / 30)
            return f"{years}y, {months}m"
    
    def get_cow_age(self):
        return ((timezone.now().date()) - self.date_of_birth).days
    
    def clean(self):
        # Perform age validation check
        cow_age = (self.get_cow_age())/365
        if cow_age > 7:
            raise ValidationError('Cow cannot be older than 7 years!')

        # Perform death status validation check
        if self.availability_status == 'D':
            if not self.date_of_death:
                raise ValidationError("Sorry, this cow died! Update it's status by adding the date of death.")
            if (timezone.now().date() - self.date_of_death).days > 1:
                raise ValidationError("Date of death entries longer than 24 hours ago are not allowed.")

        if (self.get_cow_age()/12) < 21 and self.pregnancy_status == 'P':
            raise ValidationError({'pregnancy_status': 'Cows must be 21 months or older to be set as pregnant'})
        
        if self.get_cow_age()/12 < 21 and self.calf != None:
            raise ValidationError("This cow is still young and cannot have a calf")

        if self.availability_status == 'D' and self.pregnancy_status != 'N':
            raise ValidationError({'pregnancy_status': 'Dead cows can only have a "Not Pregnant" status'})
        
    def __str__(self):
        return self.name 
class Pregnancy(models.Model):
    """
    This model represents a pregnancy record for a cow. It tracks the start date, end date, due date, date of calving,
    pregnancy status, sire, pregnancy notes, calving notes, pregnancy scan date, artificial insemination and pregnancy outcome.
    """
    class Meta:
        verbose_name = "Pregnancies \U0001F930"
        verbose_name_plural = "Pregnancies \U0001F930"
        
    cow = models.ForeignKey(Cow, on_delete=models.PROTECT, related_name='pregnancies')
    start_date = models.DateField()
    date_of_calving = models.DateField(null=True, blank=True)
    pregnancy_status = models.CharField(max_length=1, choices=(('C', 'Confirmed'), ('U', 'Unconfirmed'), ('F', 'Failed')), default='U')
    pregnancy_notes = models.TextField(blank=True)
    calving_notes = models.TextField(blank=True)
    pregnancy_scan_date = models.DateField(null=True, blank=True)
    pregnancy_failed_date = models.DateField(validators=[MaxValueValidator(date.today())],error_messages={'max_value': 'Future records not allowed!.'}, blank=True, null=True)
    is_pregnant = models.BooleanField(default=True, editable=False)
    pregnancy_outcome = models.CharField(max_length=1, choices=(('L', 'Live'), ('S', 'Stillborn'), ('M', 'Miscarriage')), blank=True, null=True)
    
    @property
    def pregnancy_duration(self):
        if self.start_date and self.date_of_calving:
            return f"{(self.date_of_calving - self.start_date).days} days"
        else:
            return None    
    
    @property
    def due_date(self):
        if self.date_of_calving and self.start_date:
            return "Ended"
        elif self.start_date:
            return self.start_date + timedelta(days=270)

    def clean(self):
        cow = self.cow
        if cow.get_cow_age() < 350:
            raise ValidationError("This cow must have the pregnancy threshold age of 1 year")
        
        if self.date_of_calving and self.pregnancy_status != 'C':
            raise ValidationError("Pregnancy status must be 'Confirmed' if a date of calving is provided.")
        
        if self.date_of_calving and self.date_of_calving > timezone.now().date():
            raise ValidationError("Date of calving can not be in the future.")
        
        if cow.availability_status == "D":
            raise ValidationError("Cannot add pregnancy record for a dead cow.")
        
        if cow.availability_status == "S":
            raise ValidationError("Cannot add pregnancy record for sold cow.")
        
        if cow.pregnancy_status == "P":
            raise ValidationError("This cow is already pregnant!")
        
        if cow.gender == "M":
            raise ValidationError("This is a male cow!")
        
        # if self.start_date and self.due_date and self.start_date > self.due_date:
        #     raise ValidationError("Start date must be before due date.")
        
        if self.date_of_calving and self.start_date and self.date_of_calving < self.start_date:
            raise ValidationError("Date of calving must be after start date.")
        
        # if self.date_of_calving and self.end_date and self.date_of_calving > self.end_date:
        #     raise ValidationError("Date of calving must be before end date.")
        
        if self.pregnancy_scan_date and self.start_date and self.pregnancy_scan_date < self.start_date:
            raise ValidationError("Pregnancy scan date must be after start date.")
        
        if self.pregnancy_scan_date and self.due_date and self.pregnancy_scan_date > self.due_date:
            raise ValidationError("Pregnancy scan date must be before due date.")
        
        if self.pregnancy_outcome == 'L' and self.pregnancy_status != 'C':
            raise ValidationError("Pregnancy status must be 'Confirmed' if pregnancy outcome is provided.")
        
        if self.pregnancy_outcome == 'L' and not self.date_of_calving:
            raise ValidationError("Date of calving must be provided if pregnancy outcome is 'Live'.")
        
        if self.start_date and self.start_date > timezone.now().date():
            raise ValidationError("Start date cannot be in the future.")
        
        if self.pregnancy_scan_date and self.pregnancy_scan_date > timezone.now().date():
            raise ValidationError("Pregnancy scan date cannot be in the future.")
        
        if self.pregnancy_status == 'F' and not self.pregnancy_failed_date:
            raise ValidationError("A pregnancy failed date must be provided when pregnancy status is 'Failed'.")
        
        if self.pregnancy_failed_date and self.pregnancy_failed_date > timezone.now().date():
            raise ValidationError("Pregnancy failed date cannot be in the future.")
        
        if self.pregnancy_failed_date and self.pregnancy_failed_date < self.start_date:
            raise ValidationError("Pregnancy failed date cannot be before start date.")
        
        if self.pregnancy_outcome == 'M' and self.pregnancy_status != 'F':
            raise ValidationError("Pregnancy status must be 'Failed' if pregnancy outcome is 'Miscarriage'.")
        
        if self.pregnancy_outcome == 'S' and self.pregnancy_status != 'C':
            raise ValidationError("Pregnancy status must be 'Confirmed' if pregnancy outcome is 'Stillborn'.")

class Lactation(models.Model):
    """
    ## Lactation Model

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
        unique_together = ('start_date', 'cow')
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
    The `Milk` model is a representation of a cow's milk production.

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

    #### `__str__()`

    Returns a string representation of the `Milk` object, showing the name of the cow and the milking date.

    ### Validation

    The `Milk` model includes validation to ensure that:

    - The cow is not dead or sold.
    - The cow is female and old enough to produce milk.
    - The cow is currently in a stage of lactation (early, mid, or late).
    - The amount of milk is greater than 0 and less than or equal to 35 kilograms.

    If any of these conditions are not met, a `ValidationError` is raised.

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
        latest_lactation = self.cow.lactation_set.last()
        
        if latest_lactation is None:
            raise ValidationError("Cannot add milk entry, cow has no active lactation")
        
        elif latest_lactation.lactation_stage == "Dry":
            raise ValidationError("Cannot add milk entry, Cow has been off")
        
        elif latest_lactation.lactation_stage not in ["Early", "Mid", "Late"]:
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


class WeightRecord(models.Model):
    class Meta:
        verbose_name = "Weight \U00002696"
        verbose_name_plural = "Weight \U00002696"
        unique_together = ('cow', 'date')

    cow = models.ForeignKey(Cow, on_delete=models.CASCADE)
    weight = models.DecimalField(
        default = 1,
        max_digits=6, 
        decimal_places=2,
        help_text="Enter weight in Kgs.",
        validators=[
            MinValueValidator(1, message="Invalid weight. A cow's minimum weight record can not be less than 1 Kgs."),
            MaxValueValidator(1500, message="Invalid weight. A cow's maximum weight can not exceed 1500 Kgs.")])
    date = models.DateField()
    
    
    def clean(self):
        # Check that the date of the weight record is not in the future.
        if self.date > date.today():
            raise ValidationError("Weight record date cannot be in the future.")
        
        # Check that the cow is alive at the time of the weight measurement.
        if self.cow.availability_status == 'D':
            raise ValidationError("Weight cannot be recorded for a dead cow.")
        
        # Check that the cow is present at the time of the weight measurement.
        if self.cow.availability_status == 'S':
            raise ValidationError("Weight cannot be recorded for a sold cow.") 
    
    def __str__(self):
        return f"{self.cow} - Weight: {self.weight} kgs - Date: {self.date}"
    
class Heat(models.Model):
    """
    The Heat model represents a record of a cow being in heat.
    """
    class Meta:
        verbose_name_plural = "Heat records"
    observation_time = models.DateTimeField()
    cow = models.ForeignKey(Cow, on_delete=models.CASCADE)   
    
    def __str__(self):
        return f"Heat record for cow {self.cow.tag_number} on {self.observation_time}"
    
    def clean(self):
        # Check 1: Ensure that observation time is not in the future
        if self.observation_time > timezone.now():
            raise ValidationError('Observation time cannot be in the future.')
        
        # Check 2: Ensure that cow is not already pregnant
        if self.cow.pregnancy_status == 'P':
            raise ValidationError('Cow is already pregnant.')
        
        # Check 3: Ensure that cow is not already in heat
        if self.cow.heat_set.filter(observation_time__range=(timezone.now() - timedelta(days=2), timezone.now() + timedelta(days=2))).exists():
            raise ValidationError('Cow is already in heat.')
        
        # Check 4: Ensure that cow is alive
        if self.cow.availability_status == 'D':
            raise ValidationError('Cow is dead and cannot be in heat.')
        # Check 5: Ensure that cow is female
        if self.cow.gender == 'M':
            raise ValidationError('Heat can only be observed in female cows.')
        
        # Check 6: Ensure that cow is not calved in the last 60 days
        if self.cow.pregnancy_status == 'C' and self.observation_time - self.cow.pregnancy.calving_date < timedelta(days=60):
            raise ValidationError('Cow cannot be in heat within 60 days after calving.')
        
        # Check 7: Ensure that cow is not in heat within 21 days
        if self.cow.heat_set.filter(observation_time__range=(timezone.now() - timedelta(days=21), timezone.now())).exists():
            raise ValidationError('Cow cannot be in heat within 21 days of previous heat observation.')  
        
        # Check 8: Ensure that cow is not less than 10 months old
        if self.cow.get_cow_age() < 300:
            raise ValidationError('Cow must be at least 10 months old to be in heat.')


class Inseminator(models.Model):
    """
    The Inseminator model is used to store information about the inseminators that are used in the farm.
    Inseminators are responsible for artificially inseminating cows in the farm.
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
        return f'{self.name} ({self.company})'
           
class Semen(models.Model):
    """
    This model represents the semen records of a cow. It contains information about the inseminator who produced the semen, the producer of the semen, the semen batch number, the date of production, the date of storage and the expiration date.
    It also allows for notes to be added to the record.
    """
    class Meta:
        verbose_name = "Semen \U0001F4A5"
        verbose_name_plural = "Semen \U0001F4A5"
        
    inseminator = models.ForeignKey(Inseminator, on_delete=models.PROTECT)
    producer = models.CharField(max_length=64, choices=(('KALRO', 'Kenya Agricultural and Livestock Research Organization'), 
                                                        ('KAGRIC', 'Kenya Agricultural and Livestock Research Institute')))
    semen_batch = models.CharField(max_length=64)
    date_of_production = models.DateField(validators=[MaxValueValidator(date.today())], error_messages={"max_value":"Invalid date entry, Dates of production must not be in future"})
    date_of_expiry = models.DateField(validators=[MinValueValidator(date.today())], error_messages={"min_value":"Invalid date entry, Date of expiry must be in future"})
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"Semen batch {self.semen_batch} produced by {self.producer} on {self.date_of_production}"

class Insemination(models.Model):
    """
    The Insemination model represents a record of an insemination event for a cow.
    It captures the date of insemination, the cow that was inseminated, the pregnancy that resulted from the insemination (if successful),
    notes about the insemination, and the inseminator that performed the insemination.
    """
    class Meta:
        verbose_name = "AI Record \U0001F4C6"
        verbose_name_plural = "AI Records \U0001F4C6"
        
    date_of_insemination = models.DateField(validators=[MaxValueValidator(date.today())], error_messages={"max_value":"Invalid date entry, Dates must not be in future"})
    cow = models.ForeignKey(Cow, on_delete=models.PROTECT)
    pregnancy = models.ForeignKey(Pregnancy, on_delete=models.PROTECT,editable=False, blank=True, null=True)
    success = models.BooleanField(default=False)
    notes = models.TextField(blank=True)  
    inseminator = models.ForeignKey(Inseminator, on_delete=models.PROTECT, blank=True, null=True)
    semen = models.ForeignKey(Semen, on_delete=models.PROTECT, blank=True, null=True)
    
    @property
    def days_since_insemination(self):
        """
        Calculates the number of days elapsed since the insemination event.
        """
        elapsed_time = timezone.now().date() - self.date_of_insemination
        print(elapsed_time)
        return f"{elapsed_time.days} days"
    
    def __str__(self):
        return f"Insemination record for cow {self.cow.tag_number} on {self.date_of_insemination}"

    def clean(self):
        # Check 1: Ensure that the cow is alive
        if self.cow.availability_status == 'D':
            raise ValidationError('Cannot inseminate a dead cow.')
        
        # Check 2: Ensure that the cow is not already pregnant
        if self.cow.pregnancy_status == 'P':
            raise ValidationError('Cannot inseminate a cow that is already pregnant.')

        # Check 3: Ensure that the cow has been in heat within the last 3 days
        if not Heat.objects.filter(cow=self.cow, observation_time__range=(self.date_of_insemination - timedelta(days=3), self.date_of_insemination + timedelta(days=3))).exists():
            raise ValidationError('Cow must be in heat at the time of insemination.')
        
        # Check 4: Ensure that the cow is not less than 12 months old
        if self.cow.get_cow_age() < 350:
            raise ValidationError('Cow must be at least 12 months old to be inseminated.')
        
        # # Check 5: Ensure that the cow is not inseminated within 21 days
        if self.cow.insemination_set.filter(date_of_insemination__range=(timezone.now() - timedelta(days=21), timezone.now())).exists():
            raise ValidationError('Cow cannot be inseminated within 21 days of a previous insemination.')

class Culling(models.Model):
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
        
class Pathogen(models.Model):
    class Meta:
        verbose_name = "Pathogen"
        verbose_name_plural = "Pathogens"
    name = models.CharField(max_length=50,choices=(("Virus","Virus"),("Bacteria","Bacteria"),("Fungi","Fungi")), unique=True)

    def __str__(self):
        return self.name

class DiseaseCategory(models.Model):
    class Meta:
        verbose_name = "Disease category"
        verbose_name_plural = "Disease categories"
    name = models.CharField(max_length=50, choices=(("Nutrition","Nutrition"),("Infectious","Infectious"),
                                                    ("Physiological","Physiological"),("Genetic","Genetic")), unique=True)

    def __str__(self):
        return self.name
    
    
class Symptoms(models.Model):
    """
    This class defines the model for symptoms. It has several fields such as name, type, description, date observed, severity, duration, location, visual indicator description, and visual indicator image.
    """
    class Meta:
        verbose_name = "Symptom \U0001F912"
        verbose_name_plural = "Symptoms \U0001F912"
    
    symptom_types = (('respiratory','Respiratory'), ('digestive','Digestive'),
                     ('reproductive','Reproductive'), ('musculoskeletal','Musculoskeletal'), 
                     ('metabolic','Metabolic'), ('other','Other'))
    
    SEVERITY_CHOICES = (('mild', 'Mild'), ('moderate', 'Moderate'), ('severe', 'Severe'),)
    LOCATION_CHOICES = (('head', 'Head'), ('neck', 'Neck'), ('chest', 'Chest'),
    ('abdomen', 'Abdomen'), ('back', 'Back'), ('legs', 'Legs'), ('tail', 'Tail'),
    ('Whole body', 'Whole body'), ('other', 'Other'),)
    
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=20, choices=symptom_types)
    description = models.TextField()
    date_observed = models.DateField(validators=[MaxValueValidator(date.today())],error_messages={'max_value': 'The date of observation cannot be in the future!.'})
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES)
    location = models.CharField(max_length=20, choices=LOCATION_CHOICES)
    
    def __str__(self):
        return self.name
    
class Treatment(models.Model):
    """
    The Treatment model represents a treatment given to a cow for a specific disease or diseases.
    It has fields for the cow, the date of the treatment, the treatment method, the duration of the treatment, notes, and the treatment status.
    It also has a property method for displaying the associated diseases. The model also includes a clean method that validates the data before saving, including checking for associated diseases, validating the treatment status, cost, duration and ensuring that the treatment date is not in the future.
    """
    class Meta:
        verbose_name = "Treatment \U0001F48E"
        verbose_name_plural = "Treatments \U0001F48E"
    
    TREATMENT_STATUS_CHOICES = (('scheduled', 'Scheduled'),('in progress', 'In Progress'),
                                ('completed', 'Completed'),('cancelled', 'Cancelled'),('postponed', 'Postponed'),)
   
    disease = models.ForeignKey("dairy.Disease", on_delete=models.CASCADE)
    cow = models.ForeignKey(Cow, on_delete=models.PROTECT)
    date_of_treatment = models.DateTimeField()
    treatment_method = models.TextField(max_length=200)
    duration = models.IntegerField(blank=True, null=True)
    notes = models.TextField(blank=True)
    treatment_method = models.TextField(max_length=200)
    # image = models.ImageField(upload_to='treatment_images/', blank=True, null=True)
    treatment_status = models.CharField(max_length=15, choices=TREATMENT_STATUS_CHOICES, default='scheduled')
    cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    
    def clean(self):
        if self.cost and self.cost <= 0:
            raise ValidationError('The cost should be greater than zero.')
        
        if self.duration and self.duration <= 0:
            raise ValidationError('The duration should be greater than zero.')
        
        if self.date_of_treatment > timezone.now():
            raise ValidationError('Treatment date cannot be in the future.')
        
        if self.treatment_status == 'completed' and not self.duration:
            raise ValidationError('Duration is required when treatment status is completed.')
        
        if self.treatment_status == 'cancelled' and not self.notes:
            raise ValidationError('A note is required when treatment status is cancelled.')
        
        if self.treatment_status == 'postponed' and not self.notes:
            raise ValidationError('A note is required when treatment status is postponed.')
        
        if self.cow.availability_status == 'D':
            raise ValidationError('Treatment cannot be given to a dead cow.')
        
        if self.cow.availability_status == 'S':
            raise ValidationError('Unavailable cow, This cow had been sold')

        
        if not self.treatment_method:
            raise ValidationError('Treatment method should not be left blank.')

class Disease(models.Model):
    """
    The Disease model represents a disease or condition that has affected a cow or group of cows. 
    It contains information such as the name of the disease, the causative agent (virus, bacteria, or fungi), the category of the disease (nutritional, infectious, physiological, or genetic), the date of occurrence, the date of recovery, and notes on the disease. 
    Additionally, it also contains ManyToManyFields for the affected cows and the symptoms associated with the disease. The model has various methods such as affected_cows, last_treatment, and clean method for validations.
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
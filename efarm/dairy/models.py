from django.db import models
from datetime import date, datetime, timedelta
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone

# Create your models here.

class Breed(models.Model):
    """stores information about breed"""
    FRIESIAN, AYRSHIRE, JERSEY, CROSSBREED, GUERNSEY = 'Friesian','Ayrshire', 'Jersey', 'Crossbreed', 'Guernsey'
    BREED_CHOICES = ((FRIESIAN, 'Friesian'),(AYRSHIRE, 'Ayrshire'),(JERSEY, 'Jersey'),(CROSSBREED, 'Crossbreed'),(GUERNSEY, 'Guernsey'),)
    name = models.CharField(max_length=32, choices=BREED_CHOICES,unique=True)
    
    def __str__(self):
        return self.name.capitalize()
    
    
class Cow(models.Model):
    """Stores information about cows"""
    
    STATUS_CHOICES = (('A', 'Alive'), ('D', 'Dead'), ('S', 'Sold'))
    PREGNANCY_STATUS = (('P', 'Pregnant'),('C', 'Calved'),('N', 'Not Pregnant'))
    
    name = models.CharField(max_length=64, blank=True, null=True)
    breed = models.ForeignKey(Breed, on_delete=models.PROTECT, related_name='breed')
    date_of_birth = models.DateField(validators=[MaxValueValidator(date.today())],error_messages={'max_value': 'The date of birth cannot be in the future!.'})
    sire = models.ForeignKey('self', on_delete=models.PROTECT, related_name='offspring',blank=True, null=True)
    dam = models.ForeignKey('self', on_delete=models.PROTECT, related_name='calves',blank=True, null=True)
    calf = models.ForeignKey('self', on_delete=models.PROTECT, related_name='dams', blank=True, null=True)
    gender = models.CharField(max_length=1, choices=(('M', 'Male'), ('F', 'Female')), db_index=True)
    availability_status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='A')
    pregnancy_status = models.CharField(max_length=1, choices=PREGNANCY_STATUS, default='N')
    date_of_death = models.DateField(validators=[MaxValueValidator(date.today())],error_messages={'max_value': 'The date of death cannot be in the future!.'}, blank=True, null=True)
    
    @property
    def tag_number(self):  
        year_of_birth = self.date_of_birth.strftime('%Y')
        first_two_letters_of_breed = self.breed.name[:2].upper()
        counter = self.id  # The ID is auto-incremented and unique as django uniquely save objects by internal ids
        return f'{first_two_letters_of_breed}-{year_of_birth}-{counter}'
   
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
        verbose_name_plural = "Pregnacy records"
        
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
    A model representing a lactation period of a cow.
    """
    class Meta:
        verbose_name_plural = "Lactation"
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
    The Milk model is a representation of a cow's milk production. It contains information about the milking time,
    milking date, the cow that produced the milk, the amount of milk produced, and the lactation stage of the cow at the time of milking.
    """
    class Meta:
        verbose_name_plural = "Milk"
        constraints = [
            models.UniqueConstraint(fields=['cow', 'milking_date'], name='unique_milk_record'),
        ]
        
    milking_date = models.DateTimeField(auto_now_add=True)
    cow = models.ForeignKey(Cow, on_delete=models.CASCADE, related_name='milk')
    amount_in_kgs = models.DecimalField(verbose_name="Amount (kg)", default=0.00 ,max_digits=5,decimal_places=2, 
                                        validators=[MinValueValidator(0, message="Amount of milk can not be less than 0 Kgs."),
                                                    MaxValueValidator(35, message="Amount of milk cannot be more than 35.0 Kgs.")])
    lactation = models.ForeignKey(Lactation, on_delete=models.CASCADE, editable=False, null=True)
         
    def __str__(self):
        return f"Milk record of cow {self.cow.name} on {self.milking_date.strftime('%Y-%m-%d %H:%M:%S')}"

    def clean(self):
        cow = self.cow
        latest_lactation = self.cow.lactation_set.last()
        
        if latest_lactation is None:
            raise ValidationError("Cannot add milk entry, cow has no active lactation")
        
        elif latest_lactation.lactation_stage == "Dry":
            raise ValidationError("Cannot add milk entry, Cow has been dried off")
        
        elif latest_lactation.lactation_stage not in ["Early", "Mid", "Late"]:
            raise ValidationError("Cannot add milk entry, cow's active lactation is not in stages Early, Mid, or Late")
        
        if cow.availability_status == "D":
            raise ValidationError("Cannot add milk record for a dead cow.")
        
        if cow.availability_status == "S":
            raise ValidationError("Cannot add milk record for sold cow.")
        
        if cow.get_cow_age() < 21*30:
            raise ValidationError('Cow is less than 21 months old and should not have a milk record')

        if cow.gender != "F":
            raise ValidationError("This cow is not female and cannot produce milk.")

        if self.amount_in_kgs <= 0:
            raise ValidationError("Amount in kgs should be greater than 0")
        
        # if self.milking_date > timezone.now():
        #     raise ValidationError("Milking date cannot be in the future.")


class WeightRecord(models.Model):
    class Meta:
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



    
from django.db import models


class CowProductionStatusChoices(models.TextChoices):
    OPEN = "Open"
    PREGNANT_NOT_LACTATING = "Pregnant not Lactating"
    PREGNANT_AND_LACTATING = "Pregnant and Lactating"
    DRY = "Dry"
    CULLED = "Culled"
    BULL = "Bull"
    YOUNG_BULL = "Young Bull"
    YOUNG_HEIFER = "Young Heifer"
    MATURE_BULL = "Mature Bull"
    CALF = "Calf"
    WEANER = "Weaner"


class CowCategoryChoices(models.TextChoices):
    CALF = "Calf"
    WEANER = "Weaner"
    HEIFER = "Heifer"
    BULL = "Bull"
    MILKING_COW = "Milking Cow"


class CowBreedChoices(models.TextChoices):
    """
    Choices for the breed of a cow.

    - `Friesian`: Friesian breed.
    - `Ayrshire`: Ayrshire breed.
    - `Sahiwal`: Sahiwal breed.
    - `Jersey`: Jersey breed.
    - `Crossbreed`: Crossbreed of multiple breeds.
    - `Guernsey`: Guernsey breed.
    """

    FRIESIAN = "Friesian"
    AYRSHIRE = "Ayrshire"
    SAHIWAL = "Sahiwal"
    JERSEY = "Jersey"
    CROSSBREED = "Crossbreed"
    GUERNSEY = "Guernsey"


class SexChoices(models.TextChoices):
    """
    Choices for the sex of a cow.

    - `Male`: Male sex.
    - `Female`: Female sex.
    """

    MALE = "Male"
    FEMALE = "Female"


class CowAvailabilityChoices(models.TextChoices):
    """
    Choices for the availability status of a cow.

    - `Alive`: Cow is alive and active.
    - `Sold`: Cow has been sold.
    - `Dead`: Cow has died.
    """

    ALIVE = "Alive"
    SOLD = "Sold"
    DEAD = "Dead"


class CowPregnancyChoices(models.TextChoices):
    """
    Choices for the pregnancy status of a cow.

    - `Open`: Cow is not pregnant.
    - `Pregnant`: Cow is pregnant.
    - `Calved`: Cow has calved.
    - `Unavailable`: Cow cannot have pregnancy status.
    """

    OPEN = "Open"
    PREGNANT = "Pregnant"
    CALVED = "Calved"
    UNAVAILABLE = "Unavailable"


class PregnancyStatusChoices(models.TextChoices):
    CONFIRMED = "Confirmed"
    UNCONFIRMED = "Unconfirmed"
    FAILED = "Failed"


class PregnancyOutcomeChoices(models.TextChoices):
    LIVE = "Live"
    STILLBORN = "Stillborn"
    MISCARRIAGE = "Miscarriage"


class LactationStageChoices(models.TextChoices):
    EARLY = "Early"
    MID = "Mid"
    LATE = "Late"
    DRY = "Dry"
    ENDED = "Ended"


class CowPenTypeChoices(models.TextChoices):
    """
    Choices for the type of cow pen.

    - `Movable`: Movable pen.
    - `Fixed`: Fixed pen.
    """

    Movable = "Movable"
    Fixed = "Fixed"


class CowPenCategoriesChoices(models.TextChoices):
    """
    Choices for the categories of cow pens.

    - `Calf_Pen`: Pen for calves.
    - `Sick_Pen`: Pen for sick cows.
    - `Breeding_Pen`: Pen for breeding cows.
    - `Quarantine_Pen`: Pen for cows in quarantine.
    - `Bull_Pen`: Pen for bulls.
    - `Heifer_Pen`: Pen for heifers.
    - `Dry_Pen`: Pen for dry cows.
    - `General_Pen`: General-purpose pen.
    """

    Calf_Pen = "Calf Pen"
    Sick_Pen = "Sick Pen"
    Breeding_Pen = "Breeding Pen"
    Quarantine_Pen = "Quarantine Pen"
    Bull_Pen = "Bull Pen"
    Heifer_Pen = "Heifer Pen"
    Dry_Pen = "Dry Pen"
    General_Pen = "General Pen"


class SemenSourceChoices(models.TextChoices):
    KALRO = "Kenya Agricultural and Livestock Research Organization"
    KAGRIC = "Kenya Agricultural and Livestock Research Institute"

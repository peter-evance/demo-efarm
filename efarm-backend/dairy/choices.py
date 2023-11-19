from django.db import models


class CowProductionStatusChoices(models.TextChoices):
    OPEN = "Open"
    PREGNANT_NOT_LACTATING = "Pregnant not Lactating"
    PREGNANT_AND_LACTATING = "Pregnant and Lactating"
    DRY = "Dry"
    CULLED = "Culled"
    QUARANTINED = "Quarantined"
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


class CullingReasonChoices(models.TextChoices):
    # MEDICAL_REASONS
    INJURIES = "Injuries"
    CHRONIC_HEALTH = "Chronic Health Issues"

    # FINANCIAL_REASONS
    COST_OF_CARE = "Cost Of Care"
    UNPROFITABLE = "Unprofitable"
    LOW_MARKET_DEMAND = "Low Market Demand"

    # PRODUCTION_REASONS
    AGE = "Age"
    CONSISTENT_LOW_PRODUCTION = "Consistent_Low Production"
    CONSISTENT_POOR_QUALITY = "Low Quality"
    INEFFICIENT_FEED_CONVERSION = "Inefficient Feed Conversion"

    # GENETIC_REASONS
    INHERITED_DISEASES = "Inherited Diseases"
    INBREEDING = "Inbreeding"
    UNWANTED_TRAITS = "Unwanted Traits"

    # ENVIRONMENTAL_REASONS
    CLIMATE_CHANGE = "Climate Change"
    NATURAL_DISASTER = "Natural Disaster"
    OVERPOPULATION = "Overpopulation"

    # LEGAL_REASONS
    GOVERNMENT_REGULATIONS = "Government Regulations"
    ANIMAL_WELFARE_STANDARDS = "Animal Welfare Standards"
    ENVIRONMENT_PROTECTION_LAWS = "Environmental Protection Laws"


class QuarantineReasonChoices(models.TextChoices):
    SICK_COW = "Sick Cow"
    BOUGHT_COW = "Bought Cow"
    NEW_COW = "New Cow"


class CowPenTypeChoices(models.TextChoices):
    """
    Choices for the type of cow pen.

    - `Movable`: Movable pen.
    - `Fixed`: Fixed pen.
    """

    MOVABLE = "Movable"
    FIXED = "Fixed"


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

    CALF_PEN = "Calf Pen"
    SICK_PEN = "Sick Pen"
    BREEDING_PEN = "Breeding Pen"
    QUARANTINE_PEN = "Quarantine Pen"
    BULL_PEN = "Bull Pen"
    HEIFER_PEN = "Heifer Pen"
    DRY_PEN = "Dry Pen"
    GENERAL_PEN = "General Pen"


class SemenSourceChoices(models.TextChoices):
    KALRO = "Kenya Agricultural and Livestock Research Organization"
    KAGRIC = "Kenya Agricultural and Livestock Research Institute"

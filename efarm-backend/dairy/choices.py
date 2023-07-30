from django.db import models

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
    FRIESIAN = 'Friesian'
    AYRSHIRE = 'Ayrshire'
    SAHIWAL = 'Sahiwal'
    JERSEY = 'Jersey'
    CROSSBREED = 'Crossbreed'
    GUERNSEY = 'Guernsey'

class ProductionStatusChoices(models.TextChoices):
    """
    Choices for the production status of a cow.

    - `OPEN`: Cow is open.
    - `PREGNANT_NOT_LACTATING`: Cow is pregnant but not lactating.
    - `PREGNANT_AND_LACTATING`: Cow is pregnant and lactating.
    - `DRY`: Cow is in a dry period.
    - `CULLED`: Cow has been culled.
    """
    OPEN = 'Open'
    PREGNANT_NOT_LACTATING = 'Pregnant not Lactating'
    PREGNANT_AND_LACTATING = 'Pregnant and Lactating'
    DRY = 'Dry'
    CULLED = 'Culled'


class BreedChoices(models.TextChoices):
    """
    Choices for the breed of a cow.

    - `Friesian`: Friesian breed.
    - `Ayrshire`: Ayrshire breed.
    - `Sahiwal`: Sahiwal breed.
    - `Jersey`: Jersey breed.
    - `Crossbreed`: Crossbreed of multiple breeds.
    - `Guernsey`: Guernsey breed.
    """
    Friesian = 'Friesian'
    Ayrshire = 'Ayrshire'
    Sahiwal = 'Sahiwal'
    Jersey = 'Jersey'
    Crossbreed = 'Crossbreed'
    Guernsey = 'Guernsey'


class SexChoices(models.TextChoices):
    """
    Choices for the sex of a cow.

    - `Male`: Male sex.
    - `Female`: Female sex.
    """
    Male = 'Male'
    Female = 'Female'


class CowAvailabilityChoices(models.TextChoices):
    """
    Choices for the availability status of a cow.

    - `Alive`: Cow is alive and active.
    - `Sold`: Cow has been sold.
    - `Dead`: Cow has died.
    """
    Alive = 'Alive'
    Sold = 'Sold'
    Dead = 'Dead'


class PregnancyChoices(models.TextChoices):
    """
    Choices for the pregnancy status of a cow.

    - `Open`: Cow is not pregnant.
    - `Pregnant`: Cow is pregnant.
    - `Calved`: Cow has calved.
    """
    Open = 'Open'
    Pregnant = 'Pregnant'
    Calved = 'Calved'


class CowPenTypeChoices(models.TextChoices):
    """
    Choices for the type of cow pen.

    - `Movable`: Movable pen.
    - `Fixed`: Fixed pen.
    """
    Movable = 'Movable'
    Fixed = 'Fixed'


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
    Calf_Pen = 'Calf Pen'
    Sick_Pen = 'Sick Pen'
    Breeding_Pen = 'Breeding Pen'
    Quarantine_Pen = 'Quarantine Pen'
    Bull_Pen = 'Bull Pen'
    Heifer_Pen = 'Heifer Pen'
    Dry_Pen = 'Dry Pen'
    General_Pen = 'General Pen'

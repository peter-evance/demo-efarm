from django.db import models


class ProductionStatusChoices(models.TextChoices):
    OPEN = 'Open'
    PREGNANT_NOT_LACTATING = 'Pregnant not Lactating'
    PREGNANT_AND_LACTATING = 'Pregnant and Lactating'
    DRY = 'Dry'
    CULLED = 'Culled'


class BreedChoices(models.TextChoices):
    Friesian = 'Friesian'
    Ayrshire = 'Ayrshire'
    Sahiwal = 'Sahiwal'
    Jersey = 'Jersey'
    Crossbreed = 'Crossbreed'
    Guernsey = 'Guernsey'


class SexChoices(models.TextChoices):
    Male = 'Male'
    Female = 'Female'


class AvailabilityChoices(models.TextChoices):
    Alive = 'Alive'
    Sold = 'Sold'
    Dead = 'Dead'


class PregnancyChoices(models.TextChoices):
    Open = 'Open'
    Pregnant = 'Pregnant'
    Calved = 'Calved'

from django.db import models


class SexChoices(models.TextChoices):
    MALE = 'Male'
    FEMALE = 'Female'

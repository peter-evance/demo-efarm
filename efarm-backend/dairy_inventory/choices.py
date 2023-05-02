from django.db import models


class UpdateType(models.TextChoices):
    Add = 'Added'
    Remove = 'Removed'
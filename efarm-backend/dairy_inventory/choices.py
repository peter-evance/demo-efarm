from django.db import models


class UpdateType(models.TextChoices):
    Added = 'Added'
    Removed = 'Removed'




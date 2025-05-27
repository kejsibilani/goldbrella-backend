from django.db import models


class ZoneLocationChoices(models.TextChoices):
    NEAR_WATER = ('near_water', 'Near Water')
    WITH_SHADE = ('with_shade', 'With Shade')

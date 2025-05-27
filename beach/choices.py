from django.db import models


class OpeningDayChoices(models.TextChoices):
    MONDAY = ('monday', 'Monday')
    TUESDAY = ('tuesday', 'Tuesday')
    WEDNESDAY = ('wednesday', 'wednesday')
    THURSDAY = ('thursday', 'Thursday')
    FRIDAY = ('friday', 'Friday')
    SATURDAY = ('saturday', 'Saturday')
    SUNDAY = ('sunday', 'Sunday')

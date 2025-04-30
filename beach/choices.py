from django.db import models


class OpeningDayChoices(models.TextChoices):
    MONDAY = ('monday', 'Monday')
    TUESDAY = ('tuesday', 'Tuesday')
    WEDNESDAY = ('wednesday', 'wednesday')
    THURSDAY = ('thursday', 'Thursday')
    FRIDAY = ('friday', 'Friday')
    SATURDAY = ('saturday', 'Saturday')
    SUNDAY = ('sunday', 'Sunday')


class OpeningMonthChoices(models.TextChoices):
    JANUARY = ('january', 'January')
    FEBRUARY = ('february', 'February')
    MARCH = ('march', 'March')
    APRIL = ('april', 'April')
    MAY = ('may', 'May')
    JUNE = ('june', 'June')
    JULY = ('july', 'July')
    AUGUST = ('august', 'August')
    SEPTEMBER = ('september', 'September')
    OCTOBER = ('october', 'October')
    NOVEMBER = ('november', 'November')
    DECEMBER = ('december', 'December')

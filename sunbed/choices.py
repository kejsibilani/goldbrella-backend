from django.db import models


class SunbedTypeChoices(models.TextChoices):
    STANDARD = ('standard', 'Standard')
    VIP = ('vip', 'VIP')


class SunbedStatusChoices(models.TextChoices):
    AVAILABLE = ('available', 'Available')
    UNCLEANED = ('uncleaned', 'Uncleaned')
    OCCUPIED = ('occupied', 'Occupied')
    BROKEN = ('broken', 'Broken')

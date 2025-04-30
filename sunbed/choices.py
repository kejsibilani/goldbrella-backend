from django.db import models


class SunbedTypeChoices(models.TextChoices):
    STANDARD = ('standard', 'Standard')
    VIP = ('vip', 'VIP')

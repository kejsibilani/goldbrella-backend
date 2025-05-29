from django.db import models


class BookingStatusChoices(models.TextChoices):
    UNVERIFIED = ('unverified', 'Unverified')
    CANCELLED = ('cancelled', 'Cancelled')
    CONFIRMED = ('confirmed', 'Confirmed')
    RESERVED = ('reserved', 'Reserved')

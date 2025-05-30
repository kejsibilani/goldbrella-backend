from django.db import models


class BookingStatusChoices(models.TextChoices):
    PARTIAL_RESERVED = ('partial_reserved', 'Partial Reserved')
    CANCELLED = ('cancelled', 'Cancelled')
    CONFIRMED = ('confirmed', 'Confirmed')
    RESERVED = ('reserved', 'Reserved')

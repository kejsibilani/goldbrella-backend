from django.db import models


class BookingStatusChoices(models.TextChoices):
    CANCELLED = ('cancelled', 'Cancelled')
    CONFIRMED = ('confirmed', 'Confirmed')
    PENDING = ('pending', 'Pending')

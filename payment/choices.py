from django.db import models


class PaymentMethodChoices(models.TextChoices):
    BANK_TRANSFER = ('bank_transfer', 'Bank Transfer')
    CARD = ('card', 'Card')
    CASH = ('cash', 'Cash')


class PaymentStatusChoices(models.TextChoices):
    CONFIRMED = ('confirmed', 'Confirmed')
    CANCELLED = ('cancelled', 'Cancelled')
    REFUNDED = ('refunded', 'Refunded')
    PENDING = ('pending', 'Pending')
    FAILED = ('failed', 'Failed')

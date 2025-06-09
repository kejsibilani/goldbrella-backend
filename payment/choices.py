from django.db import models


class PaymentMethodChoices(models.TextChoices):
    STRIPE = ('stripe', 'Stripe')
    CASH = ('cash', 'Cash')


class PaymentStatusChoices(models.TextChoices):
    INITIATED = ('initiated', 'Initiated')
    CANCELLED = ('cancelled', 'Cancelled')
    SUCCEEDED = ('succeeded', 'Succeeded')
    REFUNDED = ('refunded', 'Refunded')
    FAILED = ('failed', 'Failed')

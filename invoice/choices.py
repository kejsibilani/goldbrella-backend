from django.db import models


class PaymentMethodChoices(models.TextChoices):
    STRIPE = ('stripe', 'Stripe')
    CASH = ('cash', 'Cash')


class PaymentStatusChoices(models.TextChoices):
    PARTIAL_PAID = ('partial_paid', 'Partial Paid')
    UNPAID = ('unpaid', 'Unpaid')
    PAID = ('paid', 'Paid')

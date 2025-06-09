from django.db import models


class InvoiceStatusChoices(models.TextChoices):
    REFUNDED = ('refunded', 'Refunded')
    UNPAID = ('unpaid', 'Unpaid')
    PAID = ('paid', 'Paid')

from django.db import models


class InvoiceStatusChoices(models.TextChoices):
    UNPAID = ('unpaid', 'Unpaid')
    PAID = ('paid', 'Paid')

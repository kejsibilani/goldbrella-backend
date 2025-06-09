from uuid import uuid4

from django.core.validators import MinValueValidator
from django.db import models
from simple_history.models import HistoricalRecords

from invoice.choices import PaymentMethodChoices
from invoice.choices import PaymentStatusChoices


class BookingInvoice(models.Model):
    _history = HistoricalRecords(related_name="history")

    invoice_number = models.CharField(max_length=50, unique=True, editable=False, default=uuid4)
    booking = models.OneToOneField(
        to='booking.Booking',
        on_delete=models.CASCADE,
        related_name='invoice',
    )

    currency = models.CharField(max_length=3, default='EUR')
    paid_amount = models.DecimalField(
        max_digits=10, decimal_places=2,
        validators=[MinValueValidator(0.0)]
    )
    tax_amount = models.DecimalField(
        max_digits=10, decimal_places=2,
        validators=[MinValueValidator(0.0)],
        default=0.0
    )
    payment_method = models.CharField(
        choices=PaymentMethodChoices.choices,
        max_length=20
    )
    payment_status = models.CharField(
        default=PaymentStatusChoices.UNPAID.value,
        choices=PaymentStatusChoices.choices,
        max_length=20
    )

    @property
    def total_amount(self):
        sunbeds_price = sum(self.booking.sunbeds.values_list('price', flat=True))
        inventory_price = sum([
            price * quantity
            for price, quantity in self.booking.inventory.values_list(
                'inventory_item__price', 'quantity'
            )
        ])
        return sunbeds_price + inventory_price

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Invoices'
        verbose_name = 'Invoice'

    def __str__(self):
        return str(self.invoice_number)

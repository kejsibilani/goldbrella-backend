from decimal import Decimal
from uuid import uuid4

from django.core.validators import MinValueValidator
from django.db import models
from simple_history.models import HistoricalRecords

from invoice.choices import InvoiceStatusChoices


class BookingInvoice(models.Model):
    _history = HistoricalRecords(related_name="history")

    @property
    def id(self):
        return self.booking.pk

    invoice_number = models.CharField(max_length=50, primary_key=True, editable=False, default=uuid4)
    booking = models.OneToOneField(
        to='booking.Booking',
        on_delete=models.CASCADE,
        related_name='invoice',
    )

    currency = models.CharField(max_length=3, default='EUR')
    paid_amount = models.DecimalField(
        max_digits=10, decimal_places=2,
        validators=[MinValueValidator(0.0)],
        default=Decimal(0),
    )
    status = models.CharField(
        default=InvoiceStatusChoices.UNPAID.value,
        choices=InvoiceStatusChoices.choices,
        max_length=20
    )

    @property
    def payment_method(self):
        last_payment = self.payments.last()
        return getattr(last_payment, 'payment_method', None)

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

    @property
    def tax_amount(self):
        try:
            sunbeds_tax = sum(self.booking.sunbeds.values_list('tax_amount', flat=True))
            inventory_tax = sum([
                tax_amount * quantity
                for tax_amount, quantity in self.booking.inventory.values_list(
                    'inventory_item__tax_amount', 'quantity'
                )
            ])
        except Exception:
            inventory_tax = 0.0
            sunbeds_tax = 0.0
        return sunbeds_tax + inventory_tax

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Invoices'
        verbose_name = 'Invoice'

    def __str__(self):
        return str(self.invoice_number)

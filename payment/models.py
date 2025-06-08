from decimal import Decimal
from typing import Iterable

from django.db import models
from django.urls import reverse
from payments import PurchasedItem
from payments.models import BasePayment


class BookingPayment(BasePayment):
    booking = models.ForeignKey(
        to='booking.Booking',
        on_delete=models.CASCADE,
        related_name='payments',
    )

    def get_failure_url(self) -> str:
        # Return a URL where users are redirected after
        # they fail to complete a payment:
        return reverse('payment:payment-failure', args=[self.booking.pk])

    def get_success_url(self) -> str:
        # Return a URL where users are redirected after
        # they successfully complete a payment:
        return reverse('payment:payment-success', args=[self.booking.pk])

    def get_purchased_items(self) -> Iterable[PurchasedItem]:
        # Return items that will be included in this payment.
        yield PurchasedItem(
            price=Decimal(self.booking.invoice.total_amount),
            sku=self.booking.invoice.invoice_number,
            currency=self.booking.invoice.currency,
            name=f'Booking #{self.booking.pk}',
            tax_rate=Decimal(
                (self.booking.invoice.tax_amount / self.booking.invoice.total_amount * 100)
            ),
            quantity=1
        )

    class Meta:
        verbose_name_plural = 'Booking Payments'
        verbose_name = 'Booking Payment'

    def __str__(self):
        return f'Payment for booking {self.booking.pk}'

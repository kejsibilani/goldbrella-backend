from uuid import uuid4

from django.db import models

from payment.choices import PaymentMethodChoices, PaymentStatusChoices


# Create your models here.
class BookingPayment(models.Model):
    booking = models.ForeignKey(
        to='booking.Booking',
        on_delete=models.CASCADE,
        related_name="payments"
    )

    transaction_id = models.CharField(max_length=150, default=uuid4)
    payment_method = models.CharField(max_length=100, choices=PaymentMethodChoices.choices)
    payment_status = models.CharField(
        max_length=10,
        choices=PaymentStatusChoices.choices,
        default=PaymentStatusChoices.PENDING.value
    )
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    @property
    def total_amount(self):
        sunbeds_price = sum(self.booking.sunbeds.values_list('price', flat=True))
        inventory_price = sum(self.booking.inventory_items.values_list('price', flat=True))
        return sunbeds_price + inventory_price

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Booking Payments"
        verbose_name = "Booking Payment"
        constraints = [
            models.UniqueConstraint(
                fields=['booking', 'transaction_id'],
                name='unique_booking_payment_transaction'
            )
        ]

    def __str__(self):
        return f"{self.booking.user.username} - {self.method} - {self.amount}",

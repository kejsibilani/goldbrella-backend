from uuid import uuid4

from django.db import models
from pytz import country_names

from payment.choices import PaymentMethodChoices
from payment.choices import PaymentStatusChoices


class BookingPayment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    note = models.TextField(blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(
        choices=PaymentMethodChoices.choices,
        max_length=20
    )
    status = models.CharField(
        default=PaymentStatusChoices.INITIATED.value,
        choices=PaymentStatusChoices.choices,
        max_length=20
    )

    invoice = models.ForeignKey(
        to='invoice.BookingInvoice',
        on_delete=models.CASCADE,
        related_name='payments'
    )

    # billing detail
    billing_first_name = models.CharField(blank=True, null=True, max_length=200)
    billing_last_name = models.CharField(blank=True, null=True, max_length=200)
    billing_email = models.EmailField(blank=True, null=True)
    billing_phone_number = models.CharField(blank=True, null=True, max_length=20)
    # billing address
    billing_address_1 = models.CharField(blank=True, null=True, max_length=250)
    billing_address_2 = models.CharField(blank=True, null=True, max_length=250)
    billing_city = models.CharField(blank=True, null=True, max_length=100)
    billing_postcode = models.CharField(blank=True, null=True, max_length=20)
    billing_country_code = models.CharField(choices=country_names.items(), blank=True, null=True, max_length=5)

    external_intent = models.CharField(max_length=128, blank=True, null=True)
    client_secret = models.CharField(max_length=256, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Booking Payments'
        verbose_name = 'Booking Payment'

    def __str__(self):
        return f'Payment for booking {self.invoice.booking.pk}'

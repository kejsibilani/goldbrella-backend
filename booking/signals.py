from decimal import Decimal

from django.db.models.signals import post_save
from django.dispatch import receiver

from booking.models import Booking
from booking.models import BookingToken
from invoice.choices import PaymentMethodChoices
from invoice.models import BookingInvoice


@receiver(post_save, sender=Booking)
def create_booking_token(instance, created, **kwargs):
    if created: BookingToken.objects.create(booking=instance)
    return


@receiver(post_save, sender=Booking)
def create_invoice_for_booking(instance, created, **kwargs):
    if created: BookingInvoice.objects.get_or_create(
        booking=instance,
        defaults={
            'payment_method': PaymentMethodChoices.STRIPE.value,
            'paid_amount': Decimal(0),
        }
    )

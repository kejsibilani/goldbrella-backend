from decimal import Decimal

from django.conf import settings
from django.db.models.signals import post_save
from django.db.models.signals import pre_save
from django.dispatch import receiver

from booking.choices import BookingStatusChoices
from booking.models import Booking
from booking.models import BookingToken
from booking.tasks import cancel_partial_bookings
from invoice.choices import PaymentMethodChoices
from invoice.models import BookingInvoice


@receiver(pre_save, sender=Booking)
def set_booking_initial_status(instance, **kwargs):
    if not instance.pk:
        if instance.booked_by.is_guest:
            setattr(instance, "status", BookingStatusChoices.PARTIAL_RESERVED.value)
        else:
            setattr(instance, "status", BookingStatusChoices.RESERVED.value)
    return


@receiver(post_save, sender=Booking)
def schedule_auto_cancellation(instance, created, **kwargs):
    if created: cancel_partial_bookings.apply_async(
        args=[instance.id],
        countdown=settings.RESERVATION_CANCELLATION_INTERVAL
    )
    return


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

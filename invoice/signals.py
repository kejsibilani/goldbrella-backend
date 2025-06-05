from decimal import Decimal

from django.db.models.signals import post_save
from django.db.models.signals import pre_save
from django.dispatch import receiver

from booking.choices import BookingStatusChoices
from invoice.choices import PaymentStatusChoices
from invoice.models import BookingInvoice


@receiver(pre_save, sender=BookingInvoice)
def update_invoice_status(instance, **kwargs):
    if instance.paid_amount == Decimal(0):
        setattr(instance, 'payment_status', PaymentStatusChoices.UNPAID.value)
    elif instance.paid_amount == instance.total_amount:
        setattr(instance, 'payment_status', PaymentStatusChoices.PAID.value)
    elif 0 < instance.paid_amount < instance.total_amount:
        setattr(instance, 'payment_status', PaymentStatusChoices.PARTIAL_PAID.value)
    return


@receiver(post_save, sender=BookingInvoice)
def update_booking_status(instance, **kwargs):
    if instance.payment_status == PaymentStatusChoices.PAID.value:
        setattr(instance.booking, 'status', BookingStatusChoices.CONFIRMED.value)
    elif instance.payment_status == PaymentStatusChoices.PARTIAL_PAID.value:
        setattr(instance.booking, 'status', BookingStatusChoices.RESERVED.value)
    else:
        if instance.booking.booked_by.has_role('guest'):
            setattr(instance.booking, "status", BookingStatusChoices.PARTIAL_RESERVED.value)
        else:
            setattr(instance.booking, "status", BookingStatusChoices.RESERVED.value)
    instance.booking.save()

from decimal import Decimal

from django.db.models.signals import post_save
from django.db.models.signals import pre_save
from django.dispatch import receiver

from booking.choices import BookingStatusChoices
from invoice.choices import InvoiceStatusChoices
from invoice.models import BookingInvoice


@receiver(pre_save, sender=BookingInvoice)
def update_invoice_status(instance, **kwargs):
    if instance.paid_amount == instance.total_amount:
        setattr(instance, 'payment_status', InvoiceStatusChoices.PAID.value)
    else:
        setattr(instance, 'payment_status', InvoiceStatusChoices.UNPAID.value)
    return


@receiver(post_save, sender=BookingInvoice)
def update_booking_status(instance, **kwargs):
    if instance.is_refunded:
        setattr(instance.booking, 'status', BookingStatusChoices.CANCELLED.value)
        return instance.booking.save()

    if instance.payment_status == InvoiceStatusChoices.PAID.value:
        setattr(instance.booking, 'status', BookingStatusChoices.CONFIRMED.value)
        return instance.booking.save()

    if instance.booking.booked_by.is_guest:
        setattr(instance.booking, "status", BookingStatusChoices.PARTIAL_RESERVED.value)
    else:
        setattr(instance.booking, "status", BookingStatusChoices.RESERVED.value)
    return instance.booking.save()

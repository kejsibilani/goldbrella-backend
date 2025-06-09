from django.db.models.signals import post_save
from django.dispatch import receiver

from booking.choices import BookingStatusChoices
from invoice.choices import InvoiceStatusChoices
from invoice.models import BookingInvoice


@receiver(post_save, sender=BookingInvoice)
def update_booking_status(instance, **kwargs):
    if instance.payment_status == InvoiceStatusChoices.REFUNDED.value:
        setattr(instance.booking, 'status', BookingStatusChoices.CANCELLED.value)
    elif instance.payment_status == InvoiceStatusChoices.PAID.value:
        setattr(instance.booking, 'status', BookingStatusChoices.CONFIRMED.value)
    else:
        if instance.booking.booked_by.is_guest:
            setattr(instance.booking, "status", BookingStatusChoices.PARTIAL_RESERVED.value)
        else:
            setattr(instance.booking, "status", BookingStatusChoices.RESERVED.value)
    instance.booking.save()

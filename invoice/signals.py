from datetime import timedelta

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from booking.choices import BookingStatusChoices
from invoice.choices import InvoiceStatusChoices
from invoice.models import BookingInvoice
from mailer.scripts import schedule_email
from mailer.system import system_info


@receiver(post_save, sender=BookingInvoice)
def update_booking_status(instance, **kwargs):
    if instance.status == InvoiceStatusChoices.REFUNDED.value:
        setattr(instance.booking, 'status', BookingStatusChoices.CANCELLED.value)
    elif instance.status == InvoiceStatusChoices.PAID.value:
        setattr(instance.booking, 'status', BookingStatusChoices.CONFIRMED.value)
    else:
        if instance.booking.booked_by.is_guest:
            setattr(instance.booking, "status", BookingStatusChoices.PARTIAL_RESERVED.value)
        else:
            setattr(instance.booking, "status", BookingStatusChoices.RESERVED.value)
    instance.booking.save()


@receiver(post_save, sender=BookingInvoice)
def trigger_booking_email(instance, created, **kwargs):
    cancellation_interval = getattr(settings, 'RESERVATION_CANCELLATION_INTERVAL', 300)
    if created and instance.booking.is_anonymous: schedule_email(
        hold_expiry_datetime=instance.booking.created + timedelta(minutes=cancellation_interval),
        hold_expiry_minutes=cancellation_interval // 60,
        template_name='booking_reservation',
        to=[instance.booking.user.email],
        user=instance.booking.user,
        company=system_info,
        invoice=instance,
        system_mail=True
    )

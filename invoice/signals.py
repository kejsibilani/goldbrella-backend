from decimal import Decimal

from django.db.models.signals import post_save
from django.db.models.signals import pre_save
from django.dispatch import receiver

from booking.models import Booking
from invoice.choices import PaymentMethodChoices
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


@receiver(post_save, sender=Booking)
def create_invoice_for_booking(instance, created, **kwargs):
    if created: BookingInvoice.objects.get_or_create(
        booking=instance,
        defaults={
            'payment_method': PaymentMethodChoices.STRIPE.value,
            'paid_amount': 0,
        }
    )

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from rest_framework.exceptions import ValidationError

from booking.choices import BookingStatusChoices
from payment.choices import PaymentStatusChoices
from payment.models import BookingPayment


@receiver(pre_save, sender=BookingPayment)
def validate_booking_payment(instance, **kwargs):
    if instance.paid_amount > instance.total_amount:
        raise ValidationError(
            {'detail':"Paid amount cannot be greater than total amount."}
        )
    return

@receiver(post_save, sender=BookingPayment)
def set_booking_status(sender, instance, **kwargs):
    latest_instance = sender.objects.filter(
        booking=instance.booking
    ).order_by('updated').last()
    if latest_instance.payment_status == PaymentStatusChoices.PENDING.value:
        instance.booking.status = BookingStatusChoices.PENDING.value
    elif latest_instance.payment_status == PaymentStatusChoices.CONFIRMED.value:
        instance.booking.status = BookingStatusChoices.CONFIRMED.value
    else:
        instance.booking.status = BookingStatusChoices.CANCELLED.value
    instance.booking.save()

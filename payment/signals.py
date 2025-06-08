from django.dispatch import receiver
from payments import PaymentStatus
from payments.signals import status_changed


@receiver(status_changed)
def on_payment_status_changed(instance, **kwargs):
    invoice = instance.booking.invoice

    if instance.status == PaymentStatus.CONFIRMED:
        invoice.paid_amount = invoice.total_amount
    elif instance.status == PaymentStatus.REFUNDED:
        invoice.paid_amount = instance.captured_amount
    else:
        invoice.paid_amount = invoice.paid_amount
    invoice.save()

from django.db.models.aggregates import Sum
from django.db.models.signals import post_save
from django.dispatch import receiver

from invoice.choices import InvoiceStatusChoices
from payment.choices import PaymentStatusChoices
from payment.models import BookingPayment


PAYMENT_CHANGE_STATUSES = [
    PaymentStatusChoices.REFUNDED.value,
    PaymentStatusChoices.SUCCEEDED.value,
]

def calculate_total_amount(invoice, status):
    try:
        total_paid_amount = invoice.payments.filter(
            status=status
        ).aggregate(
            total=Sum('amount')
        )['total'] or 0
    except (AttributeError, KeyError):
        total_paid_amount = 0
    return total_paid_amount


@receiver(post_save, sender=BookingPayment)
def update_invoice_amount_on_payment(instance, created, **kwargs):
    if instance.status in PAYMENT_CHANGE_STATUSES:
        # calculate total paid amount
        paid_amount = calculate_total_amount(instance.invoice, PaymentStatusChoices.SUCCEEDED.value)
        refunded_amount = calculate_total_amount(instance.invoice, PaymentStatusChoices.REFUNDED.value)

        # update invoice paid_amount
        instance.invoice.paid_amount = (paid_amount - refunded_amount)
        instance.invoice.save()
    return


@receiver(post_save, sender=BookingPayment)
def update_invoice_status_on_payment(instance, created, **kwargs):
    if instance.status in PAYMENT_CHANGE_STATUSES:
        # calculate total paid amount
        paid_amount = calculate_total_amount(instance.invoice, PaymentStatusChoices.SUCCEEDED.value)
        refunded_amount = calculate_total_amount(instance.invoice, PaymentStatusChoices.REFUNDED.value)
        # fetch total amount
        total_amount = instance.invoice.total_amount

        # set invoice status
        if paid_amount == refunded_amount:
            instance.invoice.status = InvoiceStatusChoices.REFUNDED.value
        elif paid_amount == total_amount:
            instance.invoice.status = InvoiceStatusChoices.PAID.value
        else:
            instance.invoice.status = InvoiceStatusChoices.UNPAID.value
        instance.invoice.save()
    return

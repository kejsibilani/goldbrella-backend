import stripe
from django.conf import settings
from rest_framework.request import Request

from payment.models import BookingPayment

stripe.api_key = settings.STRIPE_SECRET_KEY
class PaymentHandler:
    @staticmethod
    def payment_intent(payment: BookingPayment):
        intent = stripe.PaymentIntent.create(
            amount=int(payment.amount * 100),
            currency=payment.invoice.currency.lower(),
            metadata={'invoice': str(payment.invoice.invoice_number)},
            description=f"Payment for invoice {payment.invoice.invoice_number}",
            receipt_email=payment.billing_email,
        )
        return intent

    @staticmethod
    def webhook_event(request: Request):
        payload = request.body
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']
        endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
        return event


handler = PaymentHandler()

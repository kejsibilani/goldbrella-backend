from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response

from payment.choices import PaymentMethodChoices
from payment.choices import PaymentStatusChoices
from payment.models import BookingPayment
from payment.scripts import handler


@csrf_exempt
@api_view(['POST'])
def stripe_webhook(request):
    try:
        event = handler.webhook_event(request)
    except Exception as e:
        return Response({'error': str(e)}, status=400)

    # get stripe queryset
    queryset = BookingPayment.objects.filter(
        payment_method=PaymentMethodChoices.STRIPE.value
    )

    # Helper function
    def update_payment_status(payment, status, note=None):
        if payment and payment.status != status:
            payment.status = status
            if note: payment.note = (payment.note or '') + f'\n{note}'
            payment.save()  # This triggers signals for invoice sync

    event_type = event['type']
    # payment_intent events
    if event_type == 'payment_intent.created':
        intent = event['data']['object']
        payment = queryset.filter(external_id=intent['id']).first()
        update_payment_status(payment, PaymentStatusChoices.INITIATED.value, note='PaymentIntent created.')

    elif event_type == 'payment_intent.processing':
        intent = event['data']['object']
        payment = queryset.filter(external_id=intent['id']).first()
        update_payment_status(payment, PaymentStatusChoices.PROCESSING.value, note='Stripe is processing payment.')

    elif event_type == 'payment_intent.requires_action':
        intent = event['data']['object']
        payment = queryset.filter(external_id=intent['id']).first()
        update_payment_status(payment, PaymentStatusChoices.ACTION_REQUIRED.value, note='Additional authentication required.')

    elif event_type == 'payment_intent.amount_capturable_updated':
        intent = event['data']['object']
        payment = queryset.filter(external_id=intent['id']).first()
        update_payment_status(payment, PaymentStatusChoices.CAPTURABLE.value, note='Amount capturable updated.')

    elif event_type == 'payment_intent.canceled':
        intent = event['data']['object']
        payment = queryset.filter(external_id=intent['id']).first()
        update_payment_status(payment, PaymentStatusChoices.CANCELLED.value, note='PaymentIntent cancelled.')

    elif event_type == 'payment_intent.succeeded':
        intent = event['data']['object']
        payment = queryset.filter(external_id=intent['id']).first()
        update_payment_status(payment, PaymentStatusChoices.SUCCEEDED.value, note='PaymentIntent succeeded.')

    elif event_type == 'payment_intent.payment_failed':
        intent = event['data']['object']
        payment = queryset.filter(external_id=intent['id']).first()
        update_payment_status(payment, PaymentStatusChoices.FAILED.value, note='PaymentIntent failed.')

    # charge events
    elif event_type == 'charge.succeeded':
        charge = event['data']['object']
        intent_id = charge.get('payment_intent')
        payment = queryset.filter(external_id=intent_id).first()
        update_payment_status(payment, PaymentStatusChoices.CHARGE_SUCCEEDED.value, note='Charge succeeded.')

    elif event_type == 'charge.failed':
        charge = event['data']['object']
        intent_id = charge.get('payment_intent')
        payment = queryset.filter(external_id=intent_id).first()
        update_payment_status(payment, PaymentStatusChoices.CHARGE_FAILED.value, note='Charge failed.')

    elif event_type == 'charge.pending':
        charge = event['data']['object']
        intent_id = charge.get('payment_intent')
        payment = queryset.filter(external_id=intent_id).first()
        update_payment_status(payment, PaymentStatusChoices.CHARGE_PENDING.value, note='Charge pending.')

    elif event_type == 'charge.captured':
        charge = event['data']['object']
        intent_id = charge.get('payment_intent')
        payment = queryset.filter(external_id=intent_id).first()
        update_payment_status(payment, PaymentStatusChoices.CHARGE_CAPTURED.value, note='Charge captured.')

    elif event_type == 'charge.refunded' or event_type == 'charge.refund.updated':
        charge = event['data']['object']
        intent_id = charge.get('payment_intent')
        payment = queryset.filter(external_id=intent_id).first()
        update_payment_status(payment, PaymentStatusChoices.REFUNDED.value, note='Charge refunded.')

    elif event_type == 'charge.expired':
        charge = event['data']['object']
        intent_id = charge.get('payment_intent')
        payment = queryset.filter(external_id=intent_id).first()
        update_payment_status(payment, PaymentStatusChoices.CHARGE_EXPIRED.value, note='Charge expired.')

    elif event_type == 'charge.dispute.created':
        charge = event['data']['object']
        intent_id = charge.get('payment_intent')
        payment = queryset.filter(external_id=intent_id).first()
        update_payment_status(payment, PaymentStatusChoices.DISPUTED.value, note='Charge dispute created.')

    else:
        # Optionally log unexpected events for audit/troubleshooting
        pass

    return Response({'status': 'success'})

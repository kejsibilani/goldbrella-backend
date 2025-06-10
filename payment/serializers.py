from django.conf import settings
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from helpers.short_func import nested_getattr
from payment.choices import PaymentMethodChoices
from payment.models import BookingPayment


class BookingPaymentSerializer(serializers.ModelSerializer):
    stripe = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = BookingPayment
        exclude = ('external_intent', 'client_secret')
        read_only_fields = ('status',)
        extra_kwargs = {
            'invoice': {'required': True},
            'amount': {'required': False},
        }

    def validate_payment_method(self, value):
        context_user = getattr(self.context.get('request'), 'user', None)
        is_superuser = getattr(context_user, 'is_superuser', False)
        is_staff = getattr(context_user, 'is_staff', False)

        if value == PaymentMethodChoices.CASH.value and not (is_superuser or is_staff):
            raise PermissionDenied({'detail': 'Only staff and superuser can handle cash method'})

        return value

    def validate(self, data):
        # remove amount (if any)
        data.pop('amount', None)

        # set invoice total amount as amount
        invoice = data.get('invoice', getattr(self.instance, 'invoice', None))
        data.setdefault('amount', invoice.total_amount)

        # autofill details from booking user
        booking_user = nested_getattr(invoice, 'booking', 'user')
        data.setdefault('billing_first_name', getattr(booking_user, 'first_name', None))
        data.setdefault('billing_last_name', getattr(booking_user, 'last_name', None))
        data.setdefault('billing_email', getattr(booking_user, 'email', None))
        data.setdefault('billing_phone_number', getattr(booking_user, 'phone_number', None))
        return data

    @staticmethod
    def get_stripe(instance):
        if instance.payment_method == PaymentMethodChoices.STRIPE.value:
            return {
                'client_secret': instance.client_secret,
                'publishable_key': settings.STRIPE_PUBLISHABLE_KEY
            }
        return None

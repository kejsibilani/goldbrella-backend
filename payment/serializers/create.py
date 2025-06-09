from rest_framework import serializers

from invoice.choices import PaymentMethodChoices
from payment.models import BookingPayment


class BookingPaymentCreateSerializer(serializers.ModelSerializer):
    variant = serializers.ChoiceField(choices=PaymentMethodChoices.choices)

    class Meta:
        model = BookingPayment
        fields = '__all__'

    def to_representation(self, instance):
        return {
            'id': instance.pk,
            'status': instance.status,
            'booking': instance.booking.pk,
        }


class PaymentValidationSerializer(serializers.Serializer):
    payment_method = serializers.ChoiceField(choices=PaymentMethodChoices.choices, source='variant')

    billing_first_name = serializers.CharField(required=False)
    billing_last_name = serializers.CharField(required=False)
    billing_address_1 = serializers.CharField(required=False)
    billing_address_2 = serializers.CharField(required=False)
    billing_city = serializers.CharField(required=False)
    billing_postcode = serializers.CharField(required=False)
    billing_country_code = serializers.CharField(required=False)
    billing_country_area = serializers.CharField(required=False)
    billing_email = serializers.EmailField(required=False)
    billing_phone = serializers.CharField(required=False)

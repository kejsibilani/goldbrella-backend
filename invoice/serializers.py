from decimal import Decimal

from rest_framework import serializers

from invoice.choices import PaymentMethodChoices
from invoice.models import BookingInvoice


class BookingInvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingInvoice
        fields = '__all__'
        read_only_fields = ('invoice_number', 'booking', 'payment_status')

    def validate_paid_amount(self, value):
        if value < 0:
            raise serializers.ValidationError({'paid_amount': 'Paid amount cannot be negative'})
        elif value > getattr(self.instance, 'total_amount', Decimal(0)):
            raise serializers.ValidationError({'paid_amount': 'Paid amount cannot be greater than total amount'})
        return value

    def validate(self, data):
        payment_method = data.pop('payment_method', getattr(self.instance, 'payment_method', None))
        paid_amount = data.pop('paid_amount', Decimal(0))

        if paid_amount and payment_method != PaymentMethodChoices.CASH.value:
            raise serializers.ValidationError({'paid_amount': 'Payment payment is not cash.'})
        return data

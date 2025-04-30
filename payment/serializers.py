from rest_framework import serializers

from payment.models import BookingPayment


class BookingPaymentSerializer(serializers.ModelSerializer):
    total_amount = serializers.SerializerMethodField()

    class Meta:
        model = BookingPayment
        fields = "__all__"

    def validate(self, attrs):
        # payment method
        payment_method = attrs.get('payment_method', getattr(self.instance, 'payment_method', None))
        transaction_id = attrs.get('transaction_id', getattr(self.instance, 'transaction_id', None))
        if payment_method != 'cash' and not transaction_id:
            raise serializers.ValidationError("Transaction ID is required for non-cash payment method.")
        return attrs

    @staticmethod
    def get_total_amount(obj):
        return obj.total_amount

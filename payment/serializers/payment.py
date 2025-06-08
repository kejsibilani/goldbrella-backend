from payments import get_payment_model
from rest_framework import serializers


BookingPayment = get_payment_model()
class BookingPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingPayment
        fields = (
            "id", "variant", "status", "total", "currency",
            "description", "billing_email", "created",
        )
        read_only_fields = ("status",)

from rest_framework import serializers
from payment.models import BookingPayment

class BookingPaymentSerializer(serializers.ModelSerializer):
    """
    Serializer for BookingPayment (subclass of BasePayment).
    Exposes all fields, including inherited BasePayment fields:
      - id, booking (FK)
      - variant, description, total, tax, currency, delivery
      - billing_* fields, customer_ip_address, status, etc.
      - created, modified (read-only)
    """
    class Meta:
        model = BookingPayment
        fields = '__all__'
        read_only_fields = (
            'status', 'captured_amount', 'message'
        )

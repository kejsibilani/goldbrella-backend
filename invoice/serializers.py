from rest_framework import serializers

from booking.serializers.inventory import BookedInventorySerializer
from booking.serializers.sunbed import BookingSunbedSerializer
from invoice.models import BookingInvoice


class BookingInvoiceSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField(read_only=True)
    invoice_items = serializers.SerializerMethodField(read_only=True)
    payment_method = serializers.SerializerMethodField(read_only=True)
    total_amount = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = BookingInvoice
        fields = '__all__'
        read_only_fields = (
            'invoice_number', 'booking',
            'status', 'paid_amount'
        )

    @staticmethod
    def get_invoice_items(instance):
        sunbeds = BookingSunbedSerializer(instance.booking.sunbeds.all(), many=True).data
        inventory = BookedInventorySerializer(instance.booking.inventory.all(), many=True).data
        return {
            'sunbeds': sunbeds,
            'inventory': inventory
        }

    @staticmethod
    def get_total_amount(instance):
        return instance.total_amount

    @staticmethod
    def get_payment_method(instance):
        return instance.payment_method

    @staticmethod
    def get_id(instance):
        return instance.id

from rest_framework import serializers

from invoice.models import BookingInvoice


class BookingInvoiceSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()

    class Meta:
        model = BookingInvoice
        fields = ('id', 'invoice_number', 'status')

    @staticmethod
    def get_id(instance):
        return instance.id

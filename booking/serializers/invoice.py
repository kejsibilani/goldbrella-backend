from rest_framework import serializers

from invoice.models import BookingInvoice


class BookingInvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingInvoice
        fields = ('id', 'invoice_number', 'status')

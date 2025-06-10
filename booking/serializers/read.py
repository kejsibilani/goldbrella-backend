from rest_framework import serializers

from beach.models import Beach
from booking.models import Booking
from booking.serializers.inventory import BookedInventorySerializer
from booking.serializers.invoice import BookingInvoiceSerializer
from helpers.fkeys.user import UserPrimaryKeyRelatedField
from location.models import Location
from sunbed.serializers import SunbedSerializer


class BookingLocationReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class BookingBeachReadSerializer(serializers.ModelSerializer):
    location = BookingLocationReadSerializer(read_only=True)

    class Meta:
        model = Beach
        exclude = ('facilities', 'rules')


class BookingReadSerializer(serializers.ModelSerializer):
    invoice = BookingInvoiceSerializer(read_only=True)
    beach = BookingBeachReadSerializer(read_only=True)
    sunbeds = SunbedSerializer(read_only=True, many=True)
    inventory = BookedInventorySerializer(read_only=True, many=True)
    user = UserPrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Booking
        fields = "__all__"

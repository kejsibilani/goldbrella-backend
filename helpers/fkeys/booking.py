from rest_framework import serializers

from booking.models import Booking


class BookingPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        return Booking.objects.filter(
            user=self.context['request'].user
        )

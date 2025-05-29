from django.utils.timezone import localdate
from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers

from booking.models import Booking
from booking.serializers.inventory import BookedInventorySerializer
from helpers.fkeys.sunbed import SunbedPrimaryKeyRelatedField
from helpers.fkeys.user import UserPrimaryKeyRelatedField


class BookingSerializer(WritableNestedModelSerializer):
    sunbeds = SunbedPrimaryKeyRelatedField(many=True)
    inventory = BookedInventorySerializer()
    user = UserPrimaryKeyRelatedField()

    class Meta:
        model = Booking
        fields = "__all__"
        read_only_field = ('status', 'booked_by')

    def validate(self, attrs):
        errors = []

        # validate booking date
        booking_date = attrs.get("booking_date", getattr(self.instance, 'booking_date', None))
        if booking_date < localdate():
            raise serializers.ValidationError(
                {"booking_date": "Booking date cannot be in the past"}
            )

        # validate sunbeds to guest count
        sunbeds = attrs.get("sunbeds", self.instance.sunbeds.all() if self.instance else [])
        guest_count = attrs.get("guest_count", getattr(self.instance, 'guest_count', None))
        if (guest_count or sunbeds) and guest_count != len(sunbeds):
            raise serializers.ValidationError(
                {"sunbeds": "Number of selected sunbeds must be equal to the number of guest"}
            )

        # beach validation on sunbeds
        beach = attrs.get("beach", getattr(self.instance, 'beach', None))
        for sunbed in sunbeds:
            try:
                if sunbed.zone.beach.pk != beach.pk: raise serializers.ValidationError(
                    {'sunbeds': f"Sunbed {sunbed.pk} not found in beach {beach.pk}"}
                )
            except serializers.ValidationError as ve:
                errors.append(ve.detail)
                continue

            try:
                if not sunbed.check_availability(
                    booking_date=booking_date,
                    booking=self.instance
                ): raise serializers.ValidationError(
                    {'sunbeds': f"Sunbed {sunbed.pk} is already booked for {booking_date}"}
                )
            except serializers.ValidationError as ve:
                errors.append(ve.detail)

        # beach validation on sunbeds
        inventory = attrs.get("inventory", self.instance.inventory.all() if self.instance else [])
        for item in inventory:
            try:
                if item.beach.pk != beach.pk: raise serializers.ValidationError(
                    {'inventory_items': f"Inventory item {item.pk} not found in beach {beach.pk}"}
                )
            except serializers.ValidationError as ve:
                errors.append(ve.detail)
                continue

        if errors:
            raise serializers.ValidationError({'detail': errors})
        return attrs

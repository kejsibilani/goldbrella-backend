from django.utils.timezone import localdate
from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers

from booking.models import Booking
from booking.serializers.inventory import BookedInventorySerializer
from helpers.fkeys.sunbed import SunbedPrimaryKeyRelatedField
from helpers.fkeys.user import UserPrimaryKeyRelatedField


class BookingSerializer(WritableNestedModelSerializer):
    inventory = BookedInventorySerializer(required=False, many=True)
    sunbeds = SunbedPrimaryKeyRelatedField(many=True)
    user = UserPrimaryKeyRelatedField()

    class Meta:
        model = Booking
        exclude = ('is_anonymous',)
        read_only_field = ('status', 'booked_by')

    def validate(self, attrs):
        errors = []

        # validate booking date
        booking_date = attrs.get("booking_date", getattr(self.instance, 'booking_date', None))
        if booking_date < localdate():
            raise serializers.ValidationError(
                {"booking_date": "Booking date cannot be in the past"}
            )

        # beach validation on sunbeds
        sunbeds = attrs.get("sunbeds", self.instance.sunbeds.all() if self.instance else [])
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

        inventory = attrs.get("inventory", self.instance.inventory.all() if self.instance else [])
        for item in inventory:
            if isinstance(item, dict):
                try:
                    if getattr(item.get('beach'), 'pk', None) != beach.pk: raise serializers.ValidationError(
                        {'inventory_items': f"Inventory item {getattr(item.get('inventory_item'), 'pk')} not found in beach {beach.pk}"}
                    )
                except serializers.ValidationError as ve:
                    errors.append(ve.detail)
            else:
                try:
                    if item.beach.pk != beach.pk: raise serializers.ValidationError(
                        {'inventory_items': f"Inventory item {item.inventory_item.pk} not found in beach {beach.pk}"}
                    )
                except serializers.ValidationError as ve:
                    errors.append(ve.detail)

        if errors:
            raise serializers.ValidationError({'detail': errors})
        return attrs

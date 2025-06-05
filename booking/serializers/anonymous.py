from django.utils.timezone import localdate
from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers

from booking.models import Booking
from booking.serializers import BookedInventorySerializer
from booking.serializers.user import BookingUserSerializer
from helpers.fkeys.sunbed import SunbedPrimaryKeyRelatedField
from helpers.fkeys.user import UserPrimaryKeyRelatedField
from helpers.short_func import nested_getattr


class AnonymousBookingReadSerializer(serializers.ModelSerializer):
    inventory = BookedInventorySerializer(read_only=True, many=True)
    sunbeds = SunbedPrimaryKeyRelatedField(read_only=True, many=True)
    booked_by = serializers.StringRelatedField(read_only=True)
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Booking
        exclude = ('is_anonymous',)
        read_only_field = ('status', 'beach', 'booking_date', 'note')


class AnonymousBookingSerializer(WritableNestedModelSerializer):
    inventory = BookedInventorySerializer(required=False, many=True)
    sunbeds = SunbedPrimaryKeyRelatedField(many=True)
    booked_by = BookingUserSerializer(required=False)
    user = BookingUserSerializer()

    class Meta:
        model = Booking
        exclude = ('is_anonymous',)
        read_only_field = ('status',)

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

        # beach validation on inventory
        inventory = attrs.get("inventory", self.instance.inventory.all() if self.instance else [])
        for item in inventory:
            if isinstance(item, dict):
                try:
                    if nested_getattr(item.get('inventory_item'), 'beach', 'pk') != beach.pk: raise serializers.ValidationError(
                        {
                            'inventory_items': f"Inventory item {getattr(item.get('inventory_item'), 'pk')}"
                                               f" not found in beach {beach.pk}"
                        }
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

        #  update booked by to user
        self.initial_data['booked_by'] = self.initial_data.get('user')
        attrs['booked_by'] = attrs['user']
        return attrs

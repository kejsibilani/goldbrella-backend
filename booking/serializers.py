from django.utils.timezone import localdate
from rest_framework import serializers

from booking.models import Booking, SunbedBooking, InventoryBooking
from helpers.fkeys.user import UserForeignKey
from inventory.models import InventoryItem
from sunbed.models import Sunbed


class BookingSerializer(serializers.ModelSerializer):
    inventory_items = serializers.PrimaryKeyRelatedField(
        queryset=InventoryItem.objects.all(), many=True
    )
    sunbeds = serializers.PrimaryKeyRelatedField(
        queryset=Sunbed.objects.all(), many=True
    )
    user = UserForeignKey()

    class Meta:
        model = Booking
        fields = "__all__"
        read_only_field = ('status', 'booked_by')

    @staticmethod
    def validate_inventory_items(value):
        quantity_based_dict = {}
        for item in value:
            quantity_based_dict[item] = quantity_based_dict.get(item.pk, 0) + 1
        return quantity_based_dict

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
                if sunbed.beach.pk != beach.pk: raise serializers.ValidationError(
                    {'sunbeds': f"Sunbed {sunbed.pk} not found in beach {beach.pk}"}
                )
            except serializers.ValidationError as ve:
                errors.append(ve.detail)
                continue

            is_booked = SunbedBooking.objects.filter(
                booking__status__in=['confirmed', 'pending'],
                booking__booking_date=booking_date,
                sunbed=sunbed.pk,
            ).exclude(booking=self.instance).exists()
            try:
                if is_booked: raise serializers.ValidationError(
                    {'sunbeds': f"Sunbed {sunbed.pk} is already booked for {booking_date}"}
                )
            except serializers.ValidationError as ve:
                errors.append(ve.detail)

        # beach validation on sunbeds
        inventory_items = attrs.get("inventory_items", self.instance.inventory_items.all() if self.instance else [])
        for item in inventory_items:
            try:
                if item.beach.pk != beach.pk: raise serializers.ValidationError(
                    {'inventory_items': f"Inventory item {item.pk} not found in beach {beach.pk}"}
                )
            except serializers.ValidationError as ve:
                errors.append(ve.detail)
                continue

            try:
                quantity = (
                    inventory_items[item]
                    if isinstance(inventory_items, dict) else
                    self.instance.inventory_bookings.filter(
                        inventory_item=item
                    ).values_list('inventory_quantity', flat=True).first()
                )
                previous_quantity = self.instance.inventory_bookings.filter(
                    inventory_item=item
                ).values_list('inventory_quantity', flat=True).first() if self.instance else 0
                is_booked = not item.check_available(booking_date, (quantity - previous_quantity))
                if is_booked: raise serializers.ValidationError(
                    {'inventory_items': f"Inventory item {item.pk} is booked for {booking_date}"}
                )
            except serializers.ValidationError as ve:
                errors.append(ve.detail)

        if errors:
            raise serializers.ValidationError({'detail': errors})
        return attrs

    def create(self, validated_data):
        inventory_items = validated_data.pop('inventory_items', {})
        booking = super().create(validated_data)
        for item in inventory_items:
            booking.inventory_items.add(
                item, through_defaults={'inventory_quantity': inventory_items[item]}
            )
        return booking

    def update(self, instance, validated_data):
        inventory_items = validated_data.pop('inventory_items', {})
        booking = super().update(instance, validated_data)
        if inventory_items:
            booking.inventory_items.clear()
            for item in inventory_items:
                booking.inventory_items.add(
                    item, through_defaults={'inventory_quantity': inventory_items[item]}
                )
        return booking

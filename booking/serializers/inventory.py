from rest_framework import serializers

from booking.models import BookedInventory


class BookedInventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BookedInventory
        fields = '__all__'
        extra_kwargs = {
            'booking': {'required': False},
        }

    def validate(self, attrs):
        on_demand = attrs.get("on_demand", getattr(self.instance, 'on_demand', None))
        quantity = attrs.get("quantity", getattr(self.instance, 'quantity', None))
        inventory_item = attrs.get("inventory_item", getattr(self.instance, 'inventory_item', None))
        booking = attrs.get("booking", getattr(self.instance, 'booking', None))
        booking_date = getattr(booking, 'booking_date', None)

        # beach validation on inventory
        if booking and booking.beach.pk != inventory_item.beach.pk: raise serializers.ValidationError(
            {'inventory_items': f"Inventory item {inventory_item.pk} not found in beach {booking.beach.pk}"}
        )

        if inventory_item and not inventory_item.check_availability(
            pk=getattr(self.instance, 'pk', None),
            booking_date=booking_date,
            on_demand=on_demand,
            quantity=quantity,
        ):
            raise serializers.ValidationError(
                {'inventory_items': f"Inventory item {inventory_item.pk} is booked for {booking_date}"}
            )

        return attrs

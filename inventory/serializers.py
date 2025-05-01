from rest_framework import serializers

from inventory.models import InventoryItem


class InventoryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryItem
        fields = "__all__"


class InventoryQuerySerializer(serializers.Serializer):
    only_available = serializers.BooleanField(default=False)
    booking_date = serializers.DateField(required=False)

    def validate(self, data):
        only_available = data.get("only_available")
        booking_date = data.get("booking_date")

        if only_available and not booking_date:
            raise serializers.ValidationError(
                {'detail': '`only_available` should be specified with `booking_date`'}
            )
        return data


class AvailableInventoryItemSerializer(serializers.ModelSerializer):
    available = serializers.SerializerMethodField()

    class Meta:
        model = InventoryItem
        fields = '__all__'
        read_only_fields = (
            'name', 'price', 'discount_percentage', 'beach'
        )

    def get_available(self, obj):
        booking_date = self.context.get('booking_date', None)

        if booking_date is None:
            return None
        return obj.get_available(booking_date)

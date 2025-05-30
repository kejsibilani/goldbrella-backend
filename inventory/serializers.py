from rest_framework import serializers

from helpers.validators import CaseInsensitiveUniqueTogetherValidator
from inventory.models import InventoryItem


class InventoryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryItem
        fields = "__all__"
        validators = [
            CaseInsensitiveUniqueTogetherValidator(
                queryset=InventoryItem.objects.all(),
                fields=("beach", "name"),
            )
        ]
        extra_kwargs = {
            'price': {'min_value': 0.0},
            'quantity': {'min_value': 0},
        }


class AvailableInventoryItemSerializer(serializers.ModelSerializer):
    available = serializers.SerializerMethodField()

    class Meta:
        model = InventoryItem
        fields = (
            'id', 'name', 'reusable_item', 'price', 'available',
            'beach', 'created', 'updated'
        )

    def get_available(self, obj):
        booking_date = self.context.get('booking_date', None)

        if booking_date is None:
            return None
        return obj.get_available(booking_date)


class InventoryQuerySerializer(serializers.Serializer):
    booking_date = serializers.DateField(required=False)

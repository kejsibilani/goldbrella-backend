from rest_framework import serializers

from inventory.models import Inventory, InventoryItem


class InventorySerializer(serializers.ModelSerializer):
    quantity = serializers.IntegerField()
    identities = serializers.ListField(
        child=serializers.CharField()
    )

    class Meta:
        model = Inventory
        fields = "__all__"

    def validate(self, data):
        quantity = data.pop('quantity', getattr(self.instance, 'quantity', None))

        default_identities = []
        if self.instance: default_identities = self.instance.items.values_list('identity', flat=True)
        identities = data.get('identities', default_identities)

        if quantity < 0:
            raise serializers.ValidationError("At least one item must be in stock.")
        if quantity != len(identities):
            raise serializers.ValidationError("One identity per inventory item must be provided.")
        return data

    def create(self, validated_data):
        # extract quantity from data
        identities = validated_data.pop('identities', [])
        # generate the inventory object
        instance = super().create(validated_data)
        # create items for the inventory
        for identity in identities:
            _, c = InventoryItem.objects.get_or_create(
                inventory=instance,
                identity=identity
            )
            if not c:
                raise serializers.ValidationError("Item with same identity already exists.")
        return instance

    def update(self, instance, validated_data):
        # remove all existing identities
        instance.identites.delete()
        # extract quantity from data
        identities = validated_data.pop('identities', [])
        # generate the inventory object
        instance = super().update(instance, validated_data)
        # create items for the inventory
        for identity in identities:
            _, c = InventoryItem.objects.get_or_create(
                inventory=instance,
                identity=identity
            )
            if not c:
                raise serializers.ValidationError("Item with same identity already exists.")
        return instance

    def to_representation(self, instance):
        represent = super().to_representation(instance)
        represent.setdefault('quantity', instance.quantity)
        return represent

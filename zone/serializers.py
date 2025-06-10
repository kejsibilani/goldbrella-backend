from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from helpers.short_func import nested_getattr
from zone.models import Zone


class ZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zone
        fields = "__all__"
        read_only_fields=('location', 'beach')
        validators = [
            UniqueTogetherValidator(
                queryset=Zone.objects.all(),
                fields=('location', 'beach')
            )
        ]


class ZoneListSerializer(serializers.ModelSerializer):
    beach = serializers.StringRelatedField(read_only=True)
    supervisor = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Zone
        fields = "__all__"

    @staticmethod
    def get_supervisor(obj):
        if obj.supervisor is None:
            return None
        return {
            'id': nested_getattr(obj, 'supervisor', 'id'),
            'email': nested_getattr(obj, 'supervisor', 'email'),
            'first_name': nested_getattr(obj, 'supervisor', 'first_name'),
            'last_name': nested_getattr(obj, 'supervisor', 'last_name')
        }

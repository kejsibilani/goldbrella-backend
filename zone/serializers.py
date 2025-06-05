from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from zone.models import Zone


class ZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zone
        fields = "__all__"
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

    def get_supervisor(self, obj):
        return {
            'id': obj.supervisor.id,
            'email': obj.supervisor.email,
            'first_name': obj.supervisor.first_name,
            'last_name': obj.supervisor.last_name
        }

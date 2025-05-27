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

from rest_framework import serializers

from location.models import Location
from helpers.validators import CaseInsensitiveUniqueTogetherValidator


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"
        validators = [
            CaseInsensitiveUniqueTogetherValidator(
                queryset=Location.objects.all(),
                fields=('city', 'country')
            )
        ]

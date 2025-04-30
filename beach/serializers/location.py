from rest_framework import serializers

from beach.models import BeachLocation
from helpers.validators import CaseInsensitiveUniqueTogetherValidator


class BeachLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = BeachLocation
        fields = "__all__"
        validators = [
            CaseInsensitiveUniqueTogetherValidator(
                queryset=BeachLocation.objects.all(),
                fields=('city', 'country')
            )
        ]

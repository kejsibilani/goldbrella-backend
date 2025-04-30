from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from beach.models import BeachOpeningHour


class BeachOpeningHourSerializer(serializers.ModelSerializer):
    class Meta:
        model = BeachOpeningHour
        fields = "__all__"
        validators = [
            UniqueTogetherValidator(
                queryset=BeachOpeningHour.objects.all(),
                fields=('season', 'weekday')
            )
        ]

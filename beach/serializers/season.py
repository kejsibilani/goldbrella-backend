from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from beach.models import BeachOpeningSeason


class BeachOpeningSeasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = BeachOpeningSeason
        fields = "__all__"
        validators = [
            UniqueTogetherValidator(
                queryset=BeachOpeningSeason.objects.all(),
                fields=('beach', 'opening_date', 'closing_date')
            )
        ]

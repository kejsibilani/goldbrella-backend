from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from beach.models import BeachImage


class BeachImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BeachImage
        fields = "__all__"
        validators = [
            UniqueTogetherValidator(
                queryset=BeachImage.objects.all(),
                fields=('beach', 'link')
            )
        ]

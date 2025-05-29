from rest_framework import serializers

from sunbed.models import Sunbed


class SunbedPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    queryset = Sunbed.objects.all()

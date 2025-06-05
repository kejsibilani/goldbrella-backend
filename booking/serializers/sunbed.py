from rest_framework import serializers

from sunbed.models import Sunbed


class BookingSunbedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sunbed
        fields = '__all__'

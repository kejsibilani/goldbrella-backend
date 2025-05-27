from rest_framework import serializers

from beach.models import BeachImage


class BeachImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BeachImage
        fields = "__all__"

from rest_framework import serializers

from beach.models import Beach
from helpers.short_func import nested_getattr


class BeachSerializer(serializers.ModelSerializer):
    thumbnail = serializers.SerializerMethodField()

    class Meta:
        model = Beach
        fields = "__all__"

    @staticmethod
    def get_thumbnail(instance):
        return nested_getattr(instance.images.first(), 'image', 'url')

from rest_framework import serializers

from beach.models import Beach


class BeachSerializer(serializers.ModelSerializer):
    thumbnail = serializers.SerializerMethodField()

    class Meta:
        model = Beach
        fields = "__all__"

    @staticmethod
    def get_thumbnail(instance):
        return instance.images.first().image.url

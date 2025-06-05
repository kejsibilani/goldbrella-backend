from rest_framework import serializers

from beach.models import Beach
from beach.serializers.images import BeachImageSerializer
from beach.serializers.openings import BeachOpeningHourSerializer
from beach.serializers.season import BeachOpeningSeasonSerializer
from helpers.short_func import nested_getattr
from location.serializers import LocationSerializer
from services.serializers import FacilitySerializer
from services.serializers import RuleSerializer
from sunbed.models import Sunbed


class BeachReadSerializer(serializers.ModelSerializer):
    sunbed_count = serializers.SerializerMethodField()
    lowest_sunbed_price = serializers.SerializerMethodField()
    location = LocationSerializer(read_only=True)
    seasons = BeachOpeningSeasonSerializer(many=True, read_only=True)
    images = BeachImageSerializer(many=True, read_only=True)
    opening_hours = BeachOpeningHourSerializer(many=True, read_only=True)
    facilities = FacilitySerializer(many=True, read_only=True)
    rules = RuleSerializer(many=True, read_only=True)

    class Meta:
        model = Beach
        fields = (
            'id', 'title', 'description', 'latitude', 'longitude', 'sunbed_count',
            'lowest_sunbed_price', 'location', 'seasons', 'opening_hours', 'facilities',
            'rules', 'images', 'created', 'updated'
        )
        read_only_fields = (
            'title', 'description', 'latitude', 'longitude'
        )

    @staticmethod
    def get_sunbed_count(instance):
        return Sunbed.objects.filter(zone__beach=instance).count()

    @staticmethod
    def get_lowest_sunbed_price(instance):
        return getattr(Sunbed.objects.filter(zone__beach=instance).order_by('price').first(), 'price')


class BeachListReadSerializer(serializers.ModelSerializer):
    thumbnail = serializers.SerializerMethodField()
    facilities = serializers.StringRelatedField(many=True, read_only=True)
    rules = serializers.StringRelatedField(many=True, read_only=True)
    location = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Beach
        fields = (
            'id', 'title', 'description', 'thumbnail', 'location',
            'facilities', 'rules', 'created', 'updated'
        )
        read_only_fields = ('title', 'description')

    def get_thumbnail(self, instance):
        request = self.context.get('request')
        if request:
            relative_url = nested_getattr(instance.images.first(), 'image', 'url')
            return request.build_absolute_uri(relative_url)
        return None

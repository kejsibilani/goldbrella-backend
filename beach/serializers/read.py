from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from beach.models import Beach
from beach.models import BeachLocation
from beach.models import BeachOpeningHour
from beach.models import BeachOpeningSeason
from helpers.short_func import combine_hours


class BeachLocationReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = BeachLocation
        fields = ('city', 'country')
        read_only_fields = ('city', 'country')


class BeachOpeningSeasonReadSerializer(serializers.ModelSerializer):
    start_month = serializers.SerializerMethodField()
    end_month = serializers.SerializerMethodField()

    class Meta:
        model = BeachOpeningSeason
        fields = ('start_month', 'end_month')

    @staticmethod
    def get_start_month(instance):
        return instance.opening_date.strftime("%B")

    @staticmethod
    def get_end_month(instance):
        return instance.closing_date.strftime("%B")


class BeachOpeningHourReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = BeachOpeningHour
        fields = ('day', 'opening_time', 'closing_time')
        read_only_fields = ('day', 'opening_time', 'closing_time')


class BeachReadSerializer(serializers.ModelSerializer):
    facilities = serializers.StringRelatedField(many=True, read_only=True)
    rules = serializers.StringRelatedField(many=True, read_only=True)
    images = serializers.StringRelatedField(many=True, read_only=True)
    location = BeachLocationReadSerializer(read_only=True)
    season = BeachOpeningSeasonReadSerializer(read_only=True)
    opening_hours = serializers.SerializerMethodField()
    sunbed_count = serializers.SerializerMethodField()
    lowest_sunbed_price = serializers.SerializerMethodField()

    class Meta:
        model = Beach
        fields = (
            'id', 'title', 'description', 'latitude', 'longitude', 'sunbed_count',
            'lowest_sunbed_price', 'location', 'season', 'opening_hours', 'facilities',
            'rules', 'images', 'created', 'updated'
        )
        read_only_fields = (
            'title', 'description', 'latitude', 'longitude'
        )
        validators = [
            UniqueTogetherValidator(
                queryset=Beach.objects.all(),
                fields=('latitude', 'longitude', 'location')
            )
        ]

    @staticmethod
    def get_sunbed_count(instance):
        return instance.sunbeds.count()

    @staticmethod
    def get_lowest_sunbed_price(instance):
        return instance.sunbeds.order_by('price').first().price

    @staticmethod
    def get_opening_hours(instance):
        instances = instance.season.opening_hours.values('weekday', 'opening_time', 'closing_time')
        return combine_hours(instances)


class BeachListReadSerializer(serializers.ModelSerializer):
    thumbnail = serializers.SerializerMethodField()
    facilities = serializers.StringRelatedField(many=True, read_only=True)
    rules = serializers.StringRelatedField(many=True, read_only=True)
    location = BeachLocationReadSerializer(read_only=True)

    class Meta:
        model = Beach
        fields = (
            'id', 'title', 'description', 'thumbnail', 'location',
            'facilities', 'rules', 'created', 'updated'
        )
        read_only_fields = ('title', 'description')

    @staticmethod
    def get_thumbnail(instance):
        return instance.images.first().link

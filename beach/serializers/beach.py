from django.forms import ImageField
from rest_framework import serializers
from django_filters.filters import CharFilter as CharFieldFilter

from beach.models import Beach, Menu, MenuImage
from helpers.short_func import nested_getattr


class MenuImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuImage
        fields = ['id', 'image', 'created']

class MenuSerializer(serializers.ModelSerializer):
    images = MenuImageSerializer(many=True, read_only=True)
    class Meta:
        model = Menu
        fields = ['id', 'title', 'description', 'images']

class BeachSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)
    thumbnail = serializers.SerializerMethodField()
    menu = MenuSerializer(read_only=True)

    class Meta:
        model = Beach
        fields = [
            'id', 'title', 'description', 'location', 'latitude', 'longitude',
            'image', 'thumbnail', 'menu', 'total_sunbeds', 'rows', 'columns'
        ]
        filter_overrides = {
            ImageField: {
                'filter_class': CharFieldFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains'
                },
            }
        }

    @staticmethod
    def get_thumbnail(instance):
        return nested_getattr(instance.images.first(), 'image', 'url')

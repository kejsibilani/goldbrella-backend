from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers


class ContentTypePrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        return ContentType.objects.filter(
            model__in=[
                'inventoryitem',
                'sunbed',
            ]
        )

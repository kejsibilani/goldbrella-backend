from rest_framework import viewsets

from helpers.pagination import GenericPagination
from sunbed.filters import SunbedFilterSet
from sunbed.models import Sunbed
from sunbed.serializers import SunbedSerializer


class SunbedViewSet(viewsets.ModelViewSet):
    pagination_class = GenericPagination
    serializer_class = SunbedSerializer
    filterset_class = SunbedFilterSet
    queryset = Sunbed.objects.all()

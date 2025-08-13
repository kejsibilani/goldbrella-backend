from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny

from location.filters import LocationFilterSet
from location.models import Location
from location.serializers import LocationSerializer
from helpers.pagination import GenericPagination


class LocationViewSet(viewsets.ModelViewSet):
    filter_backends = [DjangoFilterBackend, SearchFilter]
    serializer_class = LocationSerializer
    filterset_class = LocationFilterSet
    queryset = Location.objects.all().order_by('priority', 'city')
    pagination_class = GenericPagination
    search_fields = ['city', 'country']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return super().get_permissions()

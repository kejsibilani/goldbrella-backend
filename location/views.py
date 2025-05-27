from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import SearchFilter

from location.filters import LocationFilterSet
from location.models import Location
from location.serializers import LocationSerializer
from helpers.pagination import GenericPagination


class LocationViewSet(viewsets.ModelViewSet):
    filter_backends = [DjangoFilterBackend, SearchFilter]
    serializer_class = LocationSerializer
    filterset_class = LocationFilterSet
    queryset = Location.objects.all()
    pagination_class = GenericPagination
    search_fields = ['city', 'country']

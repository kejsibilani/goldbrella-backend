from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import SearchFilter

from beach.filters import BeachFilterSet
from beach.models import Beach
from beach.serializers import BeachSerializer, BeachReadSerializer, BeachListReadSerializer
from helpers.pagination import GenericPagination


class BeachViewSet(viewsets.ModelViewSet):
    filter_backends = [DjangoFilterBackend, SearchFilter]
    pagination_class = GenericPagination
    filterset_class = BeachFilterSet
    queryset = Beach.objects.all()
    search_fields = [
        'title', 'latitude', 'longitude',
        'location__city', 'location__country'
    ]

    def get_serializer_class(self):
        if self.action == 'list':
            return BeachListReadSerializer
        elif self.action == 'retrieve':
            return BeachReadSerializer
        return BeachSerializer

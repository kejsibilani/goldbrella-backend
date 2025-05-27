from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.response import Response

from beach.models import Beach
from helpers.pagination import GenericPagination
from zone.filters import ZoneFilterSet
from zone.models import Zone
from zone.serializers import ZoneSerializer


# Create your views here.
class ZoneViewSet(viewsets.ModelViewSet):
    filter_backends = [DjangoFilterBackend, SearchFilter]
    pagination_class = GenericPagination
    serializer_class = ZoneSerializer
    filterset_class = ZoneFilterSet
    queryset = Zone.objects.all()
    search_fields = ['location', 'beach__title']


class BeachZoneListViewSet(viewsets.GenericViewSet):
    pagination_class = GenericPagination
    serializer_class = ZoneSerializer
    queryset = Beach.objects.all()

    @action(detail=True, methods=['get'], url_path='zones')
    def zones(self, request, *args, **kwargs):
        # fetch instance
        beach = self.get_object()
        # fetch season for the beach
        queryset = beach.zones.all()
        # filter the queryset
        queryset = self.filter_queryset(queryset)
        # paginate the response
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

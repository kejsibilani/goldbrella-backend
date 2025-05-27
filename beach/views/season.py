from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from beach.filters import BeachOpeningSeasonFilterSet
from beach.models import Beach
from beach.models import BeachOpeningSeason
from beach.serializers import BeachOpeningSeasonSerializer
from helpers.pagination import GenericPagination


class BeachOpeningSeasonViewSet(viewsets.ModelViewSet):
    serializer_class = BeachOpeningSeasonSerializer
    filterset_class = BeachOpeningSeasonFilterSet
    queryset = BeachOpeningSeason.objects.all()
    pagination_class = GenericPagination


class BeachOpeningSeasonListViewSet(viewsets.GenericViewSet):
    serializer_class = BeachOpeningSeasonSerializer
    pagination_class = GenericPagination
    queryset = Beach.objects.all()

    @action(detail=True, methods=['get'], url_path='opening-seasons')
    def open_seasons(self, request, *args, **kwargs):
        # fetch instance
        beach = self.get_object()
        # fetch season for the beach
        queryset = beach.seasons.all()
        # filter the queryset
        queryset = self.filter_queryset(queryset)
        # paginate the response
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

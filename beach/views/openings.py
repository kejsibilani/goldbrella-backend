from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.mixins import UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from beach.filters import BeachOpeningHourFilterSet
from beach.models import Beach
from beach.models import BeachOpeningHour
from beach.models import BeachOpeningSeason
from beach.serializers import BeachOpeningHourSerializer
from helpers.pagination import GenericPagination


class BeachOpeningHourViewSet(ListModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = BeachOpeningHourSerializer
    filterset_class = BeachOpeningHourFilterSet
    queryset = BeachOpeningHour.objects.all()
    pagination_class = GenericPagination


class BeachSeasonOpeningHourListViewSet(GenericViewSet):
    serializer_class = BeachOpeningHourSerializer
    pagination_class = GenericPagination
    queryset = BeachOpeningSeason.objects.all()

    @action(detail=True, methods=['get'], url_path='opening-hours')
    def open_hours(self, request, *args, **kwargs):
        # fetch instance
        season = self.get_object()
        # fetch all hours for the season
        queryset = season.opening_hours.all()
        # filter the queryset
        queryset = self.filter_queryset(queryset)
        # paginate the response
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class BeachOpeningHourListViewSet(GenericViewSet):
    serializer_class = BeachOpeningHourSerializer
    pagination_class = GenericPagination
    queryset = Beach.objects.all()

    @action(detail=True, methods=['get'], url_path='opening-hours')
    def open_hours(self, request, *args, **kwargs):
        # fetch instance
        beach = self.get_object()
        # fetch all hours for the beach
        queryset = BeachOpeningHour.objects.filter(season__beach=beach)
        # filter the queryset
        queryset = self.filter_queryset(queryset)
        # paginate the response
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

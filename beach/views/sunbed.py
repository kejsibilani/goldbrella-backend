from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from beach.models import Beach
from helpers.pagination import GenericPagination
from sunbed.filters import SunbedFilterSet
from sunbed.serializers import AvailableSunbedSerializer


class BeachSunbedAvailabilityViewSet(GenericViewSet):
    serializer_class = AvailableSunbedSerializer
    pagination_class = GenericPagination
    filterset_class = SunbedFilterSet
    queryset = Beach.objects.all()

    @action(detail=True, methods=['get'], url_path='sunbeds')
    def sunbeds(self, request, *args, **kwargs):
        # fetch default serializer context
        context = self.get_serializer_context()
        booked_sunbeds_id = None

        # fetch instance
        beach = self.get_object()
        # fetch all sunbeds for the beach
        queryset = beach.sunbeds.all()

        # filter queryset
        queryset = self.filter_queryset(queryset)
        # paginate queryset
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True, context=context)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True, context=context)
        return Response(serializer.data)

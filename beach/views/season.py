from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from beach.filters import BeachOpeningSeasonFilterSet
from beach.models import BeachOpeningSeason, Beach
from beach.serializers import BeachOpeningSeasonSerializer
from helpers.pagination import GenericPagination


class BeachOpeningSeasonViewSet(ListModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = BeachOpeningSeasonSerializer
    filterset_class = BeachOpeningSeasonFilterSet
    queryset = BeachOpeningSeason.objects.all()
    pagination_class = GenericPagination


class BeachOpeningSeasonReadViewSet(GenericViewSet):
    serializer_class = BeachOpeningSeasonSerializer
    queryset = Beach.objects.all()

    @action(detail=True, methods=['get'], url_path='opening-seasons')
    def open_season(self, request, *args, **kwargs):
        # fetch instance
        beach = self.get_object()
        # fetch season for the beach
        instance = getattr(beach, 'season', None)
        # raise Error if no instance found
        if not instance:
            raise ValidationError({'detail': 'No season found for this beach.'})
        # searialize and return instance
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

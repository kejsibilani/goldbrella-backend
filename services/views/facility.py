from rest_framework import viewsets

from helpers.pagination import GenericPagination
from services.filters import FacilityFilterSet
from services.models import Facility
from services.serializers import FacilitySerializer


class FacilityViewSet(viewsets.ModelViewSet):
    serializer_class = FacilitySerializer
    pagination_class = GenericPagination
    filterset_class = FacilityFilterSet
    queryset = Facility.objects.all()

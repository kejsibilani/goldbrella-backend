from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import SearchFilter

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

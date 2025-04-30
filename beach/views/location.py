from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import SearchFilter

from beach.filters import BeachLocationFilterSet
from beach.models import BeachLocation
from beach.serializers import BeachLocationSerializer
from helpers.pagination import GenericPagination


class BeachLocationViewSet(viewsets.ModelViewSet):
    filter_backends = [DjangoFilterBackend, SearchFilter]
    serializer_class = BeachLocationSerializer
    filterset_class = BeachLocationFilterSet
    queryset = BeachLocation.objects.all()
    pagination_class = GenericPagination
    search_fields = ['city', 'country']

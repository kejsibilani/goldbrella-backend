from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet

from helpers.pagination import GenericPagination
from inventory.filters import InventoryItemFilterSet
from inventory.models import InventoryItem
from inventory.serializers import InventoryItemSerializer


# Create your views here.
class InventoryItemViewSet(viewsets.ModelViewSet):
    filter_backends = [DjangoFilterBackend, SearchFilter]
    serializer_class = InventoryItemSerializer
    filterset_class = InventoryItemFilterSet
    pagination_class = GenericPagination
    queryset = InventoryItem.objects.all()
    search_fields = ['name', 'identity']

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import SearchFilter

from helpers.pagination import GenericPagination
from inventory.filters import InventoryFilterSet
from inventory.models import Inventory
from inventory.serializers import InventorySerializer


# Create your views here.
class InventoryViewSet(viewsets.ModelViewSet):
    filter_backends = [DjangoFilterBackend, SearchFilter]
    serializer_class = InventorySerializer
    filterset_class = InventoryFilterSet
    pagination_class = GenericPagination
    queryset = Inventory.objects.all()
    search_fields = ['name', 'items__identity']

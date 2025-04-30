from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from beach.models import Beach
from helpers.pagination import GenericPagination
from inventory.filters import InventoryFilterSet
from inventory.serializers import InventorySerializer


class InventoryListViewSet(GenericViewSet):
    serializer_class = InventorySerializer
    filterset_class = InventoryFilterSet
    pagination_class = GenericPagination
    queryset = Beach.objects.all()

    @action(detail=True, methods=['get'], url_path='inventory-items')
    def inventory(self, request, *args, **kwargs):
        # fetch instance
        instance = self.get_object()
        # fetch all inventory
        queryset = instance.inventory_items.all()
        # filter queryset
        queryset = self.filter_queryset(queryset)
        # paginate the response
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

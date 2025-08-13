from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny

from beach.filters import BeachFilterSet
from beach.models import Beach
from beach.serializers import BeachListReadSerializer
from beach.serializers import BeachReadSerializer
from beach.serializers import BeachSerializer
from helpers.pagination import GenericPagination
from inventory.serializers import AvailableInventoryItemSerializer
from inventory.models import InventoryItem
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status


class BeachViewSet(viewsets.ModelViewSet):
    filter_backends = [DjangoFilterBackend, SearchFilter]
    pagination_class = GenericPagination
    serializer_class = BeachSerializer
    filterset_class = BeachFilterSet

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.role == 'staff' and user.managed_beach_id:
            return Beach.objects.filter(id=user.managed_beach_id)
        return Beach.objects.all()

    search_fields = [
        'title', 'latitude', 'longitude',
        'location__city', 'location__country'
    ]

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'menu_by_code']:
            return [AllowAny()]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == 'list':
            return BeachListReadSerializer
        elif self.action == 'retrieve':
            return BeachReadSerializer
        return super().get_serializer_class()

    @action(detail=False, methods=['get'], url_path='by-code/(?P<code>[^/]+)/menu')
    def menu_by_code(self, request, code=None):
        try:
            beach = Beach.objects.get(code=code)
        except Beach.DoesNotExist:
            return Response({'detail': 'Invalid code.'}, status=status.HTTP_404_NOT_FOUND)
        # Get all inventory items for this beach (bar menu)
        items = beach.inventory_items.all()
        serializer = AvailableInventoryItemSerializer(items, many=True, context={'request': request})
        return Response(serializer.data)

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from beach.models import Beach
from booking.models import InventoryBooking
from helpers.pagination import GenericPagination
from inventory.serializers import AvailableInventoryItemSerializer, InventoryQuerySerializer


class BeachInventoryItemListViewSet(GenericViewSet):
    serializer_class = AvailableInventoryItemSerializer
    pagination_class = GenericPagination
    queryset = Beach.objects.all()

    @action(detail=True, methods=['get'], url_path='inventory-items')
    def inventory(self, request, *args, **kwargs):
        # get serializer context
        context = self.get_serializer_context()
        # fetch instance
        instance = self.get_object()
        # fetch all inventory
        queryset = instance.inventory_items.all()
        # validate query params using serializer
        query_serializer = InventoryQuerySerializer(data=request.query_params)
        query_serializer.is_valid(raise_exception=True)
        # filter queryset for booking date and availability and guest count
        only_available = query_serializer.data.get('only_available', False)
        booking_date = query_serializer.data.get('booking_date')
        name = query_serializer.data.get('name')

        # set booking date in context
        context['booking_date'] = booking_date

        if only_available and booking_date:
            queryset = queryset.exclude(
                id__in=InventoryBooking.objects.filter(
                    booking__status__in=['confirmed', 'pending'],
                    booking__booking_date=booking_date
                ).values_list('inventory_item_id', flat=True)
            )

        # filter queryset
        if name:
            queryset = queryset.filter(name__icontains=name)
        # paginate the response
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True, context=context)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True, context=context)
        return Response(serializer.data)

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from beach.models import Beach
from booking.choices import BookingStatusChoices
from booking.models import SunbedBooking
from helpers.pagination import GenericPagination
from sunbed.filters import SunbedFilterSet
from sunbed.models import Sunbed
from sunbed.serializers import AvailableSunbedSerializer
from sunbed.serializers import SunbedQuerySerializer
from sunbed.serializers import SunbedSerializer
from zone.models import Zone


class SunbedViewSet(viewsets.ModelViewSet):
    pagination_class = GenericPagination
    serializer_class = SunbedSerializer
    filterset_class = SunbedFilterSet
    queryset = Sunbed.objects.all()


class ZoneSunbedListViewSet(viewsets.GenericViewSet):
    serializer_class = AvailableSunbedSerializer
    pagination_class = GenericPagination
    queryset = Zone.objects.all()

    @action(detail=True, methods=['get'], url_path='sunbeds')
    def sunbeds(self, request, *args, **kwargs):
        # fetch default serializer context
        context = self.get_serializer_context()

        # fetch instance
        zone = self.get_object()
        # fetch all sunbeds for the zone
        queryset = zone.sunbeds.all()
        # validate query params using serializer
        query_serializer = SunbedQuerySerializer(data=request.query_params)
        query_serializer.is_valid(raise_exception=True)
        # filter queryset for booking date and availability and guest count
        only_available = query_serializer.data.get('only_available', False)
        booking_date = query_serializer.data.get('booking_date')

        # set booking date in context
        context['booking_date'] = booking_date

        if only_available and booking_date:
            queryset = queryset.exclude(
                id__in=SunbedBooking.objects.filter(
                    booking__booking_date=booking_date,
                    booking__status__in=[
                        BookingStatusChoices.PARTIAL_RESERVED.value,
                        BookingStatusChoices.CONFIRMED.value,
                        BookingStatusChoices.RESERVED.value
                    ]
                ).values_list('sunbed_id', flat=True)
            )

        # filter queryset
        queryset = self.filter_queryset(queryset)
        # paginate queryset
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, read_only=True, many=True, context=context)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, read_only=True, many=True, context=context)
        return Response(serializer.data)


class BeachSunbedListViewSet(viewsets.GenericViewSet):
    serializer_class = AvailableSunbedSerializer
    pagination_class = GenericPagination
    queryset = Beach.objects.all()

    @action(detail=True, methods=['get'], url_path='sunbeds')
    def sunbeds(self, request, *args, **kwargs):
        # fetch default serializer context
        context = self.get_serializer_context()

        # fetch instance
        beach = self.get_object()
        # fetch all sunbeds for the beach
        queryset = Sunbed.objects.filter(zone__beach=beach)
        # validate query params using serializer
        query_serializer = SunbedQuerySerializer(data=request.query_params)
        query_serializer.is_valid(raise_exception=True)
        # filter queryset for booking date and availability and guest count
        only_available = query_serializer.data.get('only_available', False)
        booking_date = query_serializer.data.get('booking_date')

        # set booking date in context
        context['booking_date'] = booking_date

        if only_available and booking_date:
            queryset = queryset.exclude(
                id__in=SunbedBooking.objects.filter(
                    booking__booking_date=booking_date,
                    booking__status__in=[
                        BookingStatusChoices.PARTIAL_RESERVED.value,
                        BookingStatusChoices.CONFIRMED.value,
                        BookingStatusChoices.RESERVED.value
                    ]
                ).values_list('sunbed_id', flat=True)
            )

        # filter queryset
        queryset = self.filter_queryset(queryset)
        # paginate queryset
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, read_only=True, many=True, context=context)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, read_only=True, many=True, context=context)
        return Response(serializer.data)

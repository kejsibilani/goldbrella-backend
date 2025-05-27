from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from beach.models import Beach
from helpers.pagination import GenericPagination
from sunbed.filters import SunbedFilterSet
from sunbed.models import Sunbed
from sunbed.models import SunbedBooking
from sunbed.serializers import AvailableSunbedSerializer
from sunbed.serializers import SunbedQuerySerializer
from sunbed.serializers import SunbedSerializer


class SunbedViewSet(viewsets.ModelViewSet):
    pagination_class = GenericPagination
    serializer_class = SunbedSerializer
    filterset_class = SunbedFilterSet
    queryset = Sunbed.objects.all()


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
        queryset = beach.sunbeds.all()
        # validate query params using serializer
        query_serializer = SunbedQuerySerializer(data=request.query_params)
        query_serializer.is_valid(raise_exception=True)
        # filter queryset for booking date and availability and guest count
        only_available = query_serializer.data.get('only_available', False)
        booking_date = query_serializer.data.get('booking_date')
        guest_count = query_serializer.data.get('guest_count')

        # set booking date in context
        context['booking_date'] = booking_date

        if only_available and booking_date:
            queryset = queryset.exclude(
                id__in=SunbedBooking.objects.filter(
                    booking__status__in=['confirmed', 'pending'],
                    booking__booking_date=booking_date
                ).values_list('sunbed_id', flat=True)
            )

            available_sunbeds_count = queryset.count()
            if guest_count and guest_count > available_sunbeds_count:
                raise ValidationError(
                    {'detail': f'Not enough sunbeds available. Only {available_sunbeds_count} left.'}
                )

        elif booking_date and guest_count:
            queryset = queryset.filter(
                sunbed_bookings__isnull=False,
                sunbed_bookings__booking__status__in=['confirmed', 'pending'],
                sunbed_bookings__booking__booking_date=booking_date,
                sunbed_bookings__booking__guest_count=guest_count
            )

        # filter queryset
        queryset = self.filter_queryset(queryset)
        # paginate queryset
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True, context=context)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True, context=context)
        return Response(serializer.data)

from django_filters.rest_framework import FilterSet, filters

from booking.choices import BookingStatusChoices
from booking.models import Booking
from helpers.querysets import beach_queryset, user_queryset, sunbed_queryset


class BookingFilterSet(FilterSet):
    booking_date = filters.DateFromToRangeFilter()
    guest_count = filters.NumericRangeFilter()
    user = filters.ModelMultipleChoiceFilter(queryset=user_queryset)
    sunbeds = filters.ModelMultipleChoiceFilter(queryset=sunbed_queryset)
    booked_by = filters.ModelMultipleChoiceFilter(queryset=user_queryset)
    status = filters.MultipleChoiceFilter(choices=BookingStatusChoices.choices)
    created = filters.DateTimeFromToRangeFilter()
    updated = filters.DateTimeFromToRangeFilter()
    # beach related fields
    beach_id = filters.ModelMultipleChoiceFilter(queryset=beach_queryset, field_name='beach_id')
    beach = filters.CharFilter(lookup_expr='icontains', field_name='beach__title')
    city = filters.CharFilter(lookup_expr='icontains', field_name='beach__location__city')
    country = filters.CharFilter(lookup_expr='icontains', field_name='beach__location__country')
    # sunbed related fields
    area = filters.CharFilter(lookup_expr='icontains', field_name='sunbeds__area')
    identity = filters.CharFilter(lookup_expr='icontains', field_name='sunbeds__identity')

    class Meta:
        model = Booking
        fields = "__all__"

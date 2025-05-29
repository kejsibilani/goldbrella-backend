from django_filters.rest_framework import FilterSet
from django_filters.rest_framework import filters

from booking.choices import BookingStatusChoices
from booking.models import Booking
from helpers.querysets import beach_queryset
from helpers.querysets import inventory_queryset
from helpers.querysets import sunbed_queryset
from helpers.querysets import user_queryset


class BookingFilterSet(FilterSet):
    booking_date = filters.DateFromToRangeFilter()
    user = filters.ModelMultipleChoiceFilter(queryset=user_queryset)
    sunbeds = filters.ModelMultipleChoiceFilter(queryset=sunbed_queryset)
    booked_by = filters.ModelMultipleChoiceFilter(queryset=user_queryset)
    status = filters.MultipleChoiceFilter(choices=BookingStatusChoices.values)
    created = filters.DateTimeFromToRangeFilter()
    updated = filters.DateTimeFromToRangeFilter()
    # anonymity of booking
    is_anonymous = filters.BooleanFilter()
    # beach related fields
    beach_id = filters.ModelMultipleChoiceFilter(queryset=beach_queryset, field_name='beach_id')
    beach = filters.CharFilter(lookup_expr='icontains', field_name='beach__title')
    city = filters.CharFilter(lookup_expr='icontains', field_name='beach__location__city')
    country = filters.CharFilter(lookup_expr='icontains', field_name='beach__location__country')
    # inventory related fields
    inventory = filters.ModelMultipleChoiceFilter(queryset=inventory_queryset, field_name='inventory__inventory_item')
    inventory_item = filters.CharFilter(lookup_expr='icontains', field_name='inventory__inventory_item__name')
    # sunbed related fields
    area = filters.CharFilter(lookup_expr='icontains', field_name='sunbeds__area')
    identity = filters.CharFilter(lookup_expr='icontains', field_name='sunbeds__identity')

    class Meta:
        model = Booking
        fields = "__all__"

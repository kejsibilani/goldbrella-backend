from django_filters.rest_framework import FilterSet
from django_filters.rest_framework import filters
from pytz import country_names

from beach.models import Beach
from helpers.querysets import beach_location_queryset
from helpers.querysets import facilities_queryset
from helpers.querysets import rules_queryset


class BeachFilterSet(FilterSet):
    title = filters.CharFilter(lookup_expr='icontains')
    description = filters.CharFilter(lookup_expr='icontains')
    latitude = filters.NumericRangeFilter()
    longitude = filters.NumericRangeFilter()
    location = filters.ModelMultipleChoiceFilter(queryset=beach_location_queryset)
    facilities = filters.ModelMultipleChoiceFilter(queryset=facilities_queryset)
    rules = filters.ModelMultipleChoiceFilter(queryset=rules_queryset)
    created = filters.DateTimeFromToRangeFilter()
    updated = filters.DateTimeFromToRangeFilter()
    # query on location city and country
    city = filters.CharFilter(lookup_expr='icontains', field_name='location__city')
    country = filters.MultipleChoiceFilter(choices=country_names.items(), field_name='location__country')
    # opening season
    opening_date = filters.DateFromToRangeFilter(field_name='seasons__opening_date')
    closing_date = filters.DateFromToRangeFilter(field_name='seasons__closing_date')

    class Meta:
        model = Beach
        fields = "__all__"

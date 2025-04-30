from django_filters.rest_framework import FilterSet, filters
from pytz import country_names

from beach.models import Beach
from helpers.querysets import beach_location_queryset, facilities_queryset, rules_queryset


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
    # query image links
    images = filters.CharFilter(lookup_expr='icontains', field_name='images__link')
    # query on location city and country
    city = filters.CharFilter(lookup_expr='icontains', field_name='location__city')
    country = filters.MultipleChoiceFilter(choices=country_names.items(), field_name='location__country')

    class Meta:
        model = Beach
        fields = "__all__"

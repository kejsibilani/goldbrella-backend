from django_filters.rest_framework import filters, FilterSet
from pytz import country_names

from location.models import Location


class LocationFilterSet(FilterSet):
    country = filters.MultipleChoiceFilter(choices=country_names.items())
    city = filters.CharFilter(lookup_expr='icontains')
    created = filters.DateTimeFromToRangeFilter()
    updated = filters.DateTimeFromToRangeFilter()

    class Meta:
        model = Location
        fields = "__all__"

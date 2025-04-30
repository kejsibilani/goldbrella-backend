from django_filters.rest_framework import filters, FilterSet
from pytz import country_names

from beach.models import BeachLocation


class BeachLocationFilterSet(FilterSet):
    country = filters.MultipleChoiceFilter(choices=country_names.items())
    city = filters.CharFilter(lookup_expr='icontains')
    created = filters.DateTimeFromToRangeFilter()
    updated = filters.DateTimeFromToRangeFilter()

    class Meta:
        model = BeachLocation
        fields = "__all__"

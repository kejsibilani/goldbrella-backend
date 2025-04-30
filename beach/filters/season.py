from django_filters.rest_framework import FilterSet, filters

from beach.models import BeachOpeningSeason
from helpers.querysets import beach_queryset


class BeachOpeningSeasonFilterSet(FilterSet):
    title = filters.CharFilter(lookup_expr='icontains')
    beach = filters.ModelMultipleChoiceFilter(queryset=beach_queryset)
    opening_date = filters.DateFromToRangeFilter()
    closing_date = filters.DateFromToRangeFilter()
    created = filters.DateTimeFromToRangeFilter()
    updated = filters.DateTimeFromToRangeFilter()

    class Meta:
        model = BeachOpeningSeason
        fields = '__all__'

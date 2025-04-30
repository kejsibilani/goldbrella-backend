from django_filters.rest_framework import FilterSet, filters

from beach.models import BeachImage
from helpers.querysets import beach_queryset


class BeachImageFilterSet(FilterSet):
    beach = filters.ModelMultipleChoiceFilter(queryset=beach_queryset)
    link = filters.CharFilter(lookup_expr='icontains')
    created = filters.DateTimeFromToRangeFilter()
    updated = filters.DateTimeFromToRangeFilter()

    class Meta:
        model = BeachImage
        fields = "__all__"

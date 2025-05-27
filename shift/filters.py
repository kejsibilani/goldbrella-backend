from django_filters.rest_framework import FilterSet
from django_filters.rest_framework import filters

from helpers.querysets import staff_queryset
from helpers.querysets import zone_queryset
from shift.models import Shift


class ShiftFilterSet(FilterSet):
    start_time = filters.TimeRangeFilter()
    end_time = filters.TimeRangeFilter()
    zone = filters.ModelMultipleChoiceFilter(queryset=zone_queryset)
    user = filters.ModelMultipleChoiceFilter(queryset=staff_queryset)
    created = filters.DateTimeFromToRangeFilter()
    updated = filters.DateTimeFromToRangeFilter()

    class Meta:
        model = Shift
        fields = "__all__"

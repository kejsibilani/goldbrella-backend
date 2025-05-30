from django_filters.rest_framework import FilterSet
from django_filters.rest_framework import filters

from helpers.querysets import beach_queryset
from helpers.querysets import supervisor_queryset
from zone.choices import ZoneLocationChoices
from zone.models import Zone


class ZoneFilterSet(FilterSet):

    supervisor = filters.ModelMultipleChoiceFilter(queryset=supervisor_queryset)
    beach = filters.ModelMultipleChoiceFilter(queryset=beach_queryset)
    location = filters.MultipleChoiceFilter(choices=ZoneLocationChoices.values)
    created = filters.DateTimeFromToRangeFilter()
    updated = filters.DateTimeFromToRangeFilter()

    class Meta:
        model = Zone
        fields = "__all__"

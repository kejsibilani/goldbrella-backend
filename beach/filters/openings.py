from django_filters.rest_framework import FilterSet
from django_filters.rest_framework import filters

from beach.choices import OpeningDayChoices
from beach.models import BeachOpeningHour
from helpers.querysets import beach_queryset
from helpers.querysets import beach_season_queryset


class BeachOpeningHourFilterSet(FilterSet):
    season = filters.ModelMultipleChoiceFilter(queryset=beach_season_queryset)
    weekday = filters.MultipleChoiceFilter(choices=OpeningDayChoices.values)
    opening_time = filters.TimeRangeFilter()
    closing_time = filters.TimeRangeFilter()
    created = filters.DateTimeFromToRangeFilter()
    updated = filters.DateTimeFromToRangeFilter()
    # additional support
    beach = filters.ModelMultipleChoiceFilter(queryset=beach_queryset, field_name='season__beach')

    class Meta:
        model = BeachOpeningHour
        fields = "__all__"

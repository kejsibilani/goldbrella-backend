from django_filters.rest_framework import FilterSet
from django_filters.rest_framework import filters

from helpers.querysets import zone_queryset
from sunbed.choices import SunbedStatusChoices
from sunbed.choices import SunbedTypeChoices
from sunbed.models import Sunbed


class SunbedFilterSet(FilterSet):
    price = filters.NumericRangeFilter()
    sunbed_type = filters.MultipleChoiceFilter(choices=SunbedTypeChoices.values)
    status = filters.MultipleChoiceFilter(choices=SunbedStatusChoices.values)
    area = filters.CharFilter(lookup_expr='icontains')
    identity = filters.CharFilter(lookup_expr='icontains')
    zone = filters.ModelMultipleChoiceFilter(queryset=zone_queryset)
    created = filters.DateTimeFromToRangeFilter()
    updated = filters.DateTimeFromToRangeFilter()

    class Meta:
        model = Sunbed
        fields = '__all__'

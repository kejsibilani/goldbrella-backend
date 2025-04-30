from django_filters.rest_framework import FilterSet, filters

from helpers.querysets import beach_queryset
from sunbed.choices import SunbedTypeChoices
from sunbed.models import Sunbed


class SunbedFilterSet(FilterSet):
    price = filters.NumericRangeFilter()
    discount_percentage = filters.NumericRangeFilter()
    sunbed_type = filters.MultipleChoiceFilter(choices=SunbedTypeChoices.choices)
    area = filters.CharFilter(lookup_expr='icontains')
    identity = filters.CharFilter(lookup_expr='icontains')
    beach = filters.ModelMultipleChoiceFilter(queryset=beach_queryset)
    created = filters.DateTimeFromToRangeFilter()
    updated = filters.DateTimeFromToRangeFilter()

    class Meta:
        model = Sunbed
        fields = '__all__'

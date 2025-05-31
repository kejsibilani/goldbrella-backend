from django_filters.rest_framework import FilterSet
from django_filters.rest_framework import filters

from helpers.querysets import beach_queryset
from helpers.querysets import zone_queryset
from sunbed.choices import SunbedStatusChoices
from sunbed.choices import SunbedTypeChoices
from sunbed.models import Sunbed


class SunbedFilterSet(FilterSet):
    price = filters.NumericRangeFilter()
    sunbed_type = filters.MultipleChoiceFilter(choices=SunbedTypeChoices.choices)
    status = filters.MultipleChoiceFilter(choices=SunbedStatusChoices.choices)
    area = filters.CharFilter(lookup_expr='icontains')
    identity = filters.CharFilter(lookup_expr='icontains')
    zone = filters.ModelMultipleChoiceFilter(queryset=zone_queryset)
    created = filters.DateTimeFromToRangeFilter()
    updated = filters.DateTimeFromToRangeFilter()
    # zone beach filter
    beach = filters.ModelMultipleChoiceFilter(queryset=beach_queryset, field_name='zone__beach')

    class Meta:
        model = Sunbed
        fields = '__all__'

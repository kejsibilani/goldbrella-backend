from django_filters.rest_framework import FilterSet, filters

from services.models import Facility


class FacilityFilterSet(FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')
    created = filters.DateTimeFromToRangeFilter()
    updated = filters.DateTimeFromToRangeFilter()

    class Meta:
        model = Facility
        fields = '__all__'

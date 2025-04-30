from django_filters.rest_framework import FilterSet, filters

from services.models import Rule


class RuleFilterSet(FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')
    created = filters.DateTimeFromToRangeFilter()
    updated = filters.DateTimeFromToRangeFilter()

    class Meta:
        model = Rule
        fields = '__all__'

from django_filters.rest_framework import FilterSet, filters

from helpers.querysets import beach_queryset
from inventory.models import InventoryItem


class InventoryItemFilterSet(FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')
    price = filters.NumericRangeFilter()
    discount_percentage = filters.NumericRangeFilter()
    identity = filters.CharFilter(lookup_expr='icontains')
    beach = filters.ModelMultipleChoiceFilter(queryset=beach_queryset)
    created = filters.DateTimeFromToRangeFilter()
    updated = filters.DateTimeFromToRangeFilter()

    class Meta:
        model = InventoryItem
        fields = '__all__'

from django_filters.rest_framework import FilterSet
from django_filters.rest_framework import filters

from helpers.querysets import beach_queryset
from inventory.models import InventoryItem


class InventoryItemFilterSet(FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')
    price = filters.NumericRangeFilter()
    reusable_item = filters.BooleanFilter()
    identity = filters.CharFilter(lookup_expr='icontains')
    beach = filters.ModelMultipleChoiceFilter(queryset=beach_queryset)
    created = filters.DateTimeFromToRangeFilter()
    updated = filters.DateTimeFromToRangeFilter()
    category = filters.CharFilter(lookup_expr='exact')

    class Meta:
        model = InventoryItem
        fields = '__all__'

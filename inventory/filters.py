from django_filters.rest_framework import FilterSet, filters

from helpers.querysets import beach_queryset
from inventory.models import Inventory


class InventoryFilterSet(FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')
    price = filters.NumericRangeFilter()
    discount_percentage = filters.NumericRangeFilter()
    quantity = filters.NumericRangeFilter()
    beach = filters.ModelMultipleChoiceFilter(queryset=beach_queryset)
    created = filters.DateTimeFromToRangeFilter()
    updated = filters.DateTimeFromToRangeFilter()

    class Meta:
        model = Inventory
        fields = '__all__'

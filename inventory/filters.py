from django.db.models import Count
from django_filters.rest_framework import FilterSet, filters

from helpers.querysets import beach_queryset
from inventory.models import Inventory


class InventoryFilterSet(FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')
    price = filters.NumericRangeFilter()
    discount_percentage = filters.NumericRangeFilter()
    quantity = filters.NumericRangeFilter(method='filter_quantity')
    beach = filters.ModelMultipleChoiceFilter(queryset=beach_queryset)
    created = filters.DateTimeFromToRangeFilter()
    updated = filters.DateTimeFromToRangeFilter()
    # Item based filters
    identity = filters.CharFilter(lookup_expr='icontains', field_name='items__identity')

    class Meta:
        model = Inventory
        fields = '__all__'

    @staticmethod
    def filter_quantity(queryset, name, value):
        return queryset.annotate(
            count=Count('items')
        ).filter(
            count__gte=value.start,
            count__lte=value.stop
        )

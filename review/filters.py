from django_filters.rest_framework import FilterSet
from django_filters.rest_framework import filters

from helpers.querysets import booking_queryset
from helpers.querysets import user_queryset
from review.models import Review


class ReviewFilterSet(FilterSet):
    message = filters.CharFilter(lookup_expr='icontains')
    rating = filters.NumericRangeFilter()
    booking = filters.ModelMultipleChoiceFilter(queryset=booking_queryset)
    user = filters.ModelMultipleChoiceFilter(queryset=user_queryset)
    created = filters.DateTimeFromToRangeFilter()
    updated = filters.DateTimeFromToRangeFilter()

    class Meta:
        model = Review
        fields = '__all__'

from django_filters.rest_framework import FilterSet
from django_filters.rest_framework import filters

from helpers.querysets import self_user_queryset
from notification.models import Notification


class NotificationFilterSet(FilterSet):
    message = filters.CharFilter(lookup_expr='icontains')
    user = filters.ModelMultipleChoiceFilter(queryset=self_user_queryset)
    is_read = filters.BooleanFilter()
    created = filters.DateTimeFromToRangeFilter()
    updated = filters.DateTimeFromToRangeFilter()

    class Meta:
        model = Notification
        fields = '__all__'

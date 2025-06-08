from django_filters.rest_framework import FilterSet
from django_filters.rest_framework import filters

from mailer.choices import ScheduledEmailStatusChoices
from mailer.models import ScheduledEmail


class ScheduledEmailFilterSet(FilterSet):
    receivers = filters.CharFilter(lookup_expr='icontains')
    sender = filters.CharFilter(lookup_expr='icontains')
    system_generated = filters.BooleanFilter()
    timestamp = filters.DateTimeFromToRangeFilter()
    message = filters.CharFilter(lookup_expr='icontains')
    status = filters.MultipleChoiceFilter(choices=ScheduledEmailStatusChoices.choices)

    class Meta:
        model = ScheduledEmail
        exclude = ('subject', 'content')

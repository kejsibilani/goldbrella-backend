from django_filters.rest_framework import FilterSet
from django_filters.rest_framework import filters

from complaint.choices import ComplaintStatusChoices
from complaint.models import Complaint
from helpers.querysets import complaint_related_queryset
from helpers.querysets import management_queryset


class ComplaintFilterSet(FilterSet):
    creator = filters.ModelMultipleChoiceFilter(queryset=management_queryset)
    status = filters.MultipleChoiceFilter(choices=ComplaintStatusChoices.values)
    details = filters.CharFilter(lookup_expr='icontains')
    related_content_type = filters.MultipleChoiceFilter(queryset=complaint_related_queryset)
    related_object_id = filters.NumericRangeFilter()
    created = filters.DateTimeFromToRangeFilter()
    updated = filters.DateTimeFromToRangeFilter()

    class Meta:
        model = Complaint
        fields = '__all__'

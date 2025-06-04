from django_filters.rest_framework import FilterSet
from django_filters.rest_framework import filters

from helpers.querysets import booking_queryset
from invoice.choices import PaymentMethodChoices
from invoice.choices import PaymentStatusChoices
from invoice.models import BookingInvoice


class BookingInvoiceFilterSet(FilterSet):
    invoice_number = filters.CharFilter(lookup_expr='icontains')
    booking = filters.ModelMultipleChoiceFilter(queryset=booking_queryset)
    paid_amount = filters.NumericRangeFilter()
    payment_method = filters.MultipleChoiceFilter(choices=PaymentMethodChoices.choices)
    payment_status = filters.MultipleChoiceFilter(choices=PaymentStatusChoices.choices)
    created = filters.DateTimeFromToRangeFilter()
    updated = filters.DateTimeFromToRangeFilter()

    class Meta:
        model = BookingInvoice
        fields = '__all__'

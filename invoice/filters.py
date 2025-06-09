from django_filters.rest_framework import FilterSet
from django_filters.rest_framework import filters

from helpers.querysets import booking_queryset
from invoice.choices import InvoiceStatusChoices
from invoice.models import BookingInvoice
from payment.choices import PaymentMethodChoices


class BookingInvoiceFilterSet(FilterSet):
    invoice_number = filters.CharFilter(lookup_expr='icontains')
    booking = filters.ModelMultipleChoiceFilter(queryset=booking_queryset)
    paid_amount = filters.NumericRangeFilter()
    status = filters.MultipleChoiceFilter(choices=InvoiceStatusChoices.choices)
    is_refunded = filters.BooleanFilter()
    created = filters.DateTimeFromToRangeFilter()
    updated = filters.DateTimeFromToRangeFilter()
    # payment based filter
    payment_method = filters.MultipleChoiceFilter(choices=PaymentMethodChoices.choices, field_name='payments__payment_method')

    class Meta:
        model = BookingInvoice
        fields = '__all__'

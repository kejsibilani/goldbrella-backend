from django_filters.rest_framework import FilterSet, filters

from helpers.querysets import booking_queryset
from payment.choices import PaymentMethodChoices, PaymentStatusChoices
from payment.models import BookingPayment


class BookingPaymentFilterSet(FilterSet):
    booking = filters.ModelMultipleChoiceFilter(queryset=booking_queryset)
    transaction_id = filters.CharFilter(lookup_expr='icontains')
    method = filters.MultipleChoiceFilter(choices=PaymentMethodChoices.choices)
    status = filters.MultipleChoiceFilter(choices=PaymentStatusChoices.choices)
    amount = filters.NumericRangeFilter()
    created = filters.DateTimeFromToRangeFilter()
    updated = filters.DateTimeFromToRangeFilter()

    class Meta:
        model = BookingPayment
        fields = '__all__'

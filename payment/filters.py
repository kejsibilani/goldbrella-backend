from django_filters.rest_framework import FilterSet
from django_filters.rest_framework import filters

from helpers.querysets import booking_queryset
from helpers.querysets import invoice_queryset
from payment.choices import PaymentMethodChoices
from payment.choices import PaymentStatusChoices
from payment.models import BookingPayment


class BookingPaymentFilterSet(FilterSet):
    """
    Example FilterSet for BookingPayment in the same style as your BookingFilterSet.
    Defines commonly‐used filters; you can add or remove fields as needed.
    """

    # Filter by the related Booking(s)
    booking = filters.ModelMultipleChoiceFilter(queryset=booking_queryset, field_name='invoice__booking')
    # Filter by the related Invoice
    invoice = filters.ModelMultipleChoiceFilter(queryset=invoice_queryset)
    currency = filters.CharFilter(lookup_expr='icontains', field_name='invoice__currency')

    # BasePayment fields (django-payments) – common filters:
    payment_method = filters.MultipleChoiceFilter(choices=PaymentMethodChoices.choices)
    status = filters.MultipleChoiceFilter(choices=PaymentStatusChoices.choices)
    note = filters.CharFilter(lookup_expr='icontains')
    amount = filters.NumericRangeFilter()

    billing_first_name = filters.CharFilter(lookup_expr='icontains')
    billing_last_name = filters.CharFilter(lookup_expr='icontains')
    billing_phone_number = filters.CharFilter(lookup_expr='icontains')
    billing_email = filters.CharFilter(lookup_expr='iexact')

    billing_address_1 = filters.CharFilter(lookup_expr='icontains')
    billing_address_2 = filters.CharFilter(lookup_expr='icontains')
    billing_city = filters.CharFilter(lookup_expr='icontains')
    billing_postcode = filters.CharFilter(lookup_expr='icontains')
    billing_country_code = filters.CharFilter(lookup_expr='icontains')

    created = filters.DateTimeFromToRangeFilter()
    updated = filters.DateTimeFromToRangeFilter()

    class Meta:
        model = BookingPayment
        fields = "__all__"

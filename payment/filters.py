from django_filters.rest_framework import FilterSet, filters
from django.contrib.auth import get_user_model
from booking.models import Booking
from payment.models import BookingPayment

User = get_user_model()


class BookingPaymentFilterSet(FilterSet):
    """
    Example FilterSet for BookingPayment in the same style as your BookingFilterSet.
    Defines commonly‐used filters; you can add or remove fields as needed.
    """

    # Filter by the related Booking(s)
    booking = filters.ModelMultipleChoiceFilter(queryset=booking_queryset)

    # BasePayment fields (django-payments) – common filters:

    variant = filters.CharFilter(lookup_expr='icontains')
    description = filters.CharFilter(lookup_expr='icontains')
    currency = filters.CharFilter(lookup_expr='icontains')
    message = filters.CharFilter(lookup_expr='icontains')

    total = filters.NumericRangeFilter()
    tax = filters.NumericRangeFilter()
    delivery = filters.NumericRangeFilter()
    captured_amount = filters.NumericRangeFilter()

    billing_first_name = filters.CharFilter(lookup_expr='icontains')
    billing_last_name = filters.CharFilter(lookup_expr='icontains')
    billing_city = filters.CharFilter(lookup_expr='icontains')
    billing_postcode = filters.CharFilter(lookup_expr='icontains')
    billing_country_code = filters.CharFilter(lookup_expr='icontains')
    billing_country_area = filters.CharFilter(lookup_expr='icontains')

    customer_ip_address = filters.CharFilter(lookup_expr='icontains')

    status = filters.MultipleChoiceFilter(choices=BookingPayment._meta.get_field('status').choices)


    # Timestamps
    created = filters.DateTimeFromToRangeFilter(field_name='created')
    modified = filters.DateTimeFromToRangeFilter(field_name='modified')

    class Meta:
        model = BookingPayment
        fields = "__all__"

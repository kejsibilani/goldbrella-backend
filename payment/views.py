from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import SearchFilter

from helpers.pagination import GenericPagination
from helpers.permissions import CustomDjangoModelPermissions
from payment.filters import BookingPaymentFilterSet
from payment.models import BookingPayment
from payment.serializers import BookingPaymentSerializer

# from decimal import Decimal
# from django.shortcuts import get_object_or_404, redirect
# from payments import get_payment_model
# from booking.models import Booking
#
# Payment = get_payment_model()
#
# def pay_for_booking(request, booking_pk):
#     booking = get_object_or_404(Booking, pk=booking_pk)
#
#     # calculate your total (e.g. per-sunbed price)
#     total = sum(sb.price for sb in booking.sunbeds.all())
#
#     payment = Payment.objects.create(
#         variant='default',
#         description=f'Booking #{booking.pk} at {booking.beach.title}',
#         total=Decimal(total),
#         currency='EUR',
#         billing_first_name=request.user.first_name,
#         billing_last_name=request.user.last_name,
#         customer_ip_address=request.META.get('REMOTE_ADDR'),
#         booking=booking
#     )
#     # hands off to the provider (Stripe checkout, PayPal, etc.)
#     return redirect(payment.get_process_url())
#
# # booking/views.py
# from django.http import FileResponse
# from .models import Invoice
#
# def download_invoice(request, booking_pk):
#     invoice = get_object_or_404(Invoice, booking__pk=booking_pk)
#     return FileResponse(invoice.pdf, as_attachment=True,
#                         filename=f'invoice_{booking_pk}.pdf')


# Create your views here.
class BookingPaymentViewSet(viewsets.ModelViewSet):
    permission_classes = [CustomDjangoModelPermissions]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    serializer_class = BookingPaymentSerializer
    filterset_class = BookingPaymentFilterSet
    pagination_class = GenericPagination
    search_fields = ['transaction_id', 'booking__booking_date']

    def get_queryset(self):
        request_user = self.request.user
        if request_user.is_superuser:
            return BookingPayment.objects.all()
        elif request_user.is_staff:
            return BookingPayment.objects.filter(
                Q(booking__user=request_user, booking__booked_by=request_user, _connector=Q.OR)
            )
        return BookingPayment.objects.filter(booking__user=request_user)

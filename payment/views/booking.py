from django.db.models import Q
from payments import PaymentStatus
from payments import RedirectNeeded
from payments import get_payment_model
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST

from booking.models import Booking
from payment.serializers import BookingPaymentCreateSerializer
from payment.serializers.create import PaymentValidationSerializer

Payment = get_payment_model()
class BookingPaymentViewSet(viewsets.GenericViewSet):
    permission_classes = [AllowAny]
    serializer_class = BookingPaymentCreateSerializer

    def get_queryset(self):
        request_user = self.request.user

        if request_user.is_superuser:
            return Booking.objects.all()
        elif request_user.is_staff:
            return Booking.objects.filter(
                Q(booked_by=request_user, user=request_user, _connector=Q.OR)
            )
        elif request_user.is_authenticated:
            return Booking.objects.filter(user=request_user)

        invoice_number = self.request.GET.get("invoice")
        return Booking.objects.filter(invoice__invoice_number__iexact=invoice_number)

    @action(detail=True, methods=['post'], url_path='pay')
    def pay(self, request, *args, **kwargs):
        booking = self.get_object()

        query_serializer = PaymentValidationSerializer(data=request.data)
        query_serializer.is_valid(raise_exception=True)

        description = f'Payment for Booking #{booking.pk}'
        serializer = self.get_serializer(data=dict(
            tax=booking.invoice.total_tax_amount,
            total=booking.invoice.total_amount,
            currency=booking.invoice.currency,
            description=description,
            booking=booking,
            delivery=0,
            # billing details
            **query_serializer.data
        ))
        serializer.is_valid(raise_exception=True)
        payment = serializer.save()

        try:
            # Attempt to process the payment
            payment.change_status('waiting')
            # payment.get_purchased_items
            form = payment.get_form(data=request.data)
            if form.is_valid():
                form.save()
                return Response(serializer.data)
            else:
                return Response(form.errors, status=HTTP_400_BAD_REQUEST)
        except RedirectNeeded as redirect_to:
            # For card payments (like Stripe) that require redirection
            return Response({'redirect_url': str(redirect_to)})

    @action(detail=True, methods=['post'], url_path='pay-via-cash')
    def cash_payment(self, request, *args, **kwargs):
        booking = self.get_object()
        # Here, you can add permission checks (e.g. is staff)
        if request.user.is_staff or request.user.is_superuser:
            description = f'Payment for Booking #{booking.pk}'
            serializer = self.get_serializer(data=dict(
                tax=booking.invoice.total_tax_amount,
                total=booking.invoice.total_amount,
                currency=booking.invoice.currency,
                description=description,
                booking=booking,
                delivery=0
            ))
            serializer.is_valid(raise_exception=True)
            payment = serializer.save()
            # Update payment to confirmed
            payment.change_status(status=PaymentStatus.CONFIRMED)
            return Response(serializer.data)
        raise PermissionDenied

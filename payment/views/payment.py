from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response

from helpers.pagination import GenericPagination
from helpers.permissions import CustomDjangoModelPermissions
from payment.choices import PaymentMethodChoices
from payment.choices import PaymentStatusChoices
from payment.filters import BookingPaymentFilterSet
from payment.models import BookingPayment
from payment.serializers import BookingPaymentSerializer


# Create your views here.
class BookingPaymentViewSet(CreateModelMixin, viewsets.ReadOnlyModelViewSet):
    filter_backends = [DjangoFilterBackend, SearchFilter]
    serializer_class = BookingPaymentSerializer
    filterset_class = BookingPaymentFilterSet
    pagination_class = GenericPagination
    search_fields = ['transaction_id', 'booking__booking_date']

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        return [CustomDjangoModelPermissions()]

    def get_queryset(self):
        request_user = self.request.user
        if request_user.is_superuser:
            return BookingPayment.objects.all()
        elif request_user.is_staff:
            return BookingPayment.objects.filter(
                Q(invoice__booking__user=request_user, invoice__booking__booked_by=request_user, _connector=Q.OR)
            )
        return BookingPayment.objects.filter(invoice__booking__user=request_user)

    @action(detail=True, methods=['post'], url_path='mark-paid')
    def mark_success(self, request, pk=None):
        """
        Staff can manually mark a payment as successful, if necessary (not for Stripe).
        """

        if not (request.user.is_staff or request.user.is_superuser):
            raise PermissionDenied({'detail': 'Only staff and superuser can handle manual payments'})

        payment = self.get_object()
        if payment.payment_method == PaymentMethodChoices.STRIPE.value:
            raise ValidationError({'detail': 'Stripe payments are auto-confirmed via webhook.'})

        serializer = self.get_serializer(payment)
        serializer.is_valid(raise_exception=True)
        serializer.save(
            status=PaymentStatusChoices.SUCCEEDED.value
        )

        return Response(serializer.data)

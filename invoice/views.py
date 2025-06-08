from django.db.models import Q
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.viewsets import ReadOnlyModelViewSet

from booking.models import Booking
from helpers.pagination import GenericPagination
from invoice.filters import BookingInvoiceFilterSet
from invoice.models import BookingInvoice
from invoice.serializers import BookingInvoiceSerializer


class BookingInvoiceViewSet(ReadOnlyModelViewSet):
    permission_classes = [DjangoModelPermissions]
    serializer_class = BookingInvoiceSerializer
    filterset_class = BookingInvoiceFilterSet
    pagination_class = GenericPagination

    def get_queryset(self):
        request_user = self.request.user

        if request_user.is_superuser:
            return BookingInvoice.objects.all()
        elif request_user.is_staff:
            return BookingInvoice.objects.filter(
                Q(booking__booked_by=request_user, booking__user=request_user, _connector=Q.OR)
            )
        return BookingInvoice.objects.filter(booking__user=request_user)


class BookingInvoiceReadViewSet(GenericViewSet):
    permission_classes = [DjangoModelPermissions]
    serializer_class = BookingInvoiceSerializer

    def get_queryset(self):
        request_user = self.request.user

        if request_user.is_superuser:
            return Booking.objects.all()
        elif request_user.is_staff:
            return BookingInvoice.objects.filter(
                Q(booked_by=request_user, user=request_user, _connector=Q.OR)
            )
        return BookingInvoice.objects.filter(user=request_user)

    @action(methods=['get'], detail=True)
    def invoice(self, request, *args, **kwargs):
        booking = self.get_object()

        instance = getattr(booking, 'invoice', None)
        if instance is None:
            raise NotFound({'detail': 'No invoice matches the given query.'})

        serializer = self.get_serializer(instance, read_only=True)
        return Response(serializer.data)

from django.db.models import Q
from rest_framework.viewsets import ReadOnlyModelViewSet

from helpers.pagination import GenericPagination
from invoice.filters import BookingInvoiceFilterSet
from invoice.models import BookingInvoice
from invoice.serializers import BookingInvoiceSerializer


class BookingInvoiceViewSet(ReadOnlyModelViewSet):
    serializer_class = BookingInvoiceSerializer
    filterset_class = BookingInvoiceFilterSet
    pagination_class = GenericPagination

    def get_queryset(self):
        request_user = self.request.user

        if request_user.has_role('admin'):
            return BookingInvoice.objects.all()
        elif request_user.has_role('supervisor'):
            return BookingInvoice.objects.filter(
                Q(booking__booked_by=request_user, booking__user=request_user, _connector=Q.OR)
            )
        elif request_user.has_role('staff'):
            return BookingInvoice.objects.filter(
                Q(booking__booked_by=request_user, booking__user=request_user, _connector=Q.OR)
            )
        return BookingInvoice.objects.filter(booking__user=request_user)

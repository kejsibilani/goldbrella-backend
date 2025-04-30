from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import SearchFilter

from helpers.pagination import GenericPagination
from helpers.permissions import CustomDjangoModelPermissions
from payment.filters import BookingPaymentFilterSet
from payment.models import BookingPayment
from payment.serializers import BookingPaymentSerializer


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

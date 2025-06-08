from django.db.models import Q
from django.utils.timezone import localdate
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.viewsets import GenericViewSet

from beach.models import Beach
from booking.serializers import BookingBeachReadSerializer
from helpers.pagination import GenericPagination


class BookingBeachViewSet(ListModelMixin, GenericViewSet):
    permission_classes = [DjangoModelPermissions]
    serializer_class = BookingBeachReadSerializer
    pagination_class = GenericPagination

    def get_queryset(self):
        request_user = self.request.user

        if request_user.is_superuser or request_user.is_staff:
            return Beach.objects.filter(
                Q(
                    Q(bookings__booking_date__lt=localdate()),
                    Q(
                        bookings__booked_by=request_user,
                        bookings__user=request_user,
                        _connector=Q.OR
                    ),
                    _connector=Q.AND,
                )
            ).order_by('-bookings__booking_date')
        return Beach.objects.filter(
            bookings__booking_date__lt=localdate(),
            bookings__user=request_user
        ).order_by('-bookings__booking_date')

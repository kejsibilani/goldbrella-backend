from django.db.models import Q
from django.utils.timezone import localdate
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.viewsets import GenericViewSet

from booking.serializers import BookingLocationReadSerializer
from helpers.pagination import GenericPagination
from location.models import Location


class BookingLocationViewSet(ListModelMixin, GenericViewSet):
    permission_classes = [DjangoModelPermissions]
    serializer_class = BookingLocationReadSerializer
    pagination_class = GenericPagination

    def get_queryset(self):
        request_user = self.request.user

        if request_user.is_superuser or request_user.is_staff:
            return Location.objects.filter(
                Q(
                    Q(beaches__bookings__booking_date__lt=localdate()),
                    Q(
                        beaches__bookings__booked_by=request_user,
                        beaches__bookings__user=request_user,
                        _connector=Q.OR
                    ),
                    _connector=Q.AND,
                )
            ).order_by('-beaches__bookings__booking_date')
        return Location.objects.filter(
            beaches__bookings__booking_date__lt=localdate(),
            beaches__bookings__user=request_user
        ).order_by('-beaches__bookings__booking_date')

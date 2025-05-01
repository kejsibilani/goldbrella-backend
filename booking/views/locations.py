from django.db.models import Q
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.viewsets import GenericViewSet

from beach.models import BeachLocation
from beach.serializers import BeachLocationSerializer
from helpers.pagination import GenericPagination


class BookingLocationViewSet(ListModelMixin, GenericViewSet):
    permission_classes = [DjangoModelPermissions]
    serializer_class = BeachLocationSerializer
    pagination_class = GenericPagination

    def get_queryset(self):
        request_user = self.request.user

        if request_user.is_superuser or request_user.is_staff:
            return BeachLocation.objects.filter(
                Q(
                    beaches__bookings__booked_by=request_user,
                    beaches__bookings__user=request_user,
                    _connector=Q.OR
                )
            ).order_by('-beaches__bookings__booking_date')
        return BeachLocation.objects.filter(
            beaches__bookings__user=request_user
        ).order_by('-beaches__bookings__booking_date')

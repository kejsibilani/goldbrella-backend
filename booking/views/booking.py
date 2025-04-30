from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.permissions import DjangoModelPermissions

from booking.filters import BookingFilterSet
from booking.models import Booking
from booking.serializers import BookingSerializer
from helpers.pagination import GenericPagination


# Create your views here.
class BookingViewSet(viewsets.ModelViewSet):
    filter_backends = [DjangoFilterBackend, SearchFilter]
    permission_classes = [DjangoModelPermissions]
    serializer_class = BookingSerializer
    pagination_class = GenericPagination
    filterset_class = BookingFilterSet
    search_fields = [
        'user__first_name', 'user__last_name', 'user__email',
        'booked_by__first_name', 'booked_by__last_name',
        'booked_by__email', 'sunbeds__identity', 'booking_date',
    ]

    def get_queryset(self):
        request_user = self.request.user

        if request_user.is_superuser:
            return Booking.objects.all()
        elif request_user.is_staff:
            return Booking.objects.filter(
                Q(booked_by=request_user, user=request_user, _connector=Q.OR)
            )
        return Booking.objects.filter(user=request_user)

    def perform_create(self, serializer):
        serializer.save(booked_by=self.request.user)

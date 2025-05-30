from django.db import transaction
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.mixins import CreateModelMixin
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.permissions import DjangoModelPermissions

from booking.choices import BookingStatusChoices
from booking.filters import BookingFilterSet
from booking.models import Booking
from booking.serializers import AnonymousBookingSerializer
from booking.serializers import BookingReadSerializer
from booking.serializers import BookingSerializer
from helpers.pagination import GenericPagination
from helpers.permissions import IsAnonymousUser


# Create your views here.
class BookingViewSet(viewsets.ModelViewSet):
    filter_backends = [DjangoFilterBackend, SearchFilter]
    permission_classes = [DjangoModelPermissions]
    pagination_class = GenericPagination
    filterset_class = BookingFilterSet
    search_fields = [
        'user__first_name', 'user__last_name', 'user__email',
        'booked_by__first_name', 'booked_by__last_name',
        'booked_by__email', 'sunbeds__identity', 'booking_date',
    ]

    def get_serializer_class(self):
        if self.action in ['retrieve', 'list']:
            return BookingReadSerializer
        return BookingSerializer

    def get_queryset(self):
        request_user = self.request.user

        if request_user.has_role('admin'):
            return Booking.objects.all()
        elif request_user.has_role('supervisor'):
            return Booking.objects.filter(
                Q(booked_by=request_user, user=request_user, _connector=Q.OR)
            )
        elif request_user.has_role('staff'):
            return Booking.objects.filter(
                Q(booked_by=request_user, user=request_user, _connector=Q.OR)
            )
        return Booking.objects.filter(user=request_user)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(booked_by=self.request.user, is_anonymous=False)


class AnonymousBookingViewSet(CreateModelMixin, ListModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsAnonymousUser]
    serializer_class = AnonymousBookingSerializer
    pagination_class = GenericPagination

    def get_queryset(self):
        token = self.request.GET.get('Authorization')
        if not token: raise PermissionDenied({'token': '`token` not found'})
        return Booking.objects.filter(is_anonymous=True, token__key=token)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(
            status=BookingStatusChoices.UNVERIFIED.value,
            is_anonymous=True
        )

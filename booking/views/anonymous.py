from django.db import transaction
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import CreateAPIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.generics import get_object_or_404

from booking.choices import BookingStatusChoices
from booking.models import Booking
from booking.serializers import AnonymousBookingReadSerializer
from booking.serializers import AnonymousBookingSerializer
from helpers.pagination import GenericPagination
from helpers.permissions import IsAnonymousUser


class AnonymousBookingView(CreateAPIView, RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAnonymousUser]
    pagination_class = GenericPagination

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return AnonymousBookingSerializer
        return AnonymousBookingReadSerializer

    def get_object(self):
        token = self.request.GET.get('token')
        if not token: raise PermissionDenied({'token': '`token` not found'})
        # fetch filtered queryset
        queryset = Booking.objects.exclude(
            status=BookingStatusChoices.CANCELLED.value
        ).filter(is_anonymous=True)
        # get booking from token
        return get_object_or_404(queryset, token__key=token)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(is_anonymous=True)

    def perform_destroy(self, instance):
        setattr(instance, 'status', BookingStatusChoices.CANCELLED.value)
        instance.save()

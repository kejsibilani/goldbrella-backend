from datetime import timedelta

from django.conf import settings
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
from mailer.scripts import schedule_email
from mailer.system import system_info


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
        booking = serializer.save(is_anonymous=True)

        cancellation_interval = getattr(settings, 'RESERVATION_CANCELLATION_INTERVAL', 300)
        if booking.is_anonymous: schedule_email(
            reservation_page_link=f"{self.request._current_scheme_host}/reservation?token={booking.token.key}",
            hold_expiry_datetime=booking.created + timedelta(minutes=cancellation_interval),
            contact_page_link=f"{self.request._current_scheme_host}/contact",
            support_page_link=f"{self.request._current_scheme_host}/support",
            hold_expiry_minutes=cancellation_interval // 60,
            template_name='booking_reservation',
            to=[booking.user.email],
            invoice=booking.invoice,
            company=system_info,
            user=booking.user,
            system_mail=True
        )

    def perform_destroy(self, instance):
        setattr(instance, 'status', BookingStatusChoices.CANCELLED.value)
        instance.save()

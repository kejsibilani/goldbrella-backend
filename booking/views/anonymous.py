from datetime import timedelta
import logging

from django.conf import settings
from django.db import transaction
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import CreateAPIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import status

from booking.choices import BookingStatusChoices
from booking.models import Booking, BookingToken
from booking.serializers import AnonymousBookingReadSerializer
from booking.serializers import AnonymousBookingSerializer
from helpers.pagination import GenericPagination
from helpers.permissions import IsAnonymousUser
from mailer.scripts import schedule_email
from mailer.system import system_info

logger = logging.getLogger(__name__)


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
        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error creating anonymous booking: {str(e)}")
            return Response(
                {'error': f'Failed to create anonymous booking: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def perform_create(self, serializer):
        try:
            booking = serializer.save(is_anonymous=True)
            logger.info(f"Anonymous booking created successfully: {booking.id}")
            
            # Ensure the booking has a token (create if it doesn't exist)
            token, created = BookingToken.objects.get_or_create(booking=booking)
            logger.info(f"Booking token {'created' if created else 'retrieved'}: {token.key}")
            
            # Refresh the booking instance to ensure we have the latest data
            booking.refresh_from_db()

            cancellation_interval = getattr(settings, 'RESERVATION_CANCELLATION_INTERVAL', 300)
            if booking.is_anonymous and token:
                try:
                    schedule_email(
                        reservation_page_link=f"{self.request._current_scheme_host}/reservation?token={token.key}",
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
                    logger.info(f"Email scheduled for anonymous booking {booking.id}")
                except Exception as e:
                    # Log the error but don't fail the booking creation
                    logger.error(f"Error scheduling email for anonymous booking {booking.id}: {str(e)}")
            
            logger.info(f"Anonymous booking {booking.id} completed successfully")
            
        except Exception as e:
            logger.error(f"Error in perform_create for anonymous booking: {str(e)}")
            raise

    def perform_destroy(self, instance):
        setattr(instance, 'status', BookingStatusChoices.CANCELLED.value)
        instance.save()

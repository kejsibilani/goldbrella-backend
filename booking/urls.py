from django.urls import path
from rest_framework.routers import DefaultRouter

from booking.views import AnonymousBookingView
from booking.views import BookingBeachViewSet
from booking.views import BookingLocationViewSet
from booking.views import BookingViewSet
from booking.views.verify import BookingVerificationView, booking_qr_code
from booking.views.qr_display import booking_qr_display, booking_qr_api
from invoice.views import BookingInvoiceReadViewSet

app_name = 'booking'

router = DefaultRouter(trailing_slash=False)
router.register(r'bookings/locations', BookingLocationViewSet, basename='booking-location')
router.register(r'bookings/beaches', BookingBeachViewSet, basename='booking-beach')
router.register(r'bookings', BookingViewSet, basename='booking')

urlpatterns = [
    path(r'anonymous/bookings', AnonymousBookingView.as_view(), name='anon-booking'),
    path(r'bookings/verify/<str:token_key>/', BookingVerificationView.as_view(), name='booking-verify'),
    path(r'bookings/<int:booking_id>/qr-code/', booking_qr_code, name='booking-qr-code'),
    # User-facing QR code endpoints
    path(r'bookings/<int:booking_id>/qr/', booking_qr_display, name='booking-qr-display'),
    path(r'api/bookings/<int:booking_id>/qr/', booking_qr_api, name='booking-qr-api'),
]

urlpatterns += router.urls

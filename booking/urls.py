from django.urls import path
from rest_framework.routers import DefaultRouter

from booking.views import AnonymousBookingView
from booking.views import BookingBeachViewSet
from booking.views import BookingLocationViewSet
from booking.views import BookingViewSet
from invoice.views import BookingInvoiceReadViewSet

app_name = 'booking'

router = DefaultRouter(trailing_slash=False)
router.register(r'bookings/locations', BookingLocationViewSet, basename='booking-location')
router.register(r'bookings/beaches', BookingBeachViewSet, basename='booking-beach')
router.register(r'bookings', BookingInvoiceReadViewSet, basename='invoice-read')
router.register(r'bookings', BookingViewSet, basename='booking')


urlpatterns = [
    path(r'anonymous/bookings', AnonymousBookingView.as_view(), name='anon-booking'),
]

urlpatterns += router.urls

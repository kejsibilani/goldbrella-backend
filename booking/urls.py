from django.urls import path
from rest_framework.routers import DefaultRouter

from booking.views import AnonymousBookingView
from booking.views import BookingBeachViewSet
from booking.views import BookingLocationViewSet
from booking.views import BookingViewSet

app_name = 'booking'

router = DefaultRouter(trailing_slash=False)
router.register(r'bookings/locations', BookingLocationViewSet, basename='booking-location')
router.register(r'bookings/beaches', BookingBeachViewSet, basename='booking-beach')
router.register(r'bookings', BookingViewSet, basename='booking')
# router.register(r'bookings', BookingPaymentListViewSet, basename='payment-list')


urlpatterns = [
    path(r'anonymous/bookings', AnonymousBookingView.as_view(), basename='anon-booking'),
]

urlpatterns += router.urls

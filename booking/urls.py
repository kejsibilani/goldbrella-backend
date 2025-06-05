from rest_framework.routers import DefaultRouter

from booking.views import AnonymousBookingViewSet
from booking.views import BookingBeachViewSet
from booking.views import BookingLocationViewSet
from booking.views import BookingViewSet

app_name = 'booking'

router = DefaultRouter(trailing_slash=False)
router.register(r'bookings/locations', BookingLocationViewSet, basename='booking-location')
router.register(r'bookings/beaches', BookingBeachViewSet, basename='booking-beach')
router.register(r'anonymous/bookings', AnonymousBookingViewSet, basename='anon-booking')
router.register(r'bookings', BookingViewSet, basename='booking')
# router.register(r'bookings', BookingPaymentListViewSet, basename='payment-list')


urlpatterns = router.urls

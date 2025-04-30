from rest_framework.routers import DefaultRouter

from booking.views import BookingViewSet
from booking.views import BookingLocationViewSet
from booking.views import BookingPaymentListViewSet

router = DefaultRouter(trailing_slash=False)

router.register(r'bookings/locations', BookingLocationViewSet, basename='booking-location')
router.register(r'bookings', BookingViewSet, basename='booking')
router.register(r'bookings', BookingPaymentListViewSet, basename='payment-list')


urlpatterns = router.urls

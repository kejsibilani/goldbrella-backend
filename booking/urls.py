from rest_framework.routers import DefaultRouter

from booking.views import BookingViewSet

router = DefaultRouter(trailing_slash=False)

router.register(r'bookings', BookingViewSet, basename='booking')


urlpatterns = router.urls

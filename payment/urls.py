from rest_framework.routers import DefaultRouter

from payment.views import BookingPaymentViewSet


router = DefaultRouter(trailing_slash=False)

router.register(r'bookings/payments', BookingPaymentViewSet, basename='booking-payment')


urlpatterns = router.urls

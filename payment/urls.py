from rest_framework.routers import DefaultRouter

from payment.views import BookingPaymentReadViewSet

app_name = 'payment'

router = DefaultRouter(trailing_slash=False)
router.register(r'bookings/payments', BookingPaymentReadViewSet, basename='read-booking-payment')


urlpatterns = router.urls

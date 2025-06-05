from rest_framework.routers import DefaultRouter

app_name = 'payment'

router = DefaultRouter(trailing_slash=False)
# router.register(r'bookings/payments', BookingPaymentViewSet, basename='booking-payment')


urlpatterns = router.urls

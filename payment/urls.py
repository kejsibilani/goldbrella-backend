from django.urls import path
from rest_framework.routers import DefaultRouter

from payment.views import BookingPaymentReadViewSet
from payment.views.redirect import BookingFailureView
from payment.views.redirect import BookingSuccessView

app_name = 'payment'

router = DefaultRouter(trailing_slash=False)
router.register(r'bookings/payments', BookingPaymentReadViewSet, basename='read-booking-payment')


urlpatterns = [
    path('booking-success/<int:pk>', BookingSuccessView.as_view(), name='payment-success'),
    path('booking-failure/<int:pk>', BookingFailureView.as_view(), name='payment-failure'),
]

urlpatterns += router.urls

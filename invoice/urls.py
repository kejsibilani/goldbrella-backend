from rest_framework.routers import DefaultRouter

from invoice.views import BookingInvoiceViewSet

app_name = 'invoice'

router = DefaultRouter(trailing_slash=False)
router.register(r'bookings/invoices', BookingInvoiceViewSet, basename='invoice')


urlpatterns = router.urls

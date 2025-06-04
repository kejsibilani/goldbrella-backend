from rest_framework.routers import DefaultRouter

from invoice.serializers import BookingInvoiceSerializer

app_name = 'invoice'

router = DefaultRouter(trailing_slash=False)
router.register(r'invoices', BookingInvoiceSerializer, basename='invoice')


urlpatterns = router.urls

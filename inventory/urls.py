from rest_framework.routers import DefaultRouter

from inventory.views import InventoryViewSet


app_name = 'inventory'
router = DefaultRouter(trailing_slash=False)

router.register(r'inventory-items', InventoryViewSet, basename='inventory')


urlpatterns = router.urls

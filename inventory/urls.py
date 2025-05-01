from rest_framework.routers import DefaultRouter

from inventory.views import InventoryItemViewSet, InventoryItemNameListViewSet

app_name = 'inventory'
router = DefaultRouter(trailing_slash=False)

router.register(r'inventory-items/names', InventoryItemNameListViewSet, basename='inventory-item-name')
router.register(r'inventory-items', InventoryItemViewSet, basename='inventory-item')


urlpatterns = router.urls

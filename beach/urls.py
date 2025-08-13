from rest_framework.routers import DefaultRouter
from django.urls import path

from beach.views import BeachImageListViewSet
from beach.views import BeachImageViewSet
from beach.views import BeachOpeningHourListViewSet
from beach.views import BeachOpeningHourViewSet
from beach.views import BeachOpeningSeasonListViewSet
from beach.views import BeachOpeningSeasonViewSet
from beach.views import BeachSeasonOpeningHourListViewSet
from beach.views import BeachViewSet
from inventory.views import BeachInventoryItemListViewSet
from sunbed.views import BeachSunbedListViewSet
from zone.views import BeachZoneListViewSet

app_name = "beach"

router = DefaultRouter(trailing_slash=False)

# Image management
router.register('beach-images', BeachImageViewSet, basename='image')
router.register('beach-images-list', BeachImageListViewSet, basename='image-list')

# Opening hours
router.register('beach-opening-hours', BeachOpeningHourViewSet, basename='opening')
router.register('beach-opening-hours-list', BeachOpeningHourListViewSet, basename='opening-list')

# Opening seasons
router.register('beach-opening-seasons', BeachOpeningSeasonViewSet, basename='season')
router.register('beach-opening-seasons-list', BeachOpeningSeasonListViewSet, basename='season-list')
router.register('beach-season-opening-hours', BeachSeasonOpeningHourListViewSet, basename='opening-list-season')

# Core beach resources
router.register('beaches', BeachViewSet, basename='beach')
router.register('beach-zones', BeachZoneListViewSet, basename='zone-list')
router.register('beach-sunbeds', BeachSunbedListViewSet, basename='sunbed-list')
router.register('beach-inventory-items', BeachInventoryItemListViewSet, basename='inventory-item-list')

urlpatterns = router.urls

# Add explicit nested routes for beaches
urlpatterns += [
    path('beaches/<int:pk>/sunbeds', BeachSunbedListViewSet.as_view({'get': 'sunbeds'}), name='beach-sunbeds'),
    path('beaches/<int:pk>/opening-seasons', BeachOpeningSeasonViewSet.as_view({'get': 'list'}), name='beach-opening-seasons'),
    path('beaches/<int:pk>/opening-hours', BeachOpeningHourListViewSet.as_view({'get': 'open_hours'}), name='beach-opening-hours'),
    path('beaches/<int:pk>/inventory-items', BeachInventoryItemListViewSet.as_view({'get': 'inventory'}), name='beach-inventory-items'),
]

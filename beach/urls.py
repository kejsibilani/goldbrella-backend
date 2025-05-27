from rest_framework.routers import DefaultRouter

from beach.views import BeachViewSet
from beach.views import BeachImageViewSet, BeachImageListViewSet
from beach.views import BeachOpeningHourViewSet, BeachOpeningHourListViewSet
from beach.views import BeachOpeningSeasonViewSet, BeachOpeningSeasonListViewSet


app_name = "beach"

router = DefaultRouter(trailing_slash=False)

router.register('beaches/images', BeachImageViewSet, basename='image')
router.register('beaches/opening-hours', BeachOpeningHourViewSet, basename='opening')
router.register('beaches/opening-seasons', BeachOpeningSeasonViewSet, basename='season')
router.register('beaches', BeachImageListViewSet, basename='image-list')
router.register('beaches', BeachOpeningHourListViewSet, basename='opening-list')
router.register('beaches', BeachOpeningSeasonListViewSet, basename='season-list')
router.register('beaches', BeachViewSet, basename='beach')


urlpatterns = router.urls

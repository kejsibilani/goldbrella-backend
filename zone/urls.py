from rest_framework.routers import DefaultRouter

from sunbed.views import ZoneSunbedListViewSet
from zone.views import ZoneViewSet


app_name = 'zone'

router = DefaultRouter(trailing_slash=False)

router.register(r'zones', ZoneSunbedListViewSet, basename='sunbed-list')
router.register('zones', ZoneViewSet, basename='zone')


urlpatterns = router.urls

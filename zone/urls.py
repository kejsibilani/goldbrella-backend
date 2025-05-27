from rest_framework.routers import DefaultRouter

from zone.views import ZoneViewSet


app_name = 'zone'

router = DefaultRouter(trailing_slash=False)

router.register('zones', ZoneViewSet, basename='zone')


urlpatterns = router.urls

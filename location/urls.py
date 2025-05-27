from rest_framework.routers import DefaultRouter

from location.views import LocationViewSet


app_name = 'location'

router = DefaultRouter(trailing_slash=False)

router.register('locations', LocationViewSet, basename='location')


urlpatterns = router.urls

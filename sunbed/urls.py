from rest_framework.routers import DefaultRouter

from sunbed.views import SunbedViewSet

app_name = 'sunbed'

router = DefaultRouter(trailing_slash=False)
router.register(r'sunbeds', SunbedViewSet, basename='sunbed')


urlpatterns = router.urls

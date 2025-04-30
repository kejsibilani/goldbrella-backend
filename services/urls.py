from rest_framework.routers import DefaultRouter

from services.views import FacilityViewSet, RuleViewSet


app_name = 'services'
router = DefaultRouter(trailing_slash=False)

router.register('facilities', FacilityViewSet, basename='facility')
router.register('rules', RuleViewSet, basename='rule')


urlpatterns = router.urls

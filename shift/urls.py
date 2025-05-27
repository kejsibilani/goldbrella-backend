from rest_framework.routers import DefaultRouter

from shift.views import ShiftViewSet


app_name = 'shift'

router = DefaultRouter(trailing_slash=False)

router.register('shifts', ShiftViewSet, basename='shift')


urlpatterns = router.urls

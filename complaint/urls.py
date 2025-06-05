from rest_framework.routers import DefaultRouter

from complaint.views import ComplaintViewSet

app_name = "complaint",

router = DefaultRouter(trailing_slash=False)
router.register(r'complaints', ComplaintViewSet, basename='complaint')


urlpatterns = router.urls

from rest_framework.routers import DefaultRouter

from review.views import ReviewViewSet

app_name = 'review'

router = DefaultRouter(trailing_slash=False)
router.register(r'reviews', ReviewViewSet, basename='review')


urlpatterns = router.urls

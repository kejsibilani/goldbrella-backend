from rest_framework.routers import DefaultRouter

from notification.views import NotificationViewSet


app_name = 'notification'

router = DefaultRouter(trailing_slash=False)
router.register(r'notification', NotificationViewSet, basename='notification')


urlpatterns = router.urls

from rest_framework.routers import DefaultRouter

from mailer.views import ScheduledEmailViewSet

app_name = 'mailer'

router = DefaultRouter(trailing_slash=False)
router.register('scheduled-emails', ScheduledEmailViewSet, basename='scheduled-email')


urlpatterns = router.urls

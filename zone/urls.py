from rest_framework.routers import DefaultRouter
from django.urls import path

from sunbed.views import ZoneSunbedListViewSet
from zone.views import ZoneViewSet

app_name = 'zone'

router = DefaultRouter(trailing_slash=False)
router.register(r'zones', ZoneViewSet, basename='zone')


urlpatterns = router.urls

# Add explicit nested route for sunbeds under zones
urlpatterns += [
    path('zones/<int:pk>/sunbeds', ZoneSunbedListViewSet.as_view({'get': 'sunbeds'}), name='zone-sunbeds'),
]

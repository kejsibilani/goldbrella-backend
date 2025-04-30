from django.urls import path, include


app_name = 'api_v1'
urlpatterns = [
    path('', include(('account.urls', 'account'), namespace='account')),
    path('', include(('services.urls', 'services'), namespace='services')),
]

from django.urls import path, include


app_name = 'api_v1'
urlpatterns = [
    path('', include(('account.urls', 'account'), namespace='account')),
    path('', include(('beach.urls', 'beach'), namespace='beach')),
    path('', include(('location.urls', 'location'), namespace='location')),
    path('', include(('sunbed.urls', 'sunbed'), namespace='sunbed')),
    path('', include(('services.urls', 'services'), namespace='services')),
    path('', include(('invoice.urls', 'invoice'), namespace='invoice')),
    path('', include(('booking.urls', 'booking'), namespace='booking')),
    path('', include(('inventory.urls', 'inventory'), namespace='inventory')),
]

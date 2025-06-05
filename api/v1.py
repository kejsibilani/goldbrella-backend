from django.urls import path, include


app_name = 'api_v1'
urlpatterns = [
    path('', include(('account.urls', 'account'), namespace='account')),
    path('', include(('beach.urls', 'beach'), namespace='beach')),
    path('', include(('booking.urls', 'booking'), namespace='booking')),
    path('', include(('complaint.urls', 'complaint'), namespace='complaint')),
    path('', include(('inventory.urls', 'inventory'), namespace='inventory')),
    path('', include(('invoice.urls', 'invoice'), namespace='invoice')),
    path('', include(('location.urls', 'location'), namespace='location')),
    path('', include(('notification.urls', 'notification'), namespace='notification')),
    path('', include(('payment.urls', 'payment'), namespace='payment')),
    path('', include(('review.urls', 'review'), namespace='review')),
    path('', include(('services.urls', 'services'), namespace='services')),
    path('', include(('shift.urls', 'shift'), namespace='shift')),
    path('', include(('sunbed.urls', 'sunbed'), namespace='sunbed')),
    path('', include(('zone.urls', 'zone'), namespace='zone')),
]

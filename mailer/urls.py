from django.urls import path

from mailer.views import IndexView

app_name = 'mailer'
urlpatterns = [
    path('send-test-mail', IndexView.as_view(), name='send-mail'),
]

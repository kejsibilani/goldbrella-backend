from django.urls import path
from django_rest_passwordreset.urls import add_reset_password_urls_to_router
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenBlacklistView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.views import TokenVerifyView

from account.views import UserProfileView
from account.views import UserRegisterViewSet
from account.views import UserViewSet

app_name = "account"

router = DefaultRouter(trailing_slash=False)
router.register(r'register', UserRegisterViewSet, basename='register')
router.register(r'users', UserViewSet, basename='user')


urlpatterns = [
    path('login', TokenObtainPairView.as_view(), name='login'),
    path('verify', TokenVerifyView.as_view(), name='verify'),
    path('refresh', TokenRefreshView.as_view(), name='refresh'),
    path('logout', TokenBlacklistView.as_view(), name='logout'),
    path('profile', UserProfileView.as_view(), name='profile'),
]

add_reset_password_urls_to_router(router, base_path='reset-password')

urlpatterns += router.urls

from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenBlacklistView, TokenVerifyView, TokenRefreshView

from account.views import UserRegisterViewSet, UserProfileView, UserViewSet

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

urlpatterns += router.urls

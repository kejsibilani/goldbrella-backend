from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet

from account.models import User
from account.serializers import UserRegisterSerializer


class UserRegisterViewSet(CreateModelMixin, GenericViewSet):
    permission_classes = [AllowAny]
    serializer_class = UserRegisterSerializer
    queryset = User.objects.all()

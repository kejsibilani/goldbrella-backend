from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.filters import SearchFilter
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.viewsets import GenericViewSet

from account.filters import UserFilterSet
from account.models import User
from account.serializers import UserSerializer, UserDeletionQuerySerializer
from helpers.pagination import GenericPagination
from helpers.permissions import CustomDjangoModelPermissions


class UserViewSet(ListModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericViewSet):
    filter_backends = [DjangoFilterBackend, SearchFilter]
    permission_classes = [CustomDjangoModelPermissions]
    pagination_class = GenericPagination
    serializer_class = UserSerializer
    filterset_class = UserFilterSet
    search_fields = [
        'first_name', 'last_name', 'email',
        'phone_number', 'office_contact',
    ]

    def get_queryset(self):
        request_user = self.request.user
        if request_user.is_superuser:
            return User.objects.all()
        elif request_user.is_staff:
            return User.objects.filter(is_staff=False, is_superuser=False)
        return User.objects.filter(pk=request_user.pk, is_active=True)

    def perform_destroy(self, instance):
        # validate the query params
        query_serializer = UserDeletionQuerySerializer(data=self.request.GET)
        query_serializer.is_valid(raise_exception=True)
        # perform deletion based on query params
        deletion_type = query_serializer.data['deletion_type']
        email = query_serializer.data['email']
        if email == instance.email and deletion_type == 'soft':
            # raise not found on soft deletion
            if instance.is_active is False:
                raise NotFound({'detail': f"No User matches the given query."})
            instance.is_active = False
            return instance.save()
        elif email == instance.email and deletion_type == 'hard':
            return super().perform_destroy(instance)
        raise ValidationError({'email': 'Invalid email'})

from django.db.models import Q
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.response import Response

from account.models import User
from helpers.pagination import GenericPagination
from shift.filters import ShiftFilterSet
from shift.models import Shift
from shift.serializers import ShiftSerializer


# Create your views here.
class ShiftViewSet(viewsets.ModelViewSet):
    permission_classes = [DjangoModelPermissions]
    pagination_class = GenericPagination
    serializer_class = ShiftSerializer
    filterset_class = ShiftFilterSet

    def get_queryset(self):
        if self.request.user.has_role('admin'):
            return Shift.objects.all()
        elif self.request.user.has_role('supervisor'):
            return Shift.objects.filter(user=self.request.user)
        elif self.request.user.has_role('staff'):
            return Shift.objects.filter(user=self.request.user)
        return Shift.objects.none()


class UserShiftReadViewSet(viewsets.GenericViewSet):
    pagination_class = GenericPagination
    serializer_class = ShiftSerializer
    queryset = User.objects.filter(
        Q(
            Q(role='staff'),
            Q(role='supervisor'),
            _connector=Q.OR
        )
    )

    @action(detail=True, methods=['get'], url_path='shifts')
    def shifts(self, request, *args, **kwargs):
        # fetch instance
        user = self.get_object()
        # fetch shift for the user
        instance = getattr(user, 'shift', None)
        # raise Error if no instance found
        if not instance:
            raise ValidationError({'detail': 'No shift found for this user.'})
        # searialize and return instance
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

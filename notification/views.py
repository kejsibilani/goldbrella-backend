from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from helpers.pagination import GenericPagination
from notification.filters import NotificationFilterSet
from notification.models import Notification
from notification.serializers import NotificationSerializer


# Create your views here.
class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationSerializer
    filterset_class = NotificationFilterSet
    pagination_class = GenericPagination

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

    @action(detail=True, methods=['patch'], url_path='mark-read')
    def mark_read(self, request, *args, **kwargs):
        instance = self.get_object()
        # update the is_read field
        instance.is_read = True
        instance.save()
        # return okay response
        return Response(status=HTTP_200_OK)

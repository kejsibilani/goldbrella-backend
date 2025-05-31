from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

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

from rest_framework import viewsets

from helpers.pagination import GenericPagination
from helpers.permissions import CustomDjangoModelPermissions
from mailer.filters import ScheduledEmailFilterSet
from mailer.models import ScheduledEmail
from mailer.serializers import ScheduledEmailSerializer


# Create your views here.
class ScheduledEmailViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [CustomDjangoModelPermissions]
    serializer_class = ScheduledEmailSerializer
    filterset_class = ScheduledEmailFilterSet
    pagination_class = GenericPagination

    def get_queryset(self):
        request_user = self.request.user
        if request_user.is_superuser:
            return ScheduledEmail.objects.all()
        elif request_user.is_staff:
            return ScheduledEmail.objects.filter(system_generated=False)
        return ScheduledEmail.objects.none()

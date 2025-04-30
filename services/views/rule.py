from rest_framework import viewsets

from helpers.pagination import GenericPagination
from services.filters import RuleFilterSet
from services.models import Rule
from services.serializers import RuleSerializer


class RuleViewSet(viewsets.ModelViewSet):
    serializer_class = RuleSerializer
    pagination_class = GenericPagination
    filterset_class = RuleFilterSet
    queryset = Rule.objects.all()

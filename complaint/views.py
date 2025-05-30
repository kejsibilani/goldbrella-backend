from rest_framework import viewsets

from complaint.filters import ComplaintFilterSet
from complaint.models import Complaint
from complaint.serializers import ComplaintSerializer
from helpers.pagination import GenericPagination


# Create your views here.
class ComplaintViewSet(viewsets.ModelViewSet):
    serializer_class = ComplaintSerializer
    filterset_class = ComplaintFilterSet
    pagination_class = GenericPagination
    queryset = Complaint.objects.all()

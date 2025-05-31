from rest_framework import viewsets

from helpers.pagination import GenericPagination
from review.filters import ReviewFilterSet
from review.models import Review
from review.serializers import ReviewSerializer


# Create your views here.
class ReviewViewSet(viewsets.ModelViewSet):
    pagination_class = GenericPagination
    serializer_class = ReviewSerializer
    filterset_class = ReviewFilterSet

    def get_queryset(self):
        if self.action not in ['list', 'retrieve']:
            return Review.objects.filter(user=self.request.user)
        return Review.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

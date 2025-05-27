from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from beach.filters import BeachImageFilterSet
from beach.models import Beach
from beach.models import BeachImage
from beach.serializers import BeachImageSerializer
from helpers.pagination import GenericPagination


class BeachImageViewSet(viewsets.ModelViewSet):
    serializer_class = BeachImageSerializer
    filterset_class = BeachImageFilterSet
    pagination_class = GenericPagination
    queryset = BeachImage.objects.all()


class BeachImageListViewSet(viewsets.GenericViewSet):
    serializer_class = BeachImageSerializer
    pagination_class = GenericPagination
    queryset = Beach.objects.all()

    @action(detail=True, methods=['get'], url_path='images')
    def images(self, request, *args, **kwargs):
        # fetch instance
        beach = self.get_object()
        # fetch all images for the beach
        queryset = beach.images.all()
        # filter the queryset
        queryset = self.filter_queryset(queryset)
        # paginate the response
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

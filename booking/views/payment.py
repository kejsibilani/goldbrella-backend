from django.db.models import Q
from rest_framework.decorators import action
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from booking.models import Booking
from payment.serializers import BookingPaymentSerializer


class BookingPaymentListViewSet(GenericViewSet):
    permission_classes = [DjangoModelPermissions]
    serializer_class = BookingPaymentSerializer

    def get_queryset(self):
        request_user = self.request.user

        if request_user.is_superuser:
            return Booking.objects.all()
        elif request_user.is_staff:
            return Booking.objects.filter(
                Q(booked_by=request_user, user=request_user, _connector=Q.OR)
            )
        return Booking.objects.filter(user=request_user)

    @action(detail=True, methods=['get'], url_path='payments')
    def payments(self, request, *args, **kwargs):
        # fetch instance
        instance = self.get_object()
        # fetch the queryset
        queryset = instance.payments.all()
        # filter the queryset
        queryset = self.filter_queryset(queryset)
        # paginate the response
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
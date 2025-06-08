from rest_framework.generics import GenericAPIView
from rest_framework.response import Response


class BookingSuccessView(GenericAPIView):
    def get(self, request, *args, **kwargs):
        return Response({})

    def post(self, request, *args, **kwargs):
        return Response({})

    def patch(self, request, *args, **kwargs):
        return Response({})

    def put(self, request, *args, **kwargs):
        return Response({})

    def delete(self, request, *args, **kwargs):
        return Response({})


class BookingFailureView(GenericAPIView):
    def get(self, request, *args, **kwargs):
        return Response({})

    def post(self, request, *args, **kwargs):
        return Response({})

    def patch(self, request, *args, **kwargs):
        return Response({})

    def put(self, request, *args, **kwargs):
        return Response({})

    def delete(self, request, *args, **kwargs):
        return Response({})

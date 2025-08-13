from rest_framework_simplejwt.views import TokenBlacklistView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

class CustomLogoutView(TokenBlacklistView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        # Accept both JSON and form-urlencoded
        refresh = request.data.get('refresh')
        if not refresh:
            # Try form-urlencoded
            refresh = request.POST.get('refresh')
        if not refresh:
            return Response({'detail': 'Refresh token required.'}, status=status.HTTP_400_BAD_REQUEST)
        request.data['refresh'] = refresh
        return super().post(request, *args, **kwargs) 
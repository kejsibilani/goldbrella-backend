from django.conf import settings
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from mailer.scripts import schedule_email
from mailer.system import system_info


# Create your views here.
class IndexView(GenericAPIView):
    authentication_classes = ()
    permission_classes = ()

    def get(self, request, *args, **kwargs):
        schedule_email(
            to=['random9603@punkproof.com'],
            template_name='reset_password',
            company=system_info,
            **{
                'logo_link': 'https://img.freepik.com/free-vector/bird-colorful-logo-gradient-vector_343694-1365.jpg?semt=ais_hybrid',
                'password_link': 'http://xyz.com?token123',
                'support_link': 'http://xyz.com/support',
                'expiration_time': getattr(settings, 'DJANGO_REST_MULTITOKENAUTH_RESET_TOKEN_EXPIRY_TIME'),
                'user': request.user,
            }
        )
        return Response({})

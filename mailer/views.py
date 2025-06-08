from django.conf import settings
from django.http import HttpResponse
from django.views import View

from mailer.scripts import mailer
from mailer.system import system_info


# Create your views here.
class IndexView(View):
    @staticmethod
    def get(request, *args, **kwargs):
        mailer(
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

        # mailer.add_attachment()
        mailer.schedule()
        return HttpResponse()

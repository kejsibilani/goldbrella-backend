from django.contrib.auth.models import AnonymousUser as BaseAnonymousUser
from django.utils.deprecation import MiddlewareMixin
from django.utils.functional import SimpleLazyObject

from account.user import AnonymousUser


class AnonymousUserMiddleware(MiddlewareMixin):
    @staticmethod
    def process_request(request):
        if isinstance(request.user, BaseAnonymousUser):
            request.user = SimpleLazyObject(lambda: AnonymousUser())

            if hasattr(request, '_cached_user'):
                setattr(request, '_cached_user', SimpleLazyObject(lambda: AnonymousUser()))

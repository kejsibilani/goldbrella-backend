from django.contrib.auth.models import AnonymousUser as BaseAnonymousUser
from django.utils.deprecation import MiddlewareMixin
from django.utils.functional import SimpleLazyObject

from account.user import AnonymousUser


class AnonymousUserMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if isinstance(request.user, BaseAnonymousUser):
            request.user = SimpleLazyObject(lambda: AnonymousUser())

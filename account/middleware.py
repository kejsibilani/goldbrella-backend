from django.contrib.auth.models import AnonymousUser as BaseAnonymousUser
from django.utils.deprecation import MiddlewareMixin
from django.utils.functional import SimpleLazyObject


class AnonymousUser(BaseAnonymousUser):
    def has_role(self, role):
        return False


class AnonymousUserMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if isinstance(request.user, BaseAnonymousUser):
            request.user = SimpleLazyObject(lambda: AnonymousUser())

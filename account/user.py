from django.contrib.auth.models import AnonymousUser as BaseAnonymousUser


class AnonymousUser(BaseAnonymousUser):
    preferred_language = None
    phone_number = None
    address = None
    email = None
    role = None

    @staticmethod
    def has_role(role: str):
        return False

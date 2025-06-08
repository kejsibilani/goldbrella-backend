from django.contrib.auth.models import AnonymousUser as BaseAnonymousUser

from account.mixins import PermissionMixin


class AnonymousUser(PermissionMixin, BaseAnonymousUser):
    id = None
    pk = None
    role = ""
    email = ""
    username = ""
    address = None
    is_staff = False
    is_active = False
    phone_number = None
    is_superuser = False
    preferred_language = None

    @staticmethod
    def has_role(role: str):
        return False

    @staticmethod
    def get_full_name():
        return ""

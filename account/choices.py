from django.db import models


class UserRoleChoices(models.TextChoices):
    SUPERVISOR = ('supervisor', 'Supervisor')
    STAFF = ('staff', 'Staff')
    ADMIN = ('admin', 'Admin')
    GUEST = ('guest', 'Guest')

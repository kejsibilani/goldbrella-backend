from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from account.choices import UserRoleChoices
from account.managers import UserManager
from account.mixins import PermissionMixin
from beach.models import Beach


# Create your models here.
class User(PermissionMixin, AbstractUser):
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _("username"),
        max_length=150,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
        blank=True, null=True
    )
    email = models.EmailField(_("email address"), unique=True)
    role = models.CharField(max_length=50, choices=UserRoleChoices.choices)

    phone_number = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    preferred_language = models.CharField(max_length=20, null=True, blank=True)

    managed_beach = models.ForeignKey(
        Beach,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='staff_members',
        help_text='The beach this staff user manages. Null for non-staff or admin.'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name_plural = 'Users'
        verbose_name = 'User'

    def __str__(self):
        return self.email

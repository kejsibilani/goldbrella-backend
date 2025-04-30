from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from account.managers import UserManager


# Create your models here.
class User(AbstractUser):
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

    # Guest-specific fields
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    preferred_language = models.CharField(max_length=20, null=True, blank=True)

    # Staff-specific fields
    assigned_area = models.CharField(max_length=100, null=True, blank=True)

    # Management-specific fields
    department = models.CharField(max_length=100, null=True, blank=True)
    office_contact = models.CharField(max_length=15, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name_plural = 'Users'
        verbose_name = 'User'

    def __str__(self):
        return self.email

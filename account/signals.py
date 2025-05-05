from django.contrib.auth.models import Group, Permission
from django.db.models.signals import pre_save
from django.dispatch import receiver

from account.models import User
from account.settings import GUEST_USER_PERMISSION_SET, STAFF_USER_PERMISSION_SET


@receiver(pre_save, sender=User)
def ensure_permission_based_groups(instance, **kwargs):
    staff, sc = Group.objects.get_or_create(name='Staff')
    guest, gc = Group.objects.get_or_create(name='Guest')

    if sc: staff.permissions.set(
        Permission.objects.filter(codename__in=STAFF_USER_PERMISSION_SET)
    )
    if gc: guest.permissions.set(
        Permission.objects.filter(codename__in=GUEST_USER_PERMISSION_SET)
    )
    return

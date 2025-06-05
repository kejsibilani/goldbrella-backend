from datetime import datetime

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import localtime
from django_celery_beat.utils import make_aware

from account.models import User
from shift.models import Shift


@receiver(post_save, sender=User)
def create_shift_for_staff(instance, created, **kwargs):
    if created and (instance.has_role('supervisor') or instance.has_role('staff')):
        Shift.objects.get_or_create(
            user=instance,
            defaults={
                'zone': None,
                'start_time': localtime(
                    make_aware(
                        datetime(1979, 1, 1, 9, 0, 0)
                    )
                ),
                'end_time': localtime(
                    make_aware(
                        datetime(1979, 1, 1, 17, 0, 0)
                    )
                ),
            }
        )

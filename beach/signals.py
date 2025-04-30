from datetime import datetime

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import make_aware, localtime, localdate

from beach.choices import OpeningDayChoices
from beach.models import BeachOpeningSeason, Beach, BeachOpeningHour


current = make_aware(datetime.now())
@receiver(post_save, sender=Beach)
def create_season_for_beach(instance, created, **kwargs):
    if created: BeachOpeningSeason.objects.get_or_create(
        beach=instance,
        defaults={
            'opening_date': localdate(
                make_aware(
                    datetime(current.year, 5, current.day)
                )
            ),
            'closing_date': localdate(
                make_aware(
                    datetime(current.year, 9, current.day)
                )
            ),
        }
    )
    return


@receiver(post_save, sender=BeachOpeningSeason)
def create_hours_for_season(instance, created, **kwargs):
    if created:
        for day in OpeningDayChoices.values:
            BeachOpeningHour.objects.get_or_create(
                season=instance,
                weekday=day,
                defaults={
                    'opening_time': localtime(
                        make_aware(
                            datetime(current.year, current.month, current.day,9, 0, 0)
                        )
                    ),
                    'closing_time': localtime(
                        make_aware(
                            datetime(current.year, current.month, current.day,20, 0, 0)
                        )
                    ),
                }
            )
    return

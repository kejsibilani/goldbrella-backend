from django.conf import settings
from django.db import models


# Create your models here.
class Shift(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()

    zone = models.ForeignKey(
        to='zone.Zone',
        on_delete=models.SET_NULL,
        related_name='shifts',
        null=True
    )

    user = models.OneToOneField(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='shift'
    )

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Shifts'
        verbose_name = 'Shift'

    def __str__(self):
        return f'{self.user} | {self.zone}'

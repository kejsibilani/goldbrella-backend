from django.conf import settings
from django.db import models

from zone.choices import ZoneLocationChoices


# Create your models here.
class Zone(models.Model):
    location = models.CharField(max_length=50, choices=ZoneLocationChoices.choices)

    supervisor = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="supervised_zones",
        null=True
    )

    beach = models.ForeignKey(
        to='beach.Beach',
        on_delete=models.CASCADE,
        related_name="zones"
    )

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Zones'
        verbose_name = 'Zone'
        constraints = [
            models.UniqueConstraint(
                fields=['location', 'beach'],
                name='unique_zone_location'
            )
        ]

    def __str__(self):
        return f'{self.location} - {self.beach.title}'

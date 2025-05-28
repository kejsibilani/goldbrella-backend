from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.db.models.functions import Upper

from sunbed.choices import SunbedStatusChoices
from sunbed.choices import SunbedTypeChoices


# Sunbed Model
class Sunbed(models.Model):
    sunbed_type = models.CharField(
        max_length=20,
        choices=SunbedTypeChoices.choices,
        default=SunbedTypeChoices.STANDARD.value
    )
    area = models.CharField(max_length=20)
    identity = models.CharField(max_length=5)
    price = models.DecimalField(
        max_digits=10, decimal_places=2,
        validators=[
            MinValueValidator(Decimal(0)),
        ],
    )
    status = models.CharField(
        max_length=20,
        choices=SunbedStatusChoices.choices,
        default=SunbedStatusChoices.AVAILABLE.value
    )

    zone = models.ForeignKey(
        to='zone.Zone',
        on_delete=models.CASCADE,
        related_name="sunbeds"
    )

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Sunbeds"
        verbose_name = "Sunbed"
        constraints = [
            models.UniqueConstraint(
                Upper('area'), Upper('identity'), 'zone',
                name='unique_sunbed_per_zone'
            ),
        ]

    def __str__(self):
        return f"Sunbed {self.id} - {self.zone.beach.title}"

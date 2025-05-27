from django.db import models
from django.db.models.functions import Lower
from pytz import country_names


class Location(models.Model):
    country = models.CharField(max_length=5, choices=country_names.items())
    city = models.CharField(max_length=100)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Locations"
        verbose_name = "Location"
        constraints = [
            models.UniqueConstraint(
                Lower('city'), 'country',
                name='unique_locations'
            ),
        ]

    def __str__(self):
        return f"{self.city}, {self.country}"

from django.db import models

class Beach(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    location = models.ForeignKey(
        to='location.Location',
        on_delete=models.CASCADE,
        related_name="beaches"
    )

    facilities = models.ManyToManyField(
        to='services.Facility',
        related_name="beaches",
        blank=True
    )
    rules = models.ManyToManyField(
        to='services.Rule',
        related_name="beaches",
        blank=True
    )

    image = models.ImageField(upload_to='beach_images/', null=True, blank=True)

    code = models.CharField(max_length=32, unique=True, null=True, blank=True, help_text="Unique code for QR or direct access")

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Beaches"
        verbose_name = "Beach"
        constraints = [
            models.UniqueConstraint(
                fields=['latitude', 'longitude', 'location'],
                name='unique_beach_per_location'
            ),
        ]

    def __str__(self):
        return self.title

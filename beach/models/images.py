from django.db import models

from beach.helpers import beach_image_filepath


class BeachImage(models.Model):
    image = models.ImageField(upload_to=beach_image_filepath)

    beach = models.ForeignKey(
        to='beach.Beach',
        on_delete=models.CASCADE,
        related_name="images"
    )

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Beach Images"
        verbose_name = 'Beach Image'

    def __str__(self):
        return self.image.url

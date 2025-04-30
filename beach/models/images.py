from django.db import models


class BeachImage(models.Model):
    link = models.URLField()

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
        constraints = [
            models.UniqueConstraint(
                fields=['link', 'beach'],
                name='unique_image_per_beach'
            ),
        ]

    def __str__(self):
        return self.link

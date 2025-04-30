from django.db import models


class BeachOpeningSeason(models.Model):
    beach = models.OneToOneField(
        "beach.Beach",
        on_delete=models.CASCADE,
        related_name="season"
    )

    opening_date = models.DateField()
    closing_date = models.DateField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Beach Opening Seasons"
        verbose_name = "Beach Opening Season"

    def __str__(self):
        return f'{self.beach} | {self.opening_date.month} - {self.closing_date.month}'

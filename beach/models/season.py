from django.db import models


class BeachOpeningSeason(models.Model):
    title = models.CharField(max_length=200)

    opening_date = models.DateField()
    closing_date = models.DateField()

    beach = models.ForeignKey(
        "beach.Beach",
        on_delete=models.CASCADE,
        related_name="seasons"
    )

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Beach Opening Seasons"
        verbose_name = "Beach Opening Season"
        constraints = [
            models.UniqueConstraint(
                fields=('beach', 'opening_date', 'closing_date'),
                name="unique_opening_season"
            )
        ]

    def __str__(self):
        return f'{self.beach} | {self.opening_date.month} - {self.closing_date.month}'

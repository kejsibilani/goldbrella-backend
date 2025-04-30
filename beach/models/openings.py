from django.db import models

from beach.choices import OpeningDayChoices


class BeachOpeningHour(models.Model):
    season = models.ForeignKey(
        to='beach.BeachOpeningSeason',
        on_delete=models.CASCADE,
        related_name="opening_hours"
    )

    weekday = models.CharField(max_length=20, choices=OpeningDayChoices.choices)  # Monday, Tuesday, etc.
    opening_time = models.TimeField()
    closing_time = models.TimeField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Beach Opening Times"
        verbose_name = "Beach Opening Time"
        constraints = [
            models.UniqueConstraint(
                fields=['season', 'weekday'],
                name='unique_opening_per_season'
            ),
        ]

    def __str__(self):
        return (
            f"{self.season.beach.title} | {self.weekday} "
            f"({self.opening_time} to {self.closing_time})"
        )

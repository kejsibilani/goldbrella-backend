from django.db import models
from django.db.models.functions import Lower


class Rule(models.Model):
    name = models.CharField(max_length=250)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Rules"
        verbose_name = "Rule"
        constraints = [
            models.UniqueConstraint(
                Lower('name'),
                name='unique_rules'
            ),
        ]

    def __str__(self):
        return self.name

from django.db.models import Q
from rest_framework import serializers

from account.models import User


class UserForeignKey(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        context_user = self.context["request"].user
        if context_user.is_superuser:
            return User.objects.all()
        elif context_user.is_staff:
            return User.objects.filter(
                Q(
                    Q(pk=context_user.pk),
                    Q(is_staff=False, is_superuser=False, _connector=Q.AND),
                    _connector=Q.OR
                )
            )
        return User.objects.filter(pk=context_user.pk)

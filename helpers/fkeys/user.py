from django.db.models import Q
from rest_framework import serializers

from account.models import User


class UserPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        context_user = self.context["request"].user

        if context_user.has_role('admin'):
            return User.objects.all()
        elif context_user.has_role('staff'):
            return User.objects.filter(
                Q(
                    pk=context_user.pk,
                    role='guest',
                    _connector=Q.OR
                )
            )
        elif context_user.has_role('supervisor'):
            return User.objects.filter(
                Q(
                    pk=context_user.pk,
                    role='guest',
                    _connector=Q.OR
                )
            )
        return User.objects.filter(pk=context_user.pk)

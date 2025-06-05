from django.contrib.auth.models import Group
from rest_framework import serializers

from account.models import User


class BookingUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            'id', 'email', 'password', 'role', 'first_name', 'last_name',
            'phone_number', 'address', 'preferred_language'
        )
        read_only_fields = ('role',)
        extra_kwargs = {
            'password': {
                'write_only': True,
                'required': False,
            },
        }

    def create(self, validated_data):
        # extract email field
        email = validated_data.pop('email')
        # extract password field
        password = validated_data.pop('password', None)
        # create user
        user, _ = User.objects.get_or_create(
            email=email,
            role='guest',
            defaults=validated_data
        )
        # set password on user
        user.set_password(password)
        user.save()
        # set user group
        user.groups.set(
            Group.objects.filter(name__iexact='guest')
        )
        # return user
        return user

    def update(self, instance, validated_data):
        # extract email field
        validated_data.pop('email', None)
        # extract password field
        password = validated_data.pop('password', None)
        # update user
        user = super().update(instance, validated_data)
        # set password on user
        if password:
            user.set_password(password)
            user.save()
        # return user
        return user

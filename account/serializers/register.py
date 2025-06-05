from django.contrib.auth.models import Group
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from account.models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'email', 'password', 'role', 'first_name', 'last_name',
            'phone_number', 'address', 'preferred_language'
        )
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'password': {
                'write_only': True,
                'required': True,
                'validators': [
                    validate_password,
                ],
            },
            'email': {
                'required': True,
                'validators': [
                    UniqueValidator(queryset=User.objects.all()),
                ],
            }
        }

    def validate(self, attrs):
        # check request user is superuser
        context_user = getattr(self.context.get('request'), 'user', None)
        is_superuser = context_user.has_role('admin') if context_user else False
        # fetch role from attrs
        role = attrs.get('role', 'guest')
        # add condition for adding role
        if not is_superuser and not (role == 'guest'):
            raise serializers.ValidationError({'detail': 'Only guest users can register themselves.'})
        # add user group
        groups = Group.objects.filter(name__iexact=role)
        attrs['groups'] = groups
        return attrs

    def create(self, validated_data):
        # extract password field
        password = validated_data.pop('password', None)
        # create user
        user = super().create(validated_data)
        # set password on user
        user.set_password(password)
        user.save()
        # return user
        return user

from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from account.models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=('guest', 'staff', 'admin'), write_only=True)

    class Meta:
        model = User
        fields = (
            'id', 'email', 'password', 'role', 'first_name', 'last_name',
            'phone_number', 'address', 'preferred_language', 'assigned_area',
            'department', 'office_contact'
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
                    UniqueValidator(queryset=User.objects.all())
                ],
            }
        }

    def validate(self, attrs):
        # check request user is superuser
        is_superuser = getattr(getattr(self.context.get('request'), 'user', None), 'is_superuser', False)
        # fetch role from attrs
        role = attrs.pop('role', 'guest')
        # add condition for adding role
        if not is_superuser and not (role == 'guest'):
            raise serializers.ValidationError({'detail': 'Only guest users can register themselves.'})
        # is_staff for staff user and is_superuser for admin user
        if role == 'staff': attrs['is_staff'] = True
        elif role == 'admin': attrs['is_superuser'] = True

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

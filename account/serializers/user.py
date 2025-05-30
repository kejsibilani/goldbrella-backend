from rest_framework import serializers

from account.models import User


class UserDeletionQuerySerializer(serializers.Serializer):
    deletion_type = serializers.ChoiceField(choices=('hard', 'soft'), default='soft')
    email = serializers.EmailField(required=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'email', 'first_name', 'last_name', 'role',
            'phone_number', 'address', 'preferred_language',
        )
        read_only_fields = ('email', 'role')

from rest_framework import serializers

from account.models import User


class UserDeletionQuerySerializer(serializers.Serializer):
    deletion_type = serializers.ChoiceField(choices=('hard', 'soft'), default='soft')
    email = serializers.EmailField(required=True)


class UserSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id', 'email', 'first_name', 'last_name', 'role',
            'phone_number', 'address', 'preferred_language',
            'assigned_area', 'department', 'office_contact',
        )
        read_only_fields = ('email', 'role')

    @staticmethod
    def get_role(obj):
        if obj.is_superuser:
            return 'admin'
        elif obj.is_staff:
            return 'staff'
        return 'guest'

from rest_framework import serializers

from account.models import User


class UserProfileSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id', 'email', 'role', 'first_name', 'last_name', 'phone_number',
            'address', 'preferred_language'
        )
        read_only_fields = ('email', 'role')

    @staticmethod
    def get_role(obj):
        if obj.is_superuser:
            return 'admin'
        elif obj.is_staff:
            return 'staff'
        return 'guest'

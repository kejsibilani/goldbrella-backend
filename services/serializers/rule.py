from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from services.models import Rule


class RuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rule
        fields = '__all__'
        extra_kwargs = {
            'name': {
                'validators': [
                    UniqueValidator(queryset=Rule.objects.all(), lookup='iexact')
                ]
            }
        }

from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'phone_number', 'civic_score', 'account_type', 'language', 'is_id_verified']
        read_only_fields = ['id', 'civic_score', 'is_id_verified']

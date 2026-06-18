from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import DidYouKnowFact, FAQ, MP, PublicEvent, CrimeReport, VotingRecord

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'phone_number', 'email', 'civic_score', 'account_type', 'language', 'is_id_verified', 'date_joined']

class DidYouKnowFactSerializer(serializers.ModelSerializer):
    class Meta:
        model = DidYouKnowFact
        fields = ['id', 'title', 'content', 'image_url', 'category', 'year', 'created_at']

class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ['id', 'question', 'answer', 'category', 'views', 'helpful_count', 'not_helpful_count', 'created_at']

class MPSerializer(serializers.ModelSerializer):
    class Meta:
        model = MP
        fields = ['id', 'name', 'constituency', 'party']

class PublicEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicEvent
        fields = '__all__'

class CrimeReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrimeReport
        fields = ['id', 'category', 'description', 'location', 'status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'status', 'created_at', 'updated_at']

class VotingRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = VotingRecord
        fields = '__all__'

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['phone_number', 'email', 'password', 'password_confirm', 'language']
    
    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({"password": "Passwords do not match"})
        return data
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField(write_only=True)

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=8)
    confirm_password = serializers.CharField(required=True)
    
    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "New passwords do not match"})
        return data

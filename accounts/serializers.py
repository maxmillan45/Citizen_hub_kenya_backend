from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import (
    DidYouKnowFact, FAQ, MP, PublicEvent, CrimeReport, 
    VotingRecord, MPPerformance, EventAttendance, MpesaTransaction
)

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'phone_number', 'email', 'civic_score', 'account_type', 'language', 'is_id_verified', 'date_joined']
        read_only_fields = ['id', 'civic_score', 'date_joined']

class DidYouKnowFactSerializer(serializers.ModelSerializer):
    class Meta:
        model = DidYouKnowFact
        fields = ['id', 'title', 'content', 'image_url', 'category', 'year', 'created_at']

class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ['id', 'question', 'answer', 'category', 'views', 'helpful_count', 'not_helpful_count', 'created_at']
        read_only_fields = ['id', 'views', 'helpful_count', 'not_helpful_count', 'created_at']

    def validate_question(self, value):
        if len(value) < 10:
            raise serializers.ValidationError("Question too short (minimum 10 characters)")
        return value

class MPSerializer(serializers.ModelSerializer):
    class Meta:
        model = MP
        fields = ['id', 'name', 'constituency', 'party', 'term_start', 'term_end', 'photo_url', 'contact_phone', 'contact_email']
        read_only_fields = ['id']

class PublicEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicEvent
        fields = ['id', 'title', 'description', 'date', 'location', 'category', 'organizer', 'is_free', 'fee_amount', 'created_at']
        read_only_fields = ['id', 'created_at']

class CrimeReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrimeReport
        fields = ['id', 'category', 'description', 'location', 'status', 'reported_by', 'created_at', 'updated_at']
        read_only_fields = ['id', 'status', 'created_at', 'updated_at']

    def validate_description(self, value):
        if len(value) < 20:
            raise serializers.ValidationError("Description too short (minimum 20 characters)")
        return value

class VotingRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = VotingRecord
        fields = ['id', 'user', 'election_type', 'voted_at', 'status']
        read_only_fields = ['id', 'voted_at']

class MPPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = MPPerformance
        fields = '__all__'

class EventAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventAttendance
        fields = '__all__'

class MpesaTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MpesaTransaction
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

from rest_framework import serializers
from .models import User, DidYouKnowFact, FAQ, MP, MPPerformance

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'phone_number', 'civic_score', 'account_type', 'language', 'is_id_verified']
        read_only_fields = ['id', 'civic_score', 'is_id_verified']

class DidYouKnowFactSerializer(serializers.ModelSerializer):
    class Meta:
        model = DidYouKnowFact
        fields = '__all__'

class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = '__all__'

class MPSerializer(serializers.ModelSerializer):
    class Meta:
        model = MP
        fields = '__all__'

class MPPerformanceSerializer(serializers.ModelSerializer):
    mp_name = serializers.CharField(source='mp.name', read_only=True)
    constituency = serializers.CharField(source='mp.constituency', read_only=True)
    
    class Meta:
        model = MPPerformance
        fields = '__all__'

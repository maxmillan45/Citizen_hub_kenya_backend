from rest_framework import serializers
from .models import Conversation

class ConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = ['id', 'question', 'answer', 'language', 'sources', 'helpful', 'created_at']
# Chatbot serializers convert conversation data to JSON format

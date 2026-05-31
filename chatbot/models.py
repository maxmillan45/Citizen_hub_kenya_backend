from django.db import models
from django.conf import settings

class Conversation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='conversations')
    question = models.TextField()
    answer = models.TextField()
    language = models.CharField(max_length=5, default='en')
    sources = models.JSONField(default=list)
    helpful = models.BooleanField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.phone_number}: {self.question[:50]}"
# Chatbot models store all user questions and AI responses for conversation history
# Conversation model for storing user chatbot interactions

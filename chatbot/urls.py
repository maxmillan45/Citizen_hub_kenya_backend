from django.urls import path
from .views import AskChatbotView, ConversationHistoryView

urlpatterns = [
    path('ask/', AskChatbotView.as_view(), name='ask-chatbot'),
    path('history/', ConversationHistoryView.as_view(), name='chatbot-history'),
]

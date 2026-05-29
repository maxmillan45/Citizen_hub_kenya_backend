from django.urls import path
from .views import AskChatbotView, ConversationHistoryView, RateAnswerView

urlpatterns = [
    path('ask/', AskChatbotView.as_view(), name='chatbot-ask'),
    path('history/', ConversationHistoryView.as_view(), name='chatbot-history'),
    path('rate/', RateAnswerView.as_view(), name='chatbot-rate'),
]

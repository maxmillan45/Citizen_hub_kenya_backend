from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, status
from django.conf import settings
from .models import Conversation
from .serializers import ConversationSerializer
from constitution.models import Article
import re

class AskChatbotView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        question = request.data.get('question')
        language = request.data.get('language', 'en')
        
        if not question:
            return Response({'error': 'Question is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Search for relevant articles
            articles = self._find_relevant_articles(question)
            sources = [article.article_number for article in articles]
            
            # Generate response
            answer = self._generate_response(question, language, articles)
            
            # Save conversation
            conversation = Conversation.objects.create(
                user=request.user,
                question=question,
                answer=answer,
                language=language,
                sources=sources
            )
            
            return Response({
                'question': question,
                'answer': answer,
                'sources': sources,
                'conversation_id': conversation.id
            })
            
        except Exception as e:
            print(f"Chatbot error: {e}")
            return Response({
                'error': 'Sorry, I could not process your question. Please try again.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def _find_relevant_articles(self, question):
        # Try exact match first
        articles = Article.objects.filter(full_text__icontains=question)[:3]
        if articles:
            return articles
        
        # Try by keywords
        keywords = self._extract_keywords(question)
        for keyword in keywords:
            articles = Article.objects.filter(full_text__icontains=keyword)[:3]
            if articles:
                return articles
        
        return []
    
    def _extract_keywords(self, question):
        question_lower = question.lower()
        keywords = []
        legal_terms = [
            'right', 'rights', 'arrest', 'police', 'land', 'property',
            'employment', 'health', 'education', 'family', 'voting',
            'corruption', 'privacy', 'dignity', 'equality'
        ]
        for term in legal_terms:
            if term in question_lower:
                keywords.append(term)
        return keywords[:3]
    
    def _generate_response(self, question, language, articles):
        if articles:
            sources = [a.article_number for a in articles]
            article_texts = []
            for article in articles:
                article_texts.append(f"Article {article.article_number}: {article.full_text[:300]}")
            
            if language == 'sw':
                return f"Nimepata habari katika Katiba ya Kenya. Hapa kuna maelezo kutoka Kifungu {', '.join(sources)}:\n\n" + "\n\n".join(article_texts) + "\n\nTafadhali rejelea Katiba kwa maelezo kamili."
            else:
                return f"I found information in the Constitution of Kenya. Here is what it says in Article(s) {', '.join(sources)}:\n\n" + "\n\n".join(article_texts) + "\n\nPlease refer to the constitution for complete details."
        else:
            fallbacks = self._get_fallback(question, language)
            return fallbacks
    
    def _get_fallback(self, question, language):
        question_lower = question.lower()
        
        responses = {
            'arrest': "Under Article 49 of the Constitution of Kenya, arrested persons have the right to remain silent, the right to a lawyer, and the right to be informed of the charges. Article 50 guarantees the right to a fair hearing.",
            'land': "Article 40 of the Constitution of Kenya protects the right to property. Article 67 establishes the National Land Commission to manage land matters.",
            'employment': "Article 41 of the Constitution of Kenya protects labour rights including fair labour practices and the right to form trade unions.",
            'health': "Article 43 of the Constitution of Kenya provides for economic and social rights including the right to health and healthcare services.",
            'education': "Article 43 of the Constitution of Kenya provides for the right to education. The state must ensure access to basic education.",
            'family': "Article 45 of the Constitution of Kenya recognizes the family as the natural and fundamental unit of society.",
            'voting': "Article 38 of the Constitution of Kenya guarantees the right to participate in elections and to vote.",
            'corruption': "Chapter Six of the Constitution of Kenya provides for leadership and integrity, including anti-corruption measures.",
            'privacy': "Article 31 of the Constitution of Kenya protects the right to privacy.",
            'dignity': "Article 28 of the Constitution of Kenya recognizes and protects human dignity.",
            'equality': "Article 27 of the Constitution of Kenya guarantees equality and freedom from discrimination.",
        }
        
        for topic, response_text in responses.items():
            if topic in question_lower:
                return f"The Constitution of Kenya states: {response_text}"
        
        if language == 'sw':
            return "Samahani, siwezi kujibu swali lako. Tafadhali rejelea Katiba ya Kenya kwa maelezo kamili au uliza swali lako kwa njia tofauti."
        else:
            return "I'm sorry, I cannot answer your question. Please refer to the Constitution of Kenya for complete details or rephrase your question."


class ConversationHistoryView(generics.ListAPIView):
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Conversation.objects.filter(user=self.request.user).order_by('-created_at')

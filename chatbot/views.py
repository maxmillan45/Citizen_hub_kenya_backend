from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from constitution.models import Article
from .models import Conversation
from .serializers import ConversationSerializer

class AskChatbotView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        question = request.data.get('question', '')
        language = request.data.get('language', 'en')
        
        if not question:
            return Response({'error': 'Question is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Build search query from question
        q_lower = question.lower()
        
        # Create broader search conditions
        search_conditions = Q()
        
        # Search for exact phrases
        if "arrest" in q_lower or "police arrest" in q_lower or "criminal" in q_lower:
            search_conditions |= Q(article_number='49')
            search_conditions |= Q(title__icontains='arrest')
        
        if "privacy" in q_lower or "phone" in q_lower or "search" in q_lower:
            search_conditions |= Q(article_number='31')
            search_conditions |= Q(title__icontains='privacy')
        
        if "land" in q_lower or "property" in q_lower or "house" in q_lower:
            search_conditions |= Q(article_number='40')
            search_conditions |= Q(title__icontains='property')
        
        if "health" in q_lower or "hospital" in q_lower:
            search_conditions |= Q(article_number='43')
            search_conditions |= Q(title__icontains='health')
        
        if "education" in q_lower or "school" in q_lower:
            search_conditions |= Q(article_number='43')
            search_conditions |= Q(title__icontains='education')
        
        if "discrimination" in q_lower or "equal" in q_lower:
            search_conditions |= Q(article_number='27')
            search_conditions |= Q(title__icontains='discrimination')
        
        if "torture" in q_lower or "cruel" in q_lower:
            search_conditions |= Q(article_number='29')
            search_conditions |= Q(title__icontains='torture')
        
        # Also search by content
        search_conditions |= Q(full_text__icontains=q_lower[:100])
        search_conditions |= Q(simplified_english__icontains=q_lower[:100])
        
        articles = Article.objects.filter(search_conditions).distinct()[:5]
        
        sources = []
        context = ""
        
        for article in articles:
            context += f"Article {article.article_number}: {article.simplified_english}\n\n"
            sources.append(article.article_number)
        
        if not sources and ("phone" in q_lower or "search" in q_lower):
            # Force privacy article for phone search questions
            try:
                privacy_article = Article.objects.get(article_number='31')
                context = f"Article 31: {privacy_article.simplified_english}\n\n"
                sources = ["31"]
            except Article.DoesNotExist:
                pass
        
        if sources:
            answer = f"Based on the Constitution of Kenya:\n\n{context}\n\nThis information is for educational purposes. Consult a lawyer for legal advice."
        else:
            answer = "I cannot answer this question specifically from the Constitution. Please consult a legal professional for advice on this matter."
        
        conversation = Conversation.objects.create(
            user=request.user,
            question=question,
            answer=answer,
            language=language,
            sources=sources
        )
        
        return Response({
            'answer': answer,
            'sources': sources,
            'conversation_id': conversation.id
        })

class ConversationHistoryView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        conversations = Conversation.objects.filter(user=request.user).order_by('-created_at')[:20]
        serializer = ConversationSerializer(conversations, many=True)
        return Response(serializer.data)

class RateAnswerView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        conversation_id = request.data.get('conversation_id')
        helpful = request.data.get('helpful')
        
        try:
            conversation = Conversation.objects.get(id=conversation_id, user=request.user)
            conversation.helpful = helpful
            conversation.save()
            return Response({'message': 'Thank you for your feedback'})
        except Conversation.DoesNotExist:
            return Response({'error': 'Conversation not found'}, status=status.HTTP_404_NOT_FOUND)
# Chatbot views: ask question, conversation history, rate answers

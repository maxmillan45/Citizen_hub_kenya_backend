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
        
        # Search for relevant articles in the database
        articles = Article.objects.filter(
            Q(full_text__icontains=question) |
            Q(simplified_english__icontains=question) |
            Q(title__icontains=question) |
            Q(article_number__icontains=question)
        )[:5]
        
        # Build response from found articles
        sources = []
        context = ""
        
        for article in articles:
            context += f"Article {article.article_number}: {article.simplified_english}\n\n"
            sources.append(article.article_number)
        
        # Generate answer based on matched articles
        if sources:
            answer = f"Based on the Constitution of Kenya:\n\n{context}\n\nThis information is for educational purposes. Consult a lawyer for legal advice."
        else:
            # Fallback answers for common questions without exact matches
            q_lower = question.lower()
            if "arrest" in q_lower or "police" in q_lower:
                answer = "Under Article 49 of the Kenyan Constitution, if you are arrested you have the right to: be informed why you are arrested, remain silent, call a lawyer, and be brought to court within 24 hours."
            elif "privacy" in q_lower or "phone" in q_lower:
                answer = "Under Article 31 of the Kenyan Constitution, you have the right to privacy. Police generally need a warrant to search your phone or home."
            elif "property" in q_lower or "land" in q_lower:
                answer = "Under Article 40 of the Kenyan Constitution, you have the right to own property. The government can only take your land for public use with fair compensation."
            else:
                answer = "I cannot answer this question specifically from the Constitution. Please consult a legal professional for advice on this matter."
        
        # Save conversation
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

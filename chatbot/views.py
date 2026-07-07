from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import generics, status
from django.conf import settings
from .models import Conversation
from .serializers import ConversationSerializer
from constitution.models import Article
import openai
import re

class AskChatbotView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        question = request.data.get('question')
        language = request.data.get('language', 'en')
        
        if not question:
            return Response({'error': 'Question is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Try to use OpenAI first
            openai_api_key = settings.OPENAI_API_KEY
            
            if openai_api_key:
                try:
                    client = openai.OpenAI(api_key=openai_api_key)
                    response = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": f"You are a legal assistant specializing in the Constitution of Kenya. Answer questions about Kenyan law, rights, and governance. Respond in {'Swahili' if language == 'sw' else 'English'}."},
                            {"role": "user", "content": question}
                        ],
                        max_tokens=500,
                        temperature=0.7
                    )
                    answer = response.choices[0].message.content
                    sources = []
                    
                    # Try to find relevant articles
                    articles = Article.objects.filter(
                        full_text__icontains=question
                    )[:3]
                    sources = [article.article_number for article in articles]
                    
                except Exception as e:
                    print(f"OpenAI error: {e}")
                    # Fallback to local search
                    answer = self._generate_fallback_response(question, language)
                    articles = Article.objects.filter(
                        full_text__icontains=question
                    )[:3]
                    sources = [article.article_number for article in articles]
            else:
                # No OpenAI key, use fallback
                answer = self._generate_fallback_response(question, language)
                articles = Article.objects.filter(
                    full_text__icontains=question
                )[:3]
                sources = [article.article_number for article in articles]
            
            # If no articles found, search by keywords
            if not sources:
                keywords = self._extract_keywords(question)
                for keyword in keywords:
                    articles = Article.objects.filter(
                        full_text__icontains=keyword
                    )[:3]
                    if articles:
                        sources = [article.article_number for article in articles]
                        break
            
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
    
    def _extract_keywords(self, question):
        # Extract keywords from question
        question_lower = question.lower()
        keywords = []
        
        # Common legal keywords
        legal_terms = [
            'right', 'rights', 'arrest', 'police', 'land', 'property', 'employment',
            'health', 'education', 'family', 'voting', 'corruption', 'privacy',
            'dignity', 'equality', 'discrimination', 'life', 'security', 'freedom',
            'speech', 'assembly', 'religion', 'movement', 'information', 'justice'
        ]
        
        for term in legal_terms:
            if term in question_lower:
                keywords.append(term)
        
        # If no keywords found, use the whole question
        if not keywords:
            keywords = [question_lower[:50]]
        
        return keywords
    
    def _generate_fallback_response(self, question, language):
        # Search for relevant articles
        articles = Article.objects.filter(
            full_text__icontains=question
        )[:5]
        
        if articles:
            sources = [a.article_number for a in articles]
            if language == 'sw':
                return f"Kulingana na Katiba ya Kenya, nimepata habari katika Kifungu {', '.join(sources)}. Hizi ndizo vifungu vinavyohusiana na swali lako. Tafadhali rejelea Katiba kwa maelezo kamili."
            else:
                return f"Based on the Constitution of Kenya, I found relevant information in Article(s) {', '.join(sources)}. These are the articles related to your question. Please refer to the constitution for complete details."
        else:
            # Search by topic
            topics = {
                'arrest': "Under the Constitution of Kenya, Article 49 provides rights for arrested persons including the right to remain silent, right to a lawyer, and right to be informed of the charges.",
                'land': "Article 40 of the Constitution of Kenya protects the right to property. Article 67 establishes the National Land Commission.",
                'employment': "Article 41 of the Constitution of Kenya protects labour rights including fair labour practices and the right to form trade unions.",
                'health': "Article 43 of the Constitution of Kenya provides for economic and social rights including the right to health and healthcare services.",
                'education': "Article 43 of the Constitution of Kenya provides for the right to education.",
                'family': "Article 45 of the Constitution of Kenya recognizes the family as the natural and fundamental unit of society.",
                'voting': "Article 38 of the Constitution of Kenya guarantees the right to participate in elections and to vote.",
                'corruption': "Chapter Six of the Constitution of Kenya provides for leadership and integrity, including anti-corruption measures.",
                'privacy': "Article 31 of the Constitution of Kenya protects the right to privacy.",
                'dignity': "Article 28 of the Constitution of Kenya recognizes and protects human dignity.",
                'equality': "Article 27 of the Constitution of Kenya guarantees equality and freedom from discrimination.",
                'speech': "Article 33 of the Constitution of Kenya protects freedom of expression.",
                'assembly': "Article 37 of the Constitution of Kenya protects the right to assemble and demonstrate.",
                'religion': "Article 32 of the Constitution of Kenya protects freedom of religion and belief.",
                'information': "Article 35 of the Constitution of Kenya guarantees the right to access information.",
                'justice': "Article 48 of the Constitution of Kenya ensures access to justice for all persons."
            }
            
            question_lower = question.lower()
            for topic, response_text in topics.items():
                if topic in question_lower:
                    if language == 'sw':
                        return f"Katiba ya Kenya inasema: {response_text}"
                    return f"The Constitution of Kenya states: {response_text}"
            
            if language == 'sw':
                return "Samahani, siwezi kujibu swali lako. Tafadhali uliza swali lako kwa njia tofauti au rejelea mhasibu wa sheria."
            else:
                return "I'm sorry, I cannot answer your question. Please rephrase your question or consult a legal professional."

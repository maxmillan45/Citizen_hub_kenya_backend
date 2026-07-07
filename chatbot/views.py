from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.conf import settings
from .models import Conversation
from .serializers import ConversationSerializer
from constitution.models import Article
import openai
import re
import time

class AskChatbotView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        question = request.data.get('question')
        language = request.data.get('language', 'en')
        
        if not question:
            return Response({'error': 'Question is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Search for relevant articles first (fast)
            articles = self._find_relevant_articles(question)
            sources = [article.article_number for article in articles]
            
            # Try to use OpenAI if available
            answer = self._get_answer(question, language, articles)
            
            # If answer is None, use fallback
            if answer is None:
                answer = self._generate_fallback_response(question, language, articles)
            
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
            import traceback
            traceback.print_exc()
            
            # Return a helpful fallback response
            fallback = self._get_fallback_answer(question, language)
            return Response({
                'question': question,
                'answer': fallback,
                'sources': [],
                'conversation_id': None
            })
    
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
        
        # Try by topic
        topic = self._get_topic(question)
        if topic:
            articles = Article.objects.filter(topic=topic)[:3]
            if articles:
                return articles
        
        return []
    
    def _extract_keywords(self, question):
        question_lower = question.lower()
        keywords = []
        legal_terms = [
            'right', 'rights', 'arrest', 'police', 'land', 'property', 
            'employment', 'health', 'education', 'family', 'voting', 
            'corruption', 'privacy', 'dignity', 'equality', 'discrimination',
            'life', 'security', 'freedom', 'speech', 'assembly', 'religion',
            'movement', 'information', 'justice', 'court', 'judge', 'law'
        ]
        for term in legal_terms:
            if term in question_lower:
                keywords.append(term)
        return keywords[:3]
    
    def _get_topic(self, question):
        question_lower = question.lower()
        topics = {
            'rights': ['right', 'rights', 'freedom', 'dignity', 'equality'],
            'land': ['land', 'property', 'environment'],
            'government': ['president', 'parliament', 'cabinet', 'judiciary'],
            'citizenship': ['citizen', 'citizenship', 'passport']
        }
        for topic, keywords in topics.items():
            if any(kw in question_lower for kw in keywords):
                return topic
        return None
    
    def _get_answer(self, question, language, articles):
        try:
            openai_api_key = settings.OPENAI_API_KEY
            if not openai_api_key:
                return None
            
            # Build context from articles
            context = ""
            for article in articles:
                context += f"Article {article.article_number}: {article.full_text[:500]}\n\n"
            
            if not context:
                context = "The Constitution of Kenya"
            
            system_prompt = f"""You are a legal assistant specializing in the Constitution of Kenya. 
            Answer the user's question based on the following context:
            
            {context}
            
            If the question is not answered by the context, say so clearly and suggest what the constitution says on related topics.
            Respond in {'Swahili' if language == 'sw' else 'English'}.
            Keep your response clear, concise, and helpful."""
            
            client = openai.OpenAI(api_key=openai_api_key)
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": question}
                ],
                max_tokens=300,
                temperature=0.7,
                timeout=10
            )
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"OpenAI error: {e}")
            return None
    
    def _generate_fallback_response(self, question, language, articles):
        if articles:
            sources = [a.article_number for a in articles]
            if language == 'sw':
                return f"Kulingana na Katiba ya Kenya, nimepata habari katika Kifungu {', '.join(sources)}. Hizi ndizo vifungu vinavyohusiana na swali lako. Tafadhali rejelea Katiba kwa maelezo kamili."
            else:
                return f"Based on the Constitution of Kenya, I found relevant information in Article(s) {', '.join(sources)}. These are the articles related to your question. Please refer to the constitution for complete details."
        else:
            return self._get_fallback_answer(question, language)
    
    def _get_fallback_answer(self, question, language):
        question_lower = question.lower()
        
        # Common legal topics
        responses = {
            'arrest': "Under the Constitution of Kenya, Article 49 provides rights for arrested persons including the right to remain silent, right to a lawyer, and right to be informed of the charges. Article 50 guarantees the right to a fair hearing.",
            'land': "Article 40 of the Constitution of Kenya protects the right to property. Article 67 establishes the National Land Commission. The Constitution also provides for land reform and protection of land rights.",
            'employment': "Article 41 of the Constitution of Kenya protects labour rights including fair labour practices, the right to form trade unions, and the right to strike.",
            'health': "Article 43 of the Constitution of Kenya provides for economic and social rights including the right to health and healthcare services. The state must ensure access to healthcare for all.",
            'education': "Article 43 of the Constitution of Kenya provides for the right to education. The state must ensure access to basic education for all children.",
            'family': "Article 45 of the Constitution of Kenya recognizes the family as the natural and fundamental unit of society. It protects marriage and family rights.",
            'voting': "Article 38 of the Constitution of Kenya guarantees the right to participate in elections and to vote. Every citizen has the right to free, fair and regular elections.",
            'corruption': "Chapter Six of the Constitution of Kenya provides for leadership and integrity, including anti-corruption measures. The Ethics and Anti-Corruption Commission is established to fight corruption.",
            'privacy': "Article 31 of the Constitution of Kenya protects the right to privacy, including privacy of the home, correspondence, and personal data.",
            'dignity': "Article 28 of the Constitution of Kenya recognizes and protects human dignity. Every person has inherent dignity and the right to have that dignity respected.",
            'equality': "Article 27 of the Constitution of Kenya guarantees equality and freedom from discrimination. The state must take measures to ensure equality.",
            'speech': "Article 33 of the Constitution of Kenya protects freedom of expression, including freedom of the press and media.",
            'assembly': "Article 37 of the Constitution of Kenya protects the right to assemble, demonstrate, picket, and present petitions to public authorities.",
            'religion': "Article 32 of the Constitution of Kenya protects freedom of religion, belief, and conscience.",
            'information': "Article 35 of the Constitution of Kenya guarantees the right to access information held by the state.",
            'justice': "Article 48 of the Constitution of Kenya ensures access to justice for all persons. The state must ensure that justice is accessible to all.",
        }
        
        for topic, response_text in responses.items():
            if topic in question_lower:
                if language == 'sw':
                    return f"Katiba ya Kenya inasema: {response_text}"
                return f"The Constitution of Kenya states: {response_text}"
        
        if language == 'sw':
            return "Samahani, siwezi kujibu swali lako kwa uhakika. Tafadhali rejelea Katiba ya Kenya au wasiliana na mwanasheria kwa ushauri wa kisheria."
        else:
            return "I'm sorry, I cannot answer your question with certainty. Please refer to the Constitution of Kenya or consult a legal professional for legal advice."

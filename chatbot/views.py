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
        
        # Chapter questions
        if "chapter" in q_lower or "chapters" in q_lower or "structure" in q_lower:
            # Return all chapter info
            chapters_article = """
            The Constitution of Kenya 2010 has 18 Chapters:
            
            Chapter 1: Sovereignty of the People and Supremacy of this Constitution (Articles 1-4)
            Chapter 2: The Republic (Articles 5-10)
            Chapter 3: Citizenship (Articles 11-18)
            Chapter 4: The Bill of Rights (Articles 19-59)
            Chapter 5: Land and Environment (Articles 60-68)
            Chapter 6: Leadership and Integrity (Articles 73-80)
            Chapter 7: Representation of the People (Articles 81-100)
            Chapter 8: The Legislature (Articles 93-122)
            Chapter 9: The Executive (Articles 129-155)
            Chapter 10: The Judiciary (Articles 159-173)
            Chapter 11: Devolved Government (Articles 174-190)
            Chapter 12: Public Finance (Articles 201-222)
            Chapter 13: The Public Service (Articles 232-239)
            Chapter 14: National Security (Articles 238-247)
            Chapter 15: Commissions and Independent Offices (Articles 248-254)
            Chapter 16: Amendment of this Constitution (Articles 255-257)
            Chapter 17: General Provisions (Articles 258-263)
            Chapter 18: Transitional and Consequential Provisions (Articles 262-264)
            """
            answer = chapters_article
            sources = ["Constitution of Kenya 2010 - Full Document"]
            
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
        
        # General constitution questions
        if "what is the constitution" in q_lower or "about the constitution" in q_lower or "tell me about constitution" in q_lower:
            answer = """
            The Constitution of Kenya 2010 is the supreme law of Kenya. It was promulgated on August 27, 2010.
            
            Key features include:
            - Bill of Rights (Chapter 4) protecting fundamental freedoms
            - Devolution creating 47 county governments
            - Separation of powers between Executive, Legislature, and Judiciary
            - Independent commissions and offices
            - Land and environment provisions
            - Leadership and integrity requirements for public officers
            
            It transformed Kenya's governance structure and expanded citizen participation in democracy.
            """
            sources = ["Constitution of Kenya 2010 - Preamble and Overview"]
            
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
        
        # Rights questions
        if "rights" in q_lower or "fundamental rights" in q_lower or "bill of rights" in q_lower:
            if "what are my rights" in q_lower or "list of rights" in q_lower:
                answer = """
                The Bill of Rights (Chapter 4, Articles 19-59) guarantees these fundamental rights:
                
                Article 26: Right to life
                Article 27: Equality and freedom from discrimination
                Article 28: Human dignity
                Article 29: Freedom and security of the person
                Article 30: Freedom from slavery and forced labor
                Article 31: Privacy
                Article 32: Freedom of conscience, religion, belief and opinion
                Article 33: Freedom of expression
                Article 34: Freedom of the media
                Article 35: Access to information
                Article 36: Freedom of association
                Article 37: Assembly, demonstration, picketing and petition
                Article 38: Political rights
                Article 39: Freedom of movement and residence
                Article 40: Protection of right to property
                Article 41: Labor relations
                Article 42: Clean and healthy environment
                Article 43: Economic and social rights (education, health, housing)
                Article 44: Cultural rights
                Article 45: Family rights
                Article 46: Consumer rights
                Article 47: Fair administrative action
                Article 48: Access to justice
                Article 49: Rights of arrested persons
                Article 50: Fair hearing
                """
                sources = ["Articles 26-50, Constitution of Kenya 2010"]
                
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
        
        # Specific keyword searches
        if "arrest" in q_lower or "police arrest" in q_lower or "criminal" in q_lower:
            search_conditions |= Q(article_number='49')
            search_conditions |= Q(title__icontains='arrest')
        
        if "privacy" in q_lower or "phone" in q_lower or "search my phone" in q_lower:
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
        
        if "vote" in q_lower or "election" in q_lower or "political" in q_lower:
            search_conditions |= Q(article_number='38')
            search_conditions |= Q(title__icontains='political')
        
        if "expression" in q_lower or "speak" in q_lower or "opinion" in q_lower:
            search_conditions |= Q(article_number='33')
            search_conditions |= Q(title__icontains='expression')
        
        if "fair hearing" in q_lower or "court" in q_lower or "justice" in q_lower:
            search_conditions |= Q(article_number='50')
            search_conditions |= Q(title__icontains='hearing')
        
        if "life" in q_lower or "death penalty" in q_lower:
            search_conditions |= Q(article_number='26')
            search_conditions |= Q(title__icontains='life')
        
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
            # Better fallback message
            answer = f"I understand you're asking about '{question}'. To get the best answer, please try:\n\n1. Asking about specific rights (e.g., 'right to privacy')\n2. Mentioning specific articles (e.g., 'Article 31')\n3. Asking about topics like: arrest, privacy, land, health, education, voting, expression, or fair hearing\n\nFor general constitutional information, ask 'What are the chapters of the constitution?'"
        
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

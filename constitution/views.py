from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.db.models import Q
from .models import Article

class ArticleSearchView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        query = request.query_params.get('q', '')
        try:
            if query:
                articles = Article.objects.filter(
                    Q(full_text__icontains=query) |
                    Q(simplified_english__icontains=query) |
                    Q(title__icontains=query) |
                    Q(article_number__icontains=query)
                )
            else:
                articles = Article.objects.all()
            
            # Manual serialization - same pattern as working history endpoint
            data = []
            for a in articles:
                data.append({
                    'id': a.id,
                    'article_number': a.article_number,
                    'chapter': a.chapter,
                    'title': a.title,
                    'full_text': a.full_text,
                    'simplified_english': a.simplified_english,
                    'simplified_swahili': a.simplified_swahili,
                    'topic': a.topic,
                    'view_count': a.view_count,
                })
            return Response(data)
        except Exception as e:
            return Response({'error': str(e)}, status=500)

class ArticleDetailView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, article_number):
        try:
            article = Article.objects.get(article_number=article_number)
            data = {
                'id': article.id,
                'article_number': article.article_number,
                'chapter': article.chapter,
                'title': article.title,
                'full_text': article.full_text,
                'simplified_english': article.simplified_english,
                'simplified_swahili': article.simplified_swahili,
                'topic': article.topic,
                'view_count': article.view_count,
            }
            return Response(data)
        except Article.DoesNotExist:
            return Response({'error': 'Article not found'}, status=404)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.db.models import Q
from .models import Article
from .serializers import ArticleSerializer

class ArticleSearchView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        query = request.query_params.get('q', '')
        if query:
            articles = Article.objects.filter(
                Q(full_text__icontains=query) |
                Q(simplified_english__icontains=query) |
                Q(simplified_swahili__icontains=query)
            )
        else:
            articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

class ArticleDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, article_number):
        try:
            article = Article.objects.get(article_number=article_number)
            article.view_count += 1
            article.save()
            serializer = ArticleSerializer(article)
            return Response(serializer.data)
        except Article.DoesNotExist:
            return Response({'error': 'Article not found'}, status=status.HTTP_404_NOT_FOUND)


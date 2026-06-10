from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.db.models import Q, Count
from .models import Article
from .serializers import ArticleSerializer

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
            article.view_count += 1
            article.save()
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


class PopularArticlesView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        articles = Article.objects.order_by('-view_count')[:10]
        data = [{'id': a.id, 'article_number': a.article_number, 'title': a.title, 'view_count': a.view_count} for a in articles]
        return Response(data)


class ArticleCategoriesView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        categories = Article.TOPIC_CHOICES
        data = []
        for value, label in categories:
            count = Article.objects.filter(topic=value).count()
            data.append({
                'value': value,
                'label': label,
                'count': count
            })
        return Response(data)


class BookmarkArticleView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, article_id):
        try:
            article = Article.objects.get(id=article_id)
            bookmarks = request.session.get('bookmarks', [])
            if article_id not in bookmarks:
                bookmarks.append(article_id)
                request.session['bookmarks'] = bookmarks
            return Response({'message': 'Article bookmarked'})
        except Article.DoesNotExist:
            return Response({'error': 'Article not found'}, status=404)
    
    def delete(self, request, article_id):
        bookmarks = request.session.get('bookmarks', [])
        if article_id in bookmarks:
            bookmarks.remove(article_id)
            request.session['bookmarks'] = bookmarks
        return Response({'message': 'Bookmark removed'})


class BookmarksListView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        bookmarks = request.session.get('bookmarks', [])
        articles = Article.objects.filter(id__in=bookmarks)
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

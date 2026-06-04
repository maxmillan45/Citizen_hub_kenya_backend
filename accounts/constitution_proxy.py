from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from constitution.models import Article
from constitution.serializers import ArticleSerializer

class ConstitutionSearchProxy(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        query = request.query_params.get('q', '')
        if query:
            from django.db.models import Q
            articles = Article.objects.filter(
                Q(full_text__icontains=query) |
                Q(simplified_english__icontains=query) |
                Q(title__icontains=query)
            )
        else:
            articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

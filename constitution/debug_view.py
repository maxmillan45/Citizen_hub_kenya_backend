from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
import traceback

class DebugView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        try:
            from .models import Article
            from .serializers import ArticleSerializer
            
            articles = Article.objects.all()
            serializer = ArticleSerializer(articles, many=True)
            return Response({
                'success': True,
                'count': len(serializer.data),
                'data': serializer.data[:3]
            })
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e),
                'traceback': traceback.format_exc()
            }, status=500)

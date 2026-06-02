from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import DidYouKnowFact, FAQ, MP

class LoadDataView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        try:
            history_count = DidYouKnowFact.objects.count()
            faq_count = FAQ.objects.count()
            mp_count = MP.objects.count()
            
            return Response({
                'history_count': history_count,
                'faq_count': faq_count,
                'mp_count': mp_count,
                'message': 'Data status retrieved successfully'
            })
        except Exception as e:
            return Response({
                'error': str(e),
                'message': 'Database tables may not exist yet. Run migrations first.'
            }, status=500)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser

class ScraperStatusView(APIView):
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        return Response({
            'status': 'Scraper is running',
            'message': 'Scraper endpoints are available'
        })

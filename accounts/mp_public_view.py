from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import MP
from .serializers import MPSerializer

class PublicMPListView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        mps = MP.objects.all()
        serializer = MPSerializer(mps, many=True)
        return Response({
            'count': mps.count(),
            'results': serializer.data
        })

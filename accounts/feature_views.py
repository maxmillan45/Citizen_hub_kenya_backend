from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import DidYouKnowFact, FAQ, MP
from .serializers import DidYouKnowFactSerializer, FAQSerializer, MPSerializer

class DidYouKnowListView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        facts = DidYouKnowFact.objects.all().order_by('-id')
        serializer = DidYouKnowFactSerializer(facts, many=True)
        return Response(serializer.data)

class DidYouKnowRandomView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        import random
        count = DidYouKnowFact.objects.count()
        if count == 0:
            return Response({'error': 'No facts available'}, status=404)
        random_index = random.randint(0, count - 1)
        fact = DidYouKnowFact.objects.all()[random_index]
        serializer = DidYouKnowFactSerializer(fact)
        return Response(serializer.data)

class FAQListView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        category = request.query_params.get('category')
        queryset = FAQ.objects.all()
        if category:
            queryset = queryset.filter(category=category)
        serializer = FAQSerializer(queryset, many=True)
        return Response(serializer.data)

class MPListView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        mps = MP.objects.all()
        serializer = MPSerializer(mps, many=True)
        return Response(serializer.data)

class EventListView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        return Response([])

class CrimeReportView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        return Response({'message': 'Crime report submitted'}, status=201)
    
    def get(self, request):
        return Response([])

class VotingStatusView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        return Response({'status': 'Not verified'})
EOFcat > accounts/feature_views.py << 'EOF'
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import DidYouKnowFact, FAQ, MP
from .serializers import DidYouKnowFactSerializer, FAQSerializer, MPSerializer

class DidYouKnowListView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        facts = DidYouKnowFact.objects.all().order_by('-id')
        serializer = DidYouKnowFactSerializer(facts, many=True)
        return Response(serializer.data)

class DidYouKnowRandomView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        import random
        count = DidYouKnowFact.objects.count()
        if count == 0:
            return Response({'error': 'No facts available'}, status=404)
        random_index = random.randint(0, count - 1)
        fact = DidYouKnowFact.objects.all()[random_index]
        serializer = DidYouKnowFactSerializer(fact)
        return Response(serializer.data)

class FAQListView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        category = request.query_params.get('category')
        queryset = FAQ.objects.all()
        if category:
            queryset = queryset.filter(category=category)
        serializer = FAQSerializer(queryset, many=True)
        return Response(serializer.data)

class MPListView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        mps = MP.objects.all()
        serializer = MPSerializer(mps, many=True)
        return Response(serializer.data)

class EventListView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        return Response([])

class CrimeReportView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        return Response({'message': 'Crime report submitted'}, status=201)
    
    def get(self, request):
        return Response([])

class VotingStatusView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        return Response({'status': 'Not verified'})

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import DidYouKnowFact, FAQ, MP, PublicEvent

class DidYouKnowListView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        facts = DidYouKnowFact.objects.all().order_by('-id')
        data = [{'id': f.id, 'title': f.title, 'content': f.content, 'image_url': f.image_url, 'category': f.category, 'year': f.year} for f in facts]
        return Response(data)

class DidYouKnowRandomView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        import random
        count = DidYouKnowFact.objects.count()
        if count == 0:
            return Response({'error': 'No facts available'}, status=404)
        random_index = random.randint(0, count - 1)
        fact = DidYouKnowFact.objects.all()[random_index]
        data = {'id': fact.id, 'title': fact.title, 'content': fact.content, 'image_url': fact.image_url, 'category': fact.category, 'year': fact.year}
        return Response(data)

class FAQListView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        category = request.query_params.get('category')
        queryset = FAQ.objects.all()
        if category:
            queryset = queryset.filter(category=category)
        data = [{'id': f.id, 'question': f.question, 'answer': f.answer, 'category': f.category} for f in queryset]
        return Response(data)

class MPListView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        mps = MP.objects.all()
        data = [{'id': m.id, 'name': m.name, 'constituency': m.constituency, 'party': m.party} for m in mps]
        return Response(data)

class EventListView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        events = PublicEvent.objects.filter(is_active=True).order_by('event_date')
        data = []
        for e in events:
            data.append({
                'id': e.id,
                'name': e.name,
                'event_type': e.event_type,
                'description': e.description,
                'event_date': e.event_date,
                'county': e.county,
                'location': e.location,
                'start_time': e.start_time.strftime('%H:%M') if e.start_time else None,
                'end_time': e.end_time.strftime('%H:%M') if e.end_time else None,
            })
        return Response(data)

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

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.db.models import Q
from .models import MP, MPPerformance

class MPSearchView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        query = request.query_params.get('q', '')
        if query:
            mps = MP.objects.filter(
                Q(name__icontains=query) |
                Q(constituency__icontains=query) |
                Q(party__icontains=query)
            )
        else:
            mps = MP.objects.all()
        
        data = [{'id': m.id, 'name': m.name, 'constituency': m.constituency, 'party': m.party} for m in mps]
        return Response(data)


class MPCompareView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        ids = request.query_params.get('ids', '')
        if not ids:
            return Response({'error': 'MP IDs required'}, status=400)
        
        mp_ids = [int(id) for id in ids.split(',')]
        mps = MP.objects.filter(id__in=mp_ids)
        
        data = []
        for mp in mps:
            performances = MPPerformance.objects.filter(mp=mp).order_by('-year')
            data.append({
                'id': mp.id,
                'name': mp.name,
                'constituency': mp.constituency,
                'party': mp.party,
                'performances': [{'year': p.year, 'attendance': p.attendance, 'grade': p.grade} for p in performances]
            })
        return Response(data)


class MPPerformanceDetailView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, mp_id):
        try:
            mp = MP.objects.get(id=mp_id)
            performances = MPPerformance.objects.filter(mp=mp).order_by('-year')
            data = {
                'mp': {'id': mp.id, 'name': mp.name, 'constituency': mp.constituency, 'party': mp.party},
                'performances': [{
                    'year': p.year,
                    'attendance': p.attendance,
                    'bills_sponsored': p.bills_sponsored,
                    'bills_passed': p.bills_passed,
                    'projects_completed': p.projects_completed,
                    'grade': p.grade
                } for p in performances]
            }
            return Response(data)
        except MP.DoesNotExist:
            return Response({'error': 'MP not found'}, status=404)

from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import FAQ, MP, PublicEvent, CrimeReport
from .serializers import FAQSerializer, MPSerializer, CrimeReportSerializer
from django.http import HttpResponse
import csv

class FAQDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer
    permission_classes = [permissions.AllowAny]
    
    def delete(self, request, *args, **kwargs):
        faq = self.get_object()
        if hasattr(faq, 'soft_delete'):
            faq.soft_delete()
        else:
            faq.delete()
        return Response({"message": "FAQ deleted"}, status=status.HTTP_204_NO_CONTENT)

class MPDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MP.objects.all()
    serializer_class = MPSerializer
    permission_classes = [permissions.AllowAny]  # Changed to public

class BulkFAQDeleteView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        ids = request.data.get('ids', [])
        if not ids:
            return Response({"error": "No IDs provided"}, status=400)
        
        deleted_count = FAQ.objects.filter(id__in=ids).count()
        FAQ.objects.filter(id__in=ids).delete()
        
        return Response({
            "message": f"Successfully deleted {deleted_count} FAQs",
            "deleted_count": deleted_count
        })

class ExportCrimeReportsView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        reports = CrimeReport.objects.all()
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="crime_reports.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['ID', 'Category', 'Description', 'Location', 'Status', 'Created At'])
        
        for report in reports:
            writer.writerow([report.id, report.category, report.description, 
                           report.location, report.status, report.created_at])
        
        return response
from .models import PublicEvent
from .serializers import PublicEventSerializer

class EventDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PublicEvent.objects.all()
    serializer_class = PublicEventSerializer
    permission_classes = [permissions.AllowAny]
from .models import PublicEvent
from .serializers import PublicEventSerializer

class EventDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PublicEvent.objects.all()
    serializer_class = PublicEventSerializer
    permission_classes = [permissions.AllowAny]

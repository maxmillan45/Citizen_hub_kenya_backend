from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model
from .models import CrimeReport, FAQ

User = get_user_model()

class AdminStatsView(APIView):
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        now = timezone.now()
        week_ago = now - timedelta(days=7)
        
        total_users = User.objects.count()
        new_users_week = User.objects.filter(date_joined__gte=week_ago).count()
        
        total_crimes = CrimeReport.objects.count()
        crimes_by_category = CrimeReport.objects.values('category').annotate(count=Count('id'))
        
        total_faqs = FAQ.objects.count()
        
        stats = {
            'users': {
                'total': total_users,
                'new_last_7_days': new_users_week,
            },
            'crime_reports': {
                'total': total_crimes,
                'by_category': crimes_by_category,
            },
            'faqs': {
                'total': total_faqs,
            },
            'timestamp': now.isoformat(),
        }
        
        return Response(stats)

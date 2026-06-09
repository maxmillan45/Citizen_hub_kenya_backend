from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import User, CrimeReport, EventAttendance

class UserStatisticsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        
        # Get civic points from user model
        civic_points = user.civic_score
        
        # Count reports filed by this user
        reports_filed = CrimeReport.objects.filter(user=user).count()
        
        # Count events attended by this user
        events_attended = EventAttendance.objects.filter(user=user).count()
        
        return Response({
            'civic_points': civic_points,
            'reports_filed': reports_filed,
            'events_attended': events_attended,
            'user_level': self.get_user_level(civic_points),
            'next_level_points': self.get_next_level_points(civic_points)
        })
    
    def get_user_level(self, points):
        if points < 100:
            return 'Bronze Citizen'
        elif points < 300:
            return 'Silver Citizen'
        elif points < 600:
            return 'Gold Citizen'
        else:
            return 'Platinum Citizen'
    
    def get_next_level_points(self, points):
        if points < 100:
            return 100 - points
        elif points < 300:
            return 300 - points
        elif points < 600:
            return 600 - points
        else:
            return 0

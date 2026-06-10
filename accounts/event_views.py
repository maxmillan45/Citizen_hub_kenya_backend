from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.utils import timezone
from .models import PublicEvent

class UpcomingEventsView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        events = PublicEvent.objects.filter(
            event_date__gte=timezone.now().date(),
            is_active=True
        ).order_by('event_date')
        
        data = [{
            'id': e.id,
            'name': e.name,
            'event_type': e.event_type,
            'description': e.description,
            'event_date': e.event_date,
            'county': e.county,
            'location': e.location,
            'start_time': e.start_time,
            'end_time': e.end_time,
        } for e in events]
        return Response(data)


class EventCountiesView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        counties = PublicEvent.objects.filter(is_active=True).values_list('county', flat=True).distinct()
        data = []
        for county in counties:
            count = PublicEvent.objects.filter(county=county, is_active=True).count()
            data.append({'county': county, 'event_count': count})
        return Response(data)


class SetEventReminderView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, event_id):
        try:
            event = PublicEvent.objects.get(id=event_id)
            reminders = request.session.get('event_reminders', [])
            if event_id not in reminders:
                reminders.append(event_id)
                request.session['event_reminders'] = reminders
            return Response({'message': f'Reminder set for {event.name}'})
        except PublicEvent.DoesNotExist:
            return Response({'error': 'Event not found'}, status=404)

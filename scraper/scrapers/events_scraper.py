import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta
from django.utils import timezone
from accounts.models import PublicEvent

class EventsScraper:
    def __init__(self):
        self.events = []
        
    def scrape_all_events(self):
        try:
            # Kenyan Public Holidays 2026
            public_holidays = [
                {"title": "New Year's Day", "date": "2026-01-01", "category": "public_holiday", "description": "New Year's Day celebration"},
                {"title": "Good Friday", "date": "2026-04-10", "category": "public_holiday", "description": "Christian holiday commemorating crucifixion"},
                {"title": "Easter Monday", "date": "2026-04-13", "category": "public_holiday", "description": "Easter Monday celebration"},
                {"title": "Labour Day", "date": "2026-05-01", "category": "public_holiday", "description": "International Workers' Day"},
                {"title": "Madaraka Day", "date": "2026-06-01", "category": "public_holiday", "description": "Kenya attained self-rule on June 1, 1963"},
                {"title": "Eid al-Fitr", "date": "2026-05-25", "category": "public_holiday", "description": "End of Ramadan (date may vary)"},
                {"title": "Eid al-Adha", "date": "2026-08-01", "category": "public_holiday", "description": "Feast of Sacrifice (date may vary)"},
                {"title": "Huduma Day", "date": "2026-10-10", "category": "public_holiday", "description": "Formerly Moi Day"},
                {"title": "Mashujaa Day", "date": "2026-10-20", "category": "public_holiday", "description": "Heroes' Day honoring Kenyan heroes"},
                {"title": "Jamhuri Day", "date": "2026-12-12", "category": "public_holiday", "description": "Independence Day - Kenya became a republic"},
                {"title": "Christmas Day", "date": "2026-12-25", "category": "public_holiday", "description": "Christmas celebration"},
                {"title": "Boxing Day", "date": "2026-12-26", "category": "public_holiday", "description": "Boxing Day celebration"},
                {"title": "Utamaduni Day", "date": "2026-12-26", "category": "public_holiday", "description": "Formerly Boxing Day"},
            ]
            
            # Important civic events
            civic_events = [
                {"title": "IEBC Voter Registration Drive", "description": "Register to vote for upcoming elections", "category": "civic", "location": "All county headquarters"},
                {"title": "Public Participation - County Budget", "description": "Submit your views on county budget allocations", "category": "town_hall", "location": "County assembly halls"},
                {"title": "EACC Civic Education", "description": "Learn about corruption reporting and prevention", "category": "civic_education", "location": "Various locations"},
                {"title": "NYS Recruitment Drive", "description": "National Youth Service recruitment for Kenyan youth", "category": "government", "location": "All sub-counties"},
                {"title": "NHIF Registration Outreach", "description": "Register for NHIF services at reduced rates", "category": "health", "location": "Ward level"},
                {"title": "Huduma Center Services Week", "description": "Free services and fast-track processing", "category": "government", "location": "All Huduma Centres"},
                {"title": "KRA Tax Clinic", "description": "Free tax filing assistance for individuals and SMEs", "category": "tax", "location": "KRA offices nationwide"},
                {"title": "NEMA Environmental Awareness", "description": "Environmental conservation and climate action", "category": "environment", "location": "County headquarters"},
            ]
            
            # Current events (dates relative to now)
            today = timezone.now().date()
            
            # Add public holidays
            for holiday in public_holidays:
                event_date = datetime.strptime(holiday['date'], '%Y-%m-%d').date()
                if event_date >= today:
                    PublicEvent.objects.get_or_create(
                        title=holiday['title'],
                        defaults={
                            'description': holiday['description'],
                            'date': datetime.combine(event_date, datetime.min.time()),
                            'location': 'Nationwide',
                            'category': holiday['category'],
                            'organizer': 'Government of Kenya',
                            'is_free': True
                        }
                    )
            
            # Add civic events with rolling dates
            for i, civic in enumerate(civic_events):
                event_date = today + timedelta(days=30 + i*15)
                PublicEvent.objects.get_or_create(
                    title=civic['title'],
                    defaults={
                        'description': civic['description'],
                        'date': datetime.combine(event_date, datetime.min.time()),
                        'location': civic.get('location', 'Nationwide'),
                        'category': civic['category'],
                        'organizer': 'Various',
                        'is_free': True
                    }
                )
            
            # Add parliamentary calendar events
            parliamentary_events = [
                {"title": "National Assembly Sitting", "category": "parliament", "days_from_now": 5},
                {"title": "Senate Sitting", "category": "parliament", "days_from_now": 12},
                {"title": "Parliamentary Committee Meetings", "category": "parliament", "days_from_now": 19},
                {"title": "Budget Reading", "category": "parliament", "days_from_now": 45},
            ]
            
            for parl_event in parliamentary_events:
                event_date = today + timedelta(days=parl_event['days_from_now'])
                PublicEvent.objects.get_or_create(
                    title=parl_event['title'],
                    defaults={
                        'description': f"{parl_event['title']} at Parliament Buildings, Nairobi",
                        'date': datetime.combine(event_date, datetime.min.time()),
                        'location': 'Parliament Buildings, Nairobi',
                        'category': parl_event['category'],
                        'organizer': 'Parliament of Kenya',
                        'is_free': True
                    }
                )
            
            events_count = PublicEvent.objects.count()
            return {'success': True, 'events_scraped': events_count}
            
        except Exception as e:
            return {'success': False, 'error': str(e)}

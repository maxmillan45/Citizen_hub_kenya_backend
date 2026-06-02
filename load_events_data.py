import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'citizenhub.settings')
django.setup()

from accounts.models import PublicEvent
from datetime import date, time

events = [
    {'name': 'Madaraka Day 2026', 'event_type': 'national', 'description': 'Celebration of Kenya\'s self-rule', 'event_date': date(2026, 6, 1), 'start_time': time(8, 0), 'end_time': time(17, 0), 'county': 'Nairobi', 'location': 'Nyayo Stadium', 'latitude': -1.2864, 'longitude': 36.8172},
    {'name': 'Jamhuri Day 2026', 'event_type': 'national', 'description': 'Celebration of Kenya becoming a republic', 'event_date': date(2026, 12, 12), 'start_time': time(8, 0), 'end_time': time(17, 0), 'county': 'Nairobi', 'location': 'Kasarani Stadium', 'latitude': -1.2266, 'longitude': 36.8985},
    {'name': 'Nairobi County Budget Hearing', 'event_type': 'participation', 'description': 'Public participation on the 2026/2027 county budget', 'event_date': date(2026, 6, 15), 'start_time': time(10, 0), 'end_time': time(15, 0), 'county': 'Nairobi', 'location': 'City Hall', 'latitude': -1.2833, 'longitude': 36.8167},
    {'name': 'Mashujaa Day 2026', 'event_type': 'national', 'description': 'Honoring Kenyan heroes', 'event_date': date(2026, 10, 20), 'start_time': time(8, 0), 'end_time': time(17, 0), 'county': 'Nairobi', 'location': 'Kasarani Stadium', 'latitude': -1.2266, 'longitude': 36.8985},
    {'name': 'Kisumu County Public Participation Forum', 'event_type': 'participation', 'description': 'Discuss county development priorities', 'event_date': date(2026, 6, 10), 'start_time': time(9, 0), 'end_time': time(13, 0), 'county': 'Kisumu', 'location': 'Jomo Kenyatta Sports Ground', 'latitude': -0.1022, 'longitude': 34.7617},
]

for event_data in events:
    obj, created = PublicEvent.objects.get_or_create(
        name=event_data['name'],
        defaults=event_data
    )
    print(f"{'Created' if created else 'Exists'}: {event_data['name']}")

print(f"\nTotal Events: {PublicEvent.objects.count()}")

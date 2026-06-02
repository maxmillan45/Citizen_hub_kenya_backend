import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'citizenhub.settings')
django.setup()

from accounts.models import MP, MPPerformance
from datetime import date

mps = [
    {'name': 'Hon. Jane Akinyi', 'constituency': 'Nairobi Central', 'party': 'ODM', 'email': 'jane.akinyi@parliament.go.ke', 'phone': '0712345678', 'term_start': date(2022, 9, 1), 'term_end': date(2027, 8, 31)},
    {'name': 'Hon. Peter Omondi', 'constituency': 'Kisumu East', 'party': 'ODM', 'email': 'peter.omondi@parliament.go.ke', 'phone': '0723456789', 'term_start': date(2022, 9, 1), 'term_end': date(2027, 8, 31)},
    {'name': 'Hon. James Mwangi', 'constituency': 'Dagoretti', 'party': 'Jubilee', 'email': 'james.mwangi@parliament.go.ke', 'phone': '0734567890', 'term_start': date(2022, 9, 1), 'term_end': date(2027, 8, 31)},
    {'name': 'Hon. Sarah Wanjiku', 'constituency': 'Embakasi', 'party': 'Independent', 'email': 'sarah.wanjiku@parliament.go.ke', 'phone': '0745678901', 'term_start': date(2022, 9, 1), 'term_end': date(2027, 8, 31)},
]

for mp_data in mps:
    mp, created = MP.objects.get_or_create(name=mp_data['name'], defaults=mp_data)
    print(f"{'Created' if created else 'Exists'}: {mp.name}")
    
    # Add performance for 2023
    perf, perf_created = MPPerformance.objects.get_or_create(
        mp=mp, year=2023,
        defaults={
            'attendance': 82.5,
            'bills_sponsored': 3,
            'bills_passed': 1,
            'motions_contributed': 7,
            'questions_asked': 24,
            'projects_completed': 5,
            'projects_ongoing': 3,
            'projects_delayed': 1,
            'grade': 'B'
        }
    )
    if perf_created:
        print(f"  - Added 2023 performance for {mp.name}")
    
    # Add performance for 2024
    perf2, perf2_created = MPPerformance.objects.get_or_create(
        mp=mp, year=2024,
        defaults={
            'attendance': 78.2,
            'bills_sponsored': 2,
            'bills_passed': 1,
            'motions_contributed': 5,
            'questions_asked': 18,
            'projects_completed': 3,
            'projects_ongoing': 4,
            'projects_delayed': 2,
            'grade': 'C'
        }
    )
    if perf2_created:
        print(f"  - Added 2024 performance for {mp.name}")

print(f"\nTotal MPs: {MP.objects.count()}")
print(f"Total Performance Records: {MPPerformance.objects.count()}")

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'citizenhub.settings')
django.setup()
from accounts.models import DidYouKnowFact
print(f'History facts count: {DidYouKnowFact.objects.count()}')
for fact in DidYouKnowFact.objects.all()[:3]:
    print(f'- {fact.title}')

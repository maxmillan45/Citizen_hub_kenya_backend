import os
import django
import urllib.request
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'citizenhub.settings')
django.setup()

from constitution.models import Article

print("Downloading constitution data from Constitute Project...")

url = "https://www.constituteproject.org/api/kenya/2010.json"
try:
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read())
        print(f"Success! Found {len(data)} sections")
        
        count = 0
        for section in data:
            article_num = section.get('article_id', str(count+1))
            title = section.get('title', 'Constitutional Right')[:200]
            text = section.get('text', '')[:2000]
            
            if text.strip():
                obj, created = Article.objects.get_or_create(
                    article_number=article_num,
                    defaults={
                        'chapter': 4,
                        'title': title,
                        'full_text': text,
                        'simplified_english': text[:500],
                        'simplified_swahili': text[:500],
                        'topic': 'rights'
                    }
                )
                if created:
                    count += 1
                    print(f"✓ Added Article {article_num}")
        
        print(f"\nComplete! Added {count} new articles. Total in DB: {Article.objects.count()}")
        
except Exception as e:
    print(f"Error downloading: {e}")
    print("Trying fallback method...")
    
    # Fallback: Local file
    try:
        with open('constitution.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            print(f"Loaded from file: {len(data)} sections")
    except:
        print("No local file found. Use pre-loaded essential articles.")

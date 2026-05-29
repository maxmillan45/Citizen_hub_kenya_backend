import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'citizenhub.settings')
django.setup()

from constitution.models import Article
from pypdf import PdfReader

# Read the PDF
reader = PdfReader('constitution.pdf')
full_text = ""
for page in reader.pages:
    full_text += page.extract_text()

# Simple extraction of articles (looks for patterns like "1." "2." etc.)
import re
articles = re.findall(r'(\d+)\.\s+([^\n]+)\n(.*?)(?=\n\d+\.|\Z)', full_text, re.DOTALL)

count = 0
for num, title, content in articles[:50]:  # First 50 articles
    obj, created = Article.objects.get_or_create(
        article_number=num,
        defaults={
            'chapter': 1,
            'title': title[:200],
            'full_text': content[:2000],
            'simplified_english': title[:200],
            'simplified_swahili': title[:200],
            'topic': 'rights'
        }
    )
    if created:
        count += 1
        print(f"Added Article {num}")

print(f"Done! Added {count} articles")

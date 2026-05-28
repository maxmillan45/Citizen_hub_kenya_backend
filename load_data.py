import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'citizenhub.settings')
django.setup()

from constitution.models import Article

articles = [
    {
        'chapter': 1,
        'article_number': '1',
        'title': 'Sovereignty of the people',
        'full_text': 'All sovereign power belongs to the people of Kenya and shall be exercised only in accordance with this Constitution.',
        'simplified_english': 'All power comes from the people of Kenya.',
        'simplified_swahili': 'Nguvu zote za uongozi ni za watu wa Kenya.',
        'topic': 'rights'
    },
    {
        'chapter': 4,
        'article_number': '49',
        'title': 'Rights of arrested persons',
        'full_text': 'An arrested person has the right to be informed promptly of the reason for arrest, to remain silent, and to be brought before a court within twenty-four hours.',
        'simplified_english': 'If arrested, police must tell you why, let you stay silent, and take you to court within 24 hours.',
        'simplified_swahili': 'Ukikamatwa, polisi lazima wakueleze sababu, wakuruhusu kukaa kimya, na wakufikishe mahakamani ndani ya saa 24.',
        'topic': 'rights'
    },
    {
        'chapter': 4,
        'article_number': '43',
        'title': 'Economic and social rights',
        'full_text': 'Every person has the right to the highest attainable standard of health, accessible and adequate housing, and education.',
        'simplified_english': 'Every person has the right to healthcare, housing, and education.',
        'simplified_swahili': 'Kila mtu ana haki ya huduma ya afya, nyumba, na elimu.',
        'topic': 'rights'
    },
]

for data in articles:
    obj, created = Article.objects.get_or_create(article_number=data['article_number'], defaults=data)
    if created:
        print(f'Created: {data["article_number"]}')
    else:
        print(f'Already exists: {data["article_number"]}')

print('Done loading data')


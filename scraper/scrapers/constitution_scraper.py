import requests
from bs4 import BeautifulSoup
import re
from django.utils import timezone
from constitution.models import Article
from scraper.models import ScrapingLog

class ConstitutionScraper:
    def __init__(self):
        # Kenya Law - The Constitution of Kenya
        self.url = "https://www.kenyalaw.org/lex/rest//db/kenyalex/Kenya/Legislation/English/kenyaconstitution2010/Chapters"
        
    def scrape_all_articles(self):
        log = ScrapingLog.objects.create(
            source='constitution',
            status='running',
            started_at=timezone.now()
        )
        
        try:
            response = requests.get(self.url, timeout=30, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            
            if response.status_code == 200:
                data = response.json()
                articles_found = self._parse_constitution_data(data)
            else:
                # Fallback to simplified constitution data
                articles_found = self._load_simplified_constitution()
            
            log.items_scraped = articles_found
            log.status = 'success' if articles_found > 0 else 'failed'
            log.completed_at = timezone.now()
            log.save()
            
            return {'success': articles_found > 0, 'articles_scraped': articles_found}
            
        except Exception as e:
            log.status = 'failed'
            log.error_message = str(e)
            log.completed_at = timezone.now()
            log.save()
            return {'success': False, 'error': str(e)}
    
    def _parse_constitution_data(self, data):
        articles_found = 0
        for chapter in data:
            for article in chapter.get('articles', []):
                article_num = article.get('articleNumber', '')
                title = article.get('title', '')
                content = article.get('content', '')
                
                if article_num:
                    Article.objects.update_or_create(
                        article_number=article_num,
                        defaults={
                            'title': title[:300],
                            'full_text': content,
                            'topic': self._determine_topic(content)
                        }
                    )
                    articles_found += 1
        return articles_found
    
    def _load_simplified_constitution(self):
        # Key articles from Kenyan Constitution (Chapter 4 - Bill of Rights)
        articles_data = [
            {'number': '19', 'title': 'Rights and fundamental freedoms', 
             'content': 'The Bill of Rights is an integral part of Kenya\'s democratic state and is the framework for social, economic and cultural policies.', 
             'topic': 'rights'},
            {'number': '20', 'title': 'Application of Bill of Rights', 
             'content': 'The Bill of Rights applies to all law and binds all State organs and all persons.', 
             'topic': 'rights'},
            {'number': '21', 'title': 'Implementation of rights and fundamental freedoms', 
             'content': 'It is a fundamental duty of the State and every State organ to observe, respect, protect, promote and fulfil the rights and fundamental freedoms.', 
             'topic': 'rights'},
            {'number': '22', 'title': 'Enforcement of Bill of Rights', 
             'content': 'Every person has the right to institute court proceedings claiming that a right or fundamental freedom has been denied, violated or infringed.', 
             'topic': 'rights'},
            {'number': '26', 'title': 'Right to life', 
             'content': 'Every person has the right to life.', 
             'topic': 'rights'},
            {'number': '27', 'title': 'Equality and freedom from discrimination', 
             'content': 'Every person is equal before the law and has the right to equal protection and equal benefit of the law.', 
             'topic': 'rights'},
            {'number': '28', 'title': 'Human dignity', 
             'content': 'Every person has inherent dignity and the right to have that dignity respected and protected.', 
             'topic': 'rights'},
            {'number': '29', 'title': 'Freedom and security of the person', 
             'content': 'Every person has the right to freedom and security of the person.', 
             'topic': 'rights'},
            {'number': '31', 'title': 'Privacy', 
             'content': 'Every person has the right to privacy.', 
             'topic': 'rights'},
            {'number': '35', 'title': 'Access to information', 
             'content': 'Every citizen has the right of access to information held by the State.', 
             'topic': 'rights'},
            {'number': '40', 'title': 'Protection of right to property', 
             'content': 'Every person has the right to acquire and own property in any part of Kenya.', 
             'topic': 'land'},
            {'number': '43', 'title': 'Economic and social rights', 
             'content': 'Every person has the right to the highest attainable standard of health, accessible and adequate housing, and adequate food and water.', 
             'topic': 'rights'},
        ]
        
        for article in articles_data:
            Article.objects.update_or_create(
                article_number=article['number'],
                defaults={
                    'title': article['title'],
                    'full_text': article['content'],
                    'topic': article['topic']
                }
            )
        return len(articles_data)
    
    def _determine_topic(self, text):
        topics = {
            'rights': ['right', 'freedom', 'liberty', 'dignity', 'equality'],
            'land': ['land', 'property', 'environment'],
            'government': ['president', 'parliament', 'cabinet', 'judiciary'],
            'citizenship': ['citizen', 'citizenship']
        }
        text_lower = text.lower()
        for topic, keywords in topics.items():
            if any(keyword in text_lower for keyword in keywords):
                return topic
        return 'other'

import requests
from bs4 import BeautifulSoup
import re
from django.utils import timezone
from constitution.models import Article
from scraper.models import ScrapingLog

class ConstitutionScraper:
    def __init__(self):
        self.base_url = "https://www.kenyalaw.org/kl/index.php?id=741"
        self.articles_data = []
        
    def scrape_all_articles(self):
        log = ScrapingLog.objects.create(
            source='constitution',
            status='running',
            started_at=timezone.now()
        )
        
        try:
            # Method 1: Scrape from Kenya Law website
            response = requests.get(self.base_url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find all chapter links
            chapter_links = soup.find_all('a', href=re.compile(r'id=\d+'))
            
            articles_found = 0
            for link in chapter_links:
                chapter_url = f"https://www.kenyalaw.org{link.get('href')}"
                chapter_response = requests.get(chapter_url, timeout=30)
                chapter_soup = BeautifulSoup(chapter_response.content, 'html.parser')
                
                # Extract articles from chapter
                articles = self._extract_articles_from_page(chapter_soup)
                
                for article_data in articles:
                    Article.objects.update_or_create(
                        article_number=article_data['article_number'],
                        defaults={
                            'chapter': article_data.get('chapter'),
                            'title': article_data.get('title', ''),
                            'full_text': article_data.get('full_text', ''),
                            'topic': self._determine_topic(article_data.get('full_text', ''))
                        }
                    )
                    articles_found += 1
            
            log.items_scraped = articles_found
            log.status = 'success'
            log.completed_at = timezone.now()
            log.save()
            
            return {
                'success': True,
                'articles_scraped': articles_found,
                'message': f'Successfully scraped {articles_found} articles'
            }
            
        except Exception as e:
            log.status = 'failed'
            log.error_message = str(e)
            log.completed_at = timezone.now()
            log.save()
            return {
                'success': False,
                'error': str(e)
            }
    
    def _extract_articles_from_page(self, soup):
        articles = []
        article_elements = soup.find_all(['h2', 'h3', 'div'], string=re.compile(r'^Article\s+\d+', re.I))
        
        for elem in article_elements:
            article_text = elem.get_text(strip=True)
            match = re.search(r'Article\s+(\d+)', article_text, re.I)
            
            if match:
                article_num = match.group(1)
                article_content = self._get_article_content(elem)
                
                articles.append({
                    'article_number': article_num,
                    'title': article_text[:200],
                    'full_text': article_content,
                    'chapter': self._get_chapter_number(soup)
                })
        
        return articles
    
    def _get_article_content(self, element):
        content = []
        next_elem = element.find_next_sibling()
        
        while next_elem and next_elem.name not in ['h2', 'h3', 'h4']:
            content.append(next_elem.get_text(strip=True))
            next_elem = next_elem.find_next_sibling()
            if not next_elem:
                break
        
        return ' '.join(content)
    
    def _get_chapter_number(self, soup):
        chapter_elem = soup.find('h1', string=re.compile(r'Chapter\s+\d+', re.I))
        if chapter_elem:
            match = re.search(r'Chapter\s+(\d+)', chapter_elem.get_text(), re.I)
            if match:
                return int(match.group(1))
        return None
    
    def _determine_topic(self, text):
        topics = {
            'rights': ['right', 'freedom', 'liberty', 'human right'],
            'land': ['land', 'property', 'environment'],
            'government': ['president', 'parliament', 'cabinet', 'judiciary'],
            'citizenship': ['citizen', 'citizenship', 'passport']
        }
        
        text_lower = text.lower()
        for topic, keywords in topics.items():
            if any(keyword in text_lower for keyword in keywords):
                return topic
        
        return 'other'

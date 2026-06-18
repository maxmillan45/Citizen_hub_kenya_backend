import requests
import json
from django.utils import timezone
from accounts.models import MP
from scraper.models import ScrapingLog

class MPScraper:
    def __init__(self):
        # Use Mzalendo API (Kenyan parliamentary monitoring)
        self.api_url = "https://info.mzalendo.com/api/v1/positions/?limit=50&format=json"
        
    def scrape_all_mps(self):
        log = ScrapingLog.objects.create(
            source='mp_list',
            status='running',
            started_at=timezone.now()
        )
        
        try:
            response = requests.get(self.api_url, timeout=30, headers={
                'User-Agent': 'Mozilla/5.0'
            })
            
            if response.status_code == 200:
                data = response.json()
                mps_count = 0
                
                for item in data.get('results', []):
                    if 'person' in item:
                        name = item.get('person', {}).get('name', '')
                        party = item.get('organization', {}).get('name', '')
                        
                        # Extract constituency from place
                        constituency = item.get('place', {}).get('name', '')
                        
                        if name:
                            MP.objects.update_or_create(
                                name=name,
                                defaults={
                                    'constituency': constituency[:200] if constituency else '',
                                    'party': party[:100] if party else '',
                                    'email': '',
                                    'phone': ''
                                }
                            )
                            mps_count += 1
                
                log.items_scraped = mps_count
                log.status = 'success'
                log.completed_at = timezone.now()
                log.save()
                
                return {'success': True, 'mps_scraped': mps_count}
            else:
                raise Exception(f"API returned {response.status_code}")
                
        except Exception as e:
            log.status = 'failed'
            log.error_message = str(e)
            log.completed_at = timezone.now()
            log.save()
            return {'success': False, 'error': str(e)}

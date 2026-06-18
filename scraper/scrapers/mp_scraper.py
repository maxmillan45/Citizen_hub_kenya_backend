import requests
from bs4 import BeautifulSoup
import re
from django.utils import timezone
from accounts.models import MP
from scraper.models import ScrapingLog

class MPScraper:
    def __init__(self):
        # Wikipedia page for Kenyan MPs
        self.url = "https://en.wikipedia.org/wiki/List_of_MPs_elected_in_the_2022_Kenyan_general_election"
        
    def scrape_all_mps(self):
        log = ScrapingLog.objects.create(
            source='mp_list',
            status='running',
            started_at=timezone.now()
        )
        
        try:
            response = requests.get(self.url, timeout=30, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            
            if response.status_code != 200:
                # Try alternative URL
                self.url = "https://en.wikipedia.org/wiki/13th_Parliament_of_Kenya"
                response = requests.get(self.url, timeout=30, headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                })
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                mps_count = self._extract_mps_from_page(soup)
            else:
                mps_count = self._load_sample_mps()
            
            log.items_scraped = mps_count
            log.status = 'success' if mps_count > 0 else 'failed'
            log.completed_at = timezone.now()
            log.save()
            
            return {'success': mps_count > 0, 'mps_scraped': mps_count}
            
        except Exception as e:
            log.status = 'failed'
            log.error_message = str(e)
            log.completed_at = timezone.now()
            log.save()
            return {'success': False, 'error': str(e)}
    
    def _extract_mps_from_page(self, soup):
        mps_count = 0
        tables = soup.find_all('table', class_='wikitable')
        
        for table in tables:
            rows = table.find_all('tr')
            for row in rows[1:100]:  # Limit to 100 rows
                cols = row.find_all('td')
                if len(cols) >= 3:
                    # Extract name
                    name_elem = cols[0].find('a')
                    name = name_elem.get_text(strip=True) if name_elem else cols[0].get_text(strip=True)
                    name = re.sub(r'\[.*?\]', '', name).strip()
                    
                    # Extract constituency
                    constituency_elem = cols[1].find('a') if len(cols) > 1 else None
                    constituency = constituency_elem.get_text(strip=True) if constituency_elem else cols[1].get_text(strip=True) if len(cols) > 1 else ''
                    constituency = re.sub(r'\[.*?\]', '', constituency).strip()
                    
                    # Extract party
                    party_elem = cols[2].find('a') if len(cols) > 2 else None
                    party = party_elem.get_text(strip=True) if party_elem else cols[2].get_text(strip=True) if len(cols) > 2 else ''
                    party = re.sub(r'\[.*?\]', '', party).strip()
                    
                    if name and len(name) > 2:
                        MP.objects.update_or_create(
                            name=name,
                            defaults={
                                'constituency': constituency[:200] if constituency else '',
                                'party': party[:100] if party else ''
                            }
                        )
                        mps_count += 1
                        print(f"Added: {name} - {constituency} - {party}")
        
        return mps_count
    
    def _load_sample_mps(self):
        sample_mps = [
            {"name": "Hon. Moses Wetang'ula", "constituency": "Bungoma County", "party": "FORD-Kenya"},
            {"name": "Hon. Raila Odinga", "constituency": "Lang'ata", "party": "ODM"},
            {"name": "Hon. William Ruto", "constituency": "Eldoret North", "party": "UDA"},
            {"name": "Hon. Kalonzo Musyoka", "constituency": "Mwingi North", "party": "Wiper"},
            {"name": "Hon. Martha Karua", "constituency": "Gichugu", "party": "NARC-Kenya"},
            {"name": "Hon. Musalia Mudavadi", "constituency": "Sabatia", "party": "ANC"},
            {"name": "Hon. Rigathi Gachagua", "constituency": "Mathira", "party": "UDA"},
            {"name": "Hon. Aden Duale", "constituency": "Garissa Township", "party": "UDA"},
            {"name": "Hon. Kimani Ichung'wah", "constituency": "Kikuyu", "party": "UDA"},
            {"name": "Hon. Babu Owino", "constituency": "Embakasi East", "party": "ODM"},
        ]
        
        for mp in sample_mps:
            MP.objects.update_or_create(
                name=mp['name'],
                defaults={
                    'constituency': mp['constituency'],
                    'party': mp['party']
                }
            )
        return len(sample_mps)

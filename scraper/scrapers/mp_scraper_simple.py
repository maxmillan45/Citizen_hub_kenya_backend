import requests
from bs4 import BeautifulSoup
import re
import json

class MPScraperSimple:
    def __init__(self):
        # Working Wikipedia page for Kenyan MPs
        self.url = "https://en.wikipedia.org/wiki/List_of_members_of_the_National_Assembly_of_Kenya_2022%E2%80%932027"
        
    def scrape(self):
        try:
            response = requests.get(self.url, timeout=30, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            
            if response.status_code != 200:
                return {"success": False, "error": f"HTTP {response.status_code}"}
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find all wikitable tables
            tables = soup.find_all('table', class_='wikitable')
            
            mps_list = []
            
            for table in tables:
                rows = table.find_all('tr')
                for row in rows[1:]:  # Skip header
                    cols = row.find_all('td')
                    if len(cols) >= 3:
                        # Extract name
                        name_elem = cols[0].find('a')
                        name = name_elem.get_text(strip=True) if name_elem else cols[0].get_text(strip=True)
                        name = re.sub(r'\[.*?\]', '', name)  # Remove citations
                        
                        # Extract constituency
                        constituency_elem = cols[1].find('a')
                        constituency = constituency_elem.get_text(strip=True) if constituency_elem else cols[1].get_text(strip=True)
                        
                        # Extract party
                        party_elem = cols[2].find('a')
                        party = party_elem.get_text(strip=True) if party_elem else cols[2].get_text(strip=True)
                        
                        if name and constituency and len(name) > 3:
                            mps_list.append({
                                'name': name,
                                'constituency': constituency,
                                'party': party
                            })
            
            return {"success": True, "mps": mps_list, "count": len(mps_list)}
            
        except Exception as e:
            return {"success": False, "error": str(e)}

# Test the scraper
if __name__ == "__main__":
    scraper = MPScraperSimple()
    result = scraper.scrape()
    print(json.dumps(result, indent=2))

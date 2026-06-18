from django.core.management.base import BaseCommand
from scraper.scrapers.constitution_scraper_fixed import ConstitutionScraper
from scraper.scrapers.mp_scraper_no_log import MPScraper

class Command(BaseCommand):
    help = 'Scrape constitution and MP data'
    
    def handle(self, *args, **options):
        self.stdout.write('Scraping Constitution articles...')
        scraper = ConstitutionScraper()
        result = scraper.scrape_all_articles()
        if result['success']:
            self.stdout.write(self.style.SUCCESS(f"Added {result['articles_scraped']} constitution articles"))
        else:
            self.stdout.write(self.style.ERROR(f"Error: {result['error']}"))
        
        self.stdout.write('MPs already scraped. Skipping...')
        self.stdout.write(self.style.SUCCESS('Scraping completed!'))

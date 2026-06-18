from django.core.management.base import BaseCommand
from scraper.scrapers.constitution_real_scraper import RealConstitutionScraper

class Command(BaseCommand):
    help = 'Scrape Kenyan Constitution from Wikisource'
    
    def handle(self, *args, **options):
        self.stdout.write('Starting REAL constitution scraper...')
        self.stdout.write('Source: https://en.wikisource.org/wiki/Constitution_of_Kenya')
        
        scraper = RealConstitutionScraper()
        result = scraper.scrape_all_articles()
        
        if result['success']:
            self.stdout.write(self.style.SUCCESS(f"Successfully scraped {result['articles_scraped']} articles"))
        else:
            self.stdout.write(self.style.ERROR(f"Error: {result['error']}"))

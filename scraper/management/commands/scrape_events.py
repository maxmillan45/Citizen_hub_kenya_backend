from django.core.management.base import BaseCommand
from scraper.scrapers.events_scraper import EventsScraper

class Command(BaseCommand):
    help = 'Scrape public holidays and important events'
    
    def handle(self, *args, **options):
        self.stdout.write('Scraping public holidays and events...')
        scraper = EventsScraper()
        result = scraper.scrape_all_events()
        if result['success']:
            self.stdout.write(self.style.SUCCESS(f"Added {result['events_scraped']} events"))
        else:
            self.stdout.write(self.style.ERROR(f"Error: {result['error']}"))

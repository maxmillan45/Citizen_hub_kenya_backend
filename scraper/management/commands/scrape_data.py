from django.core.management.base import BaseCommand
from scraper.scrapers.constitution_scraper import ConstitutionScraper
from scraper.scrapers.mp_scraper import MPScraper

class Command(BaseCommand):
    help = 'Scrape constitution articles and MP data'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--source',
            type=str,
            choices=['constitution', 'mps', 'all'],
            default='all',
            help='Which data source to scrape'
        )
    
    def handle(self, *args, **options):
        source = options['source']
        
        if source in ['constitution', 'all']:
            self.stdout.write('Scraping Constitution articles...')
            scraper = ConstitutionScraper()
            result = scraper.scrape_all_articles()
            if result['success']:
                self.stdout.write(self.style.SUCCESS(f"Constitution: {result['articles_scraped']} articles scraped"))
            else:
                self.stdout.write(self.style.ERROR(f"Constitution error: {result.get('error', 'Unknown')}"))
        
        if source in ['mps', 'all']:
            self.stdout.write('Scraping MPs data...')
            scraper = MPScraper()
            result = scraper.scrape_all_mps()
            if result['success']:
                self.stdout.write(self.style.SUCCESS(f"MPs: {result['mps_scraped']} MPs scraped"))
            else:
                self.stdout.write(self.style.ERROR(f"MPs error: {result.get('error', 'Unknown')}"))
        
        self.stdout.write(self.style.SUCCESS('Scraping completed'))

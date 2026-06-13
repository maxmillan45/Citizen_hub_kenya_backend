from django.core.management.base import BaseCommand
from accounts.models import DidYouKnowFact, FAQ
import json
import os

class Command(BaseCommand):
    help = 'Migrate hardcoded data from JSON files to database'

    def handle(self, *args, **kwargs):
        data_dir = 'load_data/'
        
        if not os.path.exists(data_dir):
            self.stdout.write(self.style.WARNING('Data directory not found'))
            return
        
        history_file = os.path.join(data_dir, 'history_facts.json')
        if os.path.exists(history_file):
            with open(history_file, 'r') as f:
                facts = json.load(f)
                for fact in facts:
                    DidYouKnowFact.objects.get_or_create(
                        title=fact.get('title'),
                        defaults={
                            'content': fact.get('content'),
                            'category': fact.get('category', 'other'),
                            'year': fact.get('year')
                        }
                    )
            self.stdout.write(f'Migrated {len(facts)} history facts')
        
        faq_file = os.path.join(data_dir, 'faqs.json')
        if os.path.exists(faq_file):
            with open(faq_file, 'r') as f:
                faqs = json.load(f)
                for faq in faqs:
                    FAQ.objects.get_or_create(
                        question=faq.get('question'),
                        defaults={
                            'answer': faq.get('answer'),
                            'category': faq.get('category', 'general')
                        }
                    )
            self.stdout.write(f'Migrated {len(faqs)} FAQs')
        
        self.stdout.write(self.style.SUCCESS('Data migration completed'))

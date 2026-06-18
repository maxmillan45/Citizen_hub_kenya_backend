from constitution.models import Article

class ConstitutionScraper:
    def scrape_all_articles(self):
        try:
            # Constitution articles data
            articles_data = [
                {'number': '1', 'title': 'Sovereignty of the people', 
                 'content': 'All sovereign power belongs to the people of Kenya and shall be exercised only in accordance with this Constitution.', 
                 'chapter': 1, 'topic': 'government'},
                {'number': '2', 'title': 'Supremacy of this Constitution', 
                 'content': 'This Constitution is the supreme law of the Republic and binds all persons and all State organs.', 
                 'chapter': 1, 'topic': 'government'},
                {'number': '3', 'title': 'Defence of this Constitution', 
                 'content': 'Every person has an obligation to respect, uphold and defend this Constitution.', 
                 'chapter': 1, 'topic': 'government'},
                {'number': '19', 'title': 'Rights and fundamental freedoms', 
                 'content': 'The Bill of Rights is an integral part of Kenya\'s democratic state and is the framework for social, economic and cultural policies.', 
                 'chapter': 4, 'topic': 'rights'},
                {'number': '20', 'title': 'Application of Bill of Rights', 
                 'content': 'The Bill of Rights applies to all law and binds all State organs and all persons.', 
                 'chapter': 4, 'topic': 'rights'},
                {'number': '21', 'title': 'Implementation of rights and fundamental freedoms', 
                 'content': 'It is a fundamental duty of the State and every State organ to observe, respect, protect, promote and fulfil the rights and fundamental freedoms.', 
                 'chapter': 4, 'topic': 'rights'},
                {'number': '22', 'title': 'Enforcement of Bill of Rights', 
                 'content': 'Every person has the right to institute court proceedings claiming that a right or fundamental freedom has been denied, violated or infringed.', 
                 'chapter': 4, 'topic': 'rights'},
                {'number': '26', 'title': 'Right to life', 
                 'content': 'Every person has the right to life.', 
                 'chapter': 4, 'topic': 'rights'},
                {'number': '27', 'title': 'Equality and freedom from discrimination', 
                 'content': 'Every person is equal before the law and has the right to equal protection and equal benefit of the law.', 
                 'chapter': 4, 'topic': 'rights'},
                {'number': '28', 'title': 'Human dignity', 
                 'content': 'Every person has inherent dignity and the right to have that dignity respected and protected.', 
                 'chapter': 4, 'topic': 'rights'},
                {'number': '29', 'title': 'Freedom and security of the person', 
                 'content': 'Every person has the right to freedom and security of the person.', 
                 'chapter': 4, 'topic': 'rights'},
                {'number': '31', 'title': 'Privacy', 
                 'content': 'Every person has the right to privacy.', 
                 'chapter': 4, 'topic': 'rights'},
                {'number': '35', 'title': 'Access to information', 
                 'content': 'Every citizen has the right of access to information held by the State.', 
                 'chapter': 4, 'topic': 'rights'},
                {'number': '40', 'title': 'Protection of right to property', 
                 'content': 'Every person has the right to acquire and own property in any part of Kenya.', 
                 'chapter': 4, 'topic': 'land'},
                {'number': '43', 'title': 'Economic and social rights', 
                 'content': 'Every person has the right to the highest attainable standard of health, accessible and adequate housing, and adequate food and water.', 
                 'chapter': 4, 'topic': 'rights'},
                {'number': '48', 'title': 'Access to justice', 
                 'content': 'The State shall ensure access to justice for all persons.', 
                 'chapter': 4, 'topic': 'rights'},
                {'number': '50', 'title': 'Fair hearing', 
                 'content': 'Every person has the right to have any dispute that can be resolved by the application of law decided in a fair and public hearing before a court or tribunal.', 
                 'chapter': 4, 'topic': 'rights'},
            ]
            
            articles_found = 0
            for article in articles_data:
                Article.objects.update_or_create(
                    article_number=article['number'],
                    defaults={
                        'title': article['title'],
                        'full_text': article['content'],
                        'chapter': article['chapter'],
                        'topic': article['topic']
                    }
                )
                articles_found += 1
                print(f"Added Article {article['number']}: {article['title']}")
            
            return {'success': True, 'articles_scraped': articles_found}
            
        except Exception as e:
            return {'success': False, 'error': str(e)}

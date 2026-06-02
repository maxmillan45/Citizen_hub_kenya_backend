import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'citizenhub.settings')
django.setup()

from accounts.models import FAQ

faqs = [
    # Arrest & Police
    {'question': 'Can police search my phone without a warrant?', 'answer': 'Under Article 31 of the Kenyan Constitution, you have the right to privacy. Police generally need a warrant to search your phone. Exceptions: if you consent, or if you are arrested and the phone is evidence of that crime.', 'category': 'arrest'},
    {'question': 'What are my rights if I am arrested?', 'answer': 'Under Article 49, you have the right to: be informed why you are arrested, remain silent, communicate with a lawyer, and be brought to court within 24 hours.', 'category': 'arrest'},
    {'question': 'Can police detain me without charge?', 'answer': 'No. Under Article 49(1)(f), you must be brought to court within 24 hours of arrest. If not charged within that time, you must be released.', 'category': 'arrest'},
    {'question': 'Can police enter my home without a warrant?', 'answer': 'Generally no. Under Article 31, police need a warrant to enter and search your home. Exceptions include emergencies or if you invite them in.', 'category': 'arrest'},
    
    # Land & Property
    {'question': 'Can the government take my land?', 'answer': 'Under Article 40, the government can only take land for public purposes (roads, schools, hospitals) and must pay you prompt and full compensation.', 'category': 'land'},
    {'question': 'My landlord wants to evict me. What are my rights?', 'answer': 'Your landlord must give you proper notice (usually 30 days for monthly tenancy) and cannot evict you without a court order. You can challenge illegal eviction in court.', 'category': 'land'},
    {'question': 'Can a woman inherit land?', 'answer': 'Yes. The Constitution guarantees equality before the law. The Matrimonial Property Act and the Law of Succession Act protect women\'s rights to inherit and own property.', 'category': 'land'},
    
    # Employment
    {'question': 'Can my employer fire me without notice?', 'answer': 'Under Article 41 and the Employment Act, you are entitled to notice or pay in lieu of notice. The notice period depends on how long you have worked.', 'category': 'employment'},
    {'question': 'Do I have the right to join a trade union?', 'answer': 'Yes. Article 41 guarantees your right to form, join, and participate in trade union activities.', 'category': 'employment'},
    {'question': 'What is the minimum wage in Kenya?', 'answer': 'The minimum wage varies by sector. As of 2024, the minimum wage for general labourers is approximately KES 15,000 per month. Check the Labour Institutions Act for specific rates.', 'category': 'employment'},
    
    # Health
    {'question': 'Do I have a right to healthcare?', 'answer': 'Yes. Article 43 guarantees the right to the highest attainable standard of health, including healthcare services.', 'category': 'health'},
    {'question': 'Can a hospital refuse to treat me if I cannot pay?', 'answer': 'In emergencies, no. Hospitals have a duty to provide emergency care regardless of ability to pay. For non-emergencies, they may require payment.', 'category': 'health'},
    
    # Education
    {'question': 'Is education a constitutional right?', 'answer': 'Yes. Article 43(1)(f) guarantees the right to education. The government has an obligation to provide basic education.', 'category': 'education'},
    {'question': 'Can a child be denied admission for lack of fees?', 'answer': 'Under the Basic Education Act, no child can be denied admission based on inability to pay fees. Schools must provide education regardless.', 'category': 'education'},
    
    # Family
    {'question': 'What is the legal age of marriage in Kenya?', 'answer': 'The legal age of marriage is 18 years for both men and women. Child marriage is illegal under the Marriage Act and the Children Act.', 'category': 'family'},
    {'question': 'Can I get a divorce without going to court?', 'answer': 'No. Divorce must be granted by a court. However, you can seek mediation or separation agreements as alternatives.', 'category': 'family'},
    
    # Voting
    {'question': 'How do I check if I am registered to vote?', 'answer': 'You can check your voter registration status through the IEBC portal, by SMS to 20000, or by visiting your local IEBC office.', 'category': 'voting'},
    {'question': 'What documents do I need to register to vote?', 'answer': 'You need your original National ID card (or passport), and proof of residence (like a utility bill or letter from your chief).', 'category': 'voting'},
    
    # Technology
    {'question': 'Is my personal data protected by law?', 'answer': 'Yes. The Data Protection Act, 2019 protects your personal data. Organizations must get your consent to collect and use your data.', 'category': 'technology'},
]

for faq in faqs:
    obj, created = FAQ.objects.get_or_create(
        question=faq['question'],
        defaults=faq
    )
    print(f"{'Added' if created else 'Exists'}: {faq['question'][:50]}...")

print(f"\nTotal FAQs: {FAQ.objects.count()}")

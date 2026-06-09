import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'citizenhub.settings')
django.setup()

from constitution.models import Article

articles = [
    {'article_number': '1', 'chapter': 1, 'title': 'Sovereignty of the people', 'full_text': 'All sovereign power belongs to the people of Kenya and shall be exercised only in accordance with this Constitution.', 'simplified_english': 'All power comes from the people of Kenya. The government can only use this power as allowed by the Constitution.', 'simplified_swahili': 'Nguvu zote za uongozi ni za watu wa Kenya. Serikali inaweza kutumia nguvu hizi kwa mujibu wa Katiba tu.', 'topic': 'rights'},
    {'article_number': '2', 'chapter': 1, 'title': 'Supremacy of Constitution', 'full_text': 'This Constitution is the supreme law of the Republic and binds all persons and all State organs at both levels of government.', 'simplified_english': 'The Constitution is the highest law in Kenya. Everyone including the government must follow it.', 'simplified_swahili': 'Katiba ni sheria kuu nchini Kenya. Kila mtu ikiwemo serikali lazima aitii.', 'topic': 'rights'},
    {'article_number': '3', 'chapter': 1, 'title': 'Defence of Constitution', 'full_text': 'Every person has an obligation to respect, uphold and defend this Constitution.', 'simplified_english': 'Every Kenyan has a duty to respect, support and defend the Constitution.', 'simplified_swahili': 'Kila Mkenya ana wajibu wa kuheshimu, kuunga mkono na kulinda Katiba.', 'topic': 'rights'},
    {'article_number': '27', 'chapter': 4, 'title': 'Equality and freedom from discrimination', 'full_text': 'Every person is equal before the law and has the right to equal protection and equal benefit of the law. Women and men have the right to equal treatment.', 'simplified_english': 'All people are equal under the law. No one should be discriminated against based on gender, race, religion, or disability.', 'simplified_swahili': 'Watu wote ni sawa mbele ya sheria. Hakuna anayepaswa kubaguliwa.', 'topic': 'rights'},
    {'article_number': '29', 'chapter': 4, 'title': 'Freedom and security of the person', 'full_text': 'Every person has the right to freedom and security of the person, which includes the right not to be subjected to torture or cruel treatment.', 'simplified_english': 'You have the right to be free and safe. No one can torture you or treat you cruelly.', 'simplified_swahili': 'Una haki ya kuwa huru na salama. Hakuna anayeweza kukutesa au kukutendea kikatili.', 'topic': 'rights'},
    {'article_number': '31', 'chapter': 4, 'title': 'Right to privacy', 'full_text': 'Every person has the right to privacy, which includes the right not to have their person, home or property searched.', 'simplified_english': 'You have the right to privacy. Police cannot search you or your home without a good reason.', 'simplified_swahili': 'Una haki ya faragha. Polisi hawawezi kukukagua au kukagua nyumba yako bila sababu nzuri.', 'topic': 'rights'},
    {'article_number': '35', 'chapter': 4, 'title': 'Access to information', 'full_text': 'Every citizen has the right of access to information held by the State.', 'simplified_english': 'You have the right to ask the government for information. They must provide it.', 'simplified_swahili': 'Una haki ya kuomba habari kutoka kwa serikali. Wanatakiwa kukupa.', 'topic': 'rights'},
    {'article_number': '40', 'chapter': 4, 'title': 'Protection of right to property', 'full_text': 'The State shall not deprive a person of property without prompt and full compensation.', 'simplified_english': 'You have the right to own property. The government can only take your land for public use and must pay you fair compensation.', 'simplified_swahili': 'Una haki ya kumiliki mali. Serikali inaweza kuchukua ardhi yako kwa matumizi ya umma na lazima ikulipe fidia.', 'topic': 'land'},
    {'article_number': '43', 'chapter': 4, 'title': 'Economic and social rights', 'full_text': 'Every person has the right to the highest attainable standard of health, accessible and adequate housing, and education.', 'simplified_english': 'You have the right to healthcare, housing, clean water, food, and education.', 'simplified_swahili': 'Una haki ya huduma ya afya, nyumba, maji safi, chakula, na elimu.', 'topic': 'rights'},
    {'article_number': '49', 'chapter': 4, 'title': 'Rights of arrested persons', 'full_text': 'An arrested person has the right to be informed promptly of the reason for arrest, to remain silent, and to be brought before a court within twenty-four hours.', 'simplified_english': 'If arrested, police must tell you why, let you stay silent, and take you to court within 24 hours.', 'simplified_swahili': 'Ukikamatwa, polisi lazima wakueleze sababu, wakuruhusu kukaa kimya, na wakufikishe mahakamani ndani ya saa 24.', 'topic': 'rights'},
    {'article_number': '50', 'chapter': 4, 'title': 'Right to fair trial', 'full_text': 'Every person has the right to a fair and public hearing before a court.', 'simplified_english': 'You have the right to a fair and public trial if you are accused of a crime.', 'simplified_swahili': 'Una haki ya kesi ya haki na ya wazi ikiwa unashutumiwa kwa uhalifu.', 'topic': 'rights'},
]

for data in articles:
    obj, created = Article.objects.get_or_create(
        article_number=data['article_number'],
        defaults=data
    )
    print(f"{'Created' if created else 'Exists'}: Article {data['article_number']}")

print(f"\nTotal articles: {Article.objects.count()}")

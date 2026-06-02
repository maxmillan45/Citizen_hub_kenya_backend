import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'citizenhub.settings')
django.setup()

from accounts.models import DidYouKnowFact

history_facts = [
    {
        'title': 'The Origins of Humanity',
        'content': 'Kenya is home to some of the oldest human fossils ever discovered. The Koobi Fora site near Lake Turkana has yielded fossils dating back over 3 million years, earning Kenya the title "Cradle of Humankind." The famous "Turkana Boy" fossil, found in 1984, is one of the most complete early human skeletons ever discovered.',
        'category': 'precolonial',
        'year': -3000000,
        'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/Koobi_Fora_Hominid_Fossils.jpg/640px-Koobi_Fora_Hominid_Fossils.jpg'
    },
    {
        'title': 'The Swahili Coast Civilization',
        'content': 'From the 8th to 16th centuries, the Kenyan coast was home to thriving Swahili city-states like Mombasa, Malindi, and Lamu. These cities were major trading hubs connecting Africa with Arabia, India, and China, trading gold, ivory, and spices for silk and porcelain.',
        'category': 'precolonial',
        'year': 800,
        'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/b/b4/Lamu_Old_Town.jpg/640px-Lamu_Old_Town.jpg'
    },
    {
        'title': 'Fort Jesus - A UNESCO World Heritage Site',
        'content': 'Built by the Portuguese in 1593-1596, Fort Jesus in Mombasa is one of the most outstanding examples of 16th century military architecture. It changed hands nine times between the Portuguese and Arabs before being captured by the British in 1895. Today, it is a UNESCO World Heritage Site and museum.',
        'category': 'colonial',
        'year': 1593,
        'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Fort_Jesus_1.jpg/640px-Fort_Jesus_1.jpg'
    },
    {
        'title': 'The Uganda Railway and the Birth of Nairobi',
        'content': 'The construction of the Uganda Railway between 1896 and 1901 transformed Kenya. The railway was built by Indian laborers, over 2,500 of whom died during construction. The railway depot at Mile 327 became the city of Nairobi, now Kenya\'s capital and the economic hub of East Africa.',
        'category': 'colonial',
        'year': 1896,
        'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/6/6a/Uganda_Railway_Construction.jpg/640px-Uganda_Railway_Construction.jpg'
    },
    {
        'title': 'The Mau Mau Uprising',
        'content': 'The Mau Mau rebellion (1952-1960) was a pivotal armed struggle against British colonial rule. The Kikuyu-led uprising demanded land freedom and independence. Although brutally suppressed, the rebellion accelerated Kenya\'s path to independence and is now recognized as a heroic struggle for freedom.',
        'category': 'independence',
        'year': 1952,
        'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/9/9e/Dedan_Kimathi.jpg/640px-Dedan_Kimathi.jpg'
    },
    {
        'title': 'Jomo Kenyatta - The First President',
        'content': 'Jomo Kenyatta (c. 1897-1978) was Kenya\'s first President and a dominant figure in the independence struggle. He served as the first Prime Minister (1963-1964) and then President (1964-1978). His philosophy of "Harambee" (pulling together) became the national motto.',
        'category': 'leaders',
        'year': 1963,
        'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/7/7a/Jomo_Kenyatta_1966.jpg/640px-Jomo_Kenyatta_1966.jpg'
    },
    {
        'title': 'The Great Rift Valley',
        'content': 'The Great Rift Valley runs through Kenya from north to south, stretching over 6,000 kilometers from Syria to Mozambique. In Kenya, it is home to stunning lakes (Naivasha, Nakuru, Bogoria), volcanoes, and is a UNESCO World Heritage site for its paleontological significance.',
        'category': 'culture',
        'year': None,
        'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/0/0c/Great_Rift_Valley_Kenya.jpg/640px-Great_Rift_Valley_Kenya.jpg'
    },
    {
        'title': 'Wangari Maathai - Nobel Peace Prize Winner',
        'content': 'Professor Wangari Maathai (1940-2011) was the founder of the Green Belt Movement, which planted over 51 million trees in Kenya. In 2004, she became the first African woman to win the Nobel Peace Prize for her contribution to sustainable development, democracy, and peace.',
        'category': 'leaders',
        'year': 2004,
        'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/2/2b/Wangari_Maathai_in_2009.jpg/640px-Wangari_Maathai_in_2009.jpg'
    },
    {
        'title': 'The Kenyan Safari Experience',
        'content': 'Kenya is home to the "Big Five" (lion, leopard, elephant, rhino, buffalo) and the world-famous Great Migration, where over 1.5 million wildebeest and zebra cross the Mara River from Tanzania to Kenya. The Maasai Mara National Reserve is one of the most celebrated wildlife destinations on Earth.',
        'category': 'culture',
        'year': None,
        'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/46/Gnu_crossing_Mara_River.jpg/640px-Gnu_crossing_Mara_River.jpg'
    },
    {
        'title': 'The 2010 Constitution - A New Dawn',
        'content': 'The Constitution of Kenya 2010 was a landmark document that replaced the 1963 independence constitution. It introduced devolution, a Bill of Rights, an independent judiciary, and reduced presidential powers. It was approved by 67% of voters in a 2010 referendum.',
        'category': 'post_independence',
        'year': 2010,
        'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/4a/Kenya_Constitution_2010.jpg/640px-Kenya_Constitution_2010.jpg'
    },
]

for fact in history_facts:
    obj, created = DidYouKnowFact.objects.get_or_create(
        title=fact['title'],
        defaults=fact
    )
    if created:
        print(f"Added: {fact['title']}")
    else:
        print(f"Already exists: {fact['title']}")

print(f"\nTotal history facts: {DidYouKnowFact.objects.count()}")

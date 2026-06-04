from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

# Hardcoded history data for now
KENYAN_HISTORY_FACTS = [
    {
        "id": 1,
        "title": "The Kenyan Constitution 2010",
        "content": "The Constitution of Kenya 2010 was approved by 67% of voters in a referendum on August 4, 2010. It replaced the 1963 independence constitution and introduced devolution, a Bill of Rights, and an independent judiciary.",
        "category": "post_independence",
        "year": 2010
    },
    {
        "id": 2,
        "title": "Jomo Kenyatta - First President",
        "content": "Jomo Kenyatta (c. 1897 - 22 August 1978) was Kenya's first President. He served as Prime Minister from 1963 to 1964 and then as President from 1964 until his death in 1978. His philosophy of 'Harambee' (pulling together) became the national motto.",
        "category": "leaders",
        "year": 1963
    },
    {
        "id": 3,
        "title": "Fort Jesus, Mombasa",
        "content": "Fort Jesus was built by the Portuguese between 1593 and 1596. It is located on the coast of Mombasa and was designed to protect the port. Today it is a UNESCO World Heritage Site and one of Kenya's most visited tourist attractions.",
        "category": "colonial",
        "year": 1593
    },
    {
        "id": 4,
        "title": "Wangari Maathai - Nobel Peace Prize",
        "content": "Professor Wangari Maathai (1940-2011) was the founder of the Green Belt Movement, which planted over 51 million trees in Kenya. In 2004, she became the first African woman to win the Nobel Peace Prize for her contribution to sustainable development, democracy, and peace.",
        "category": "leaders",
        "year": 2004
    },
    {
        "id": 5,
        "title": "The Great Rift Valley",
        "content": "The Great Rift Valley runs through Kenya from north to south, stretching over 6,000 kilometers from Syria to Mozambique. In Kenya, it is home to stunning lakes (Naivasha, Nakuru, Bogoria), volcanoes, and is a UNESCO World Heritage site for its paleontological significance.",
        "category": "culture",
        "year": None
    },
    {
        "id": 6,
        "title": "Mau Mau Uprising",
        "content": "The Mau Mau rebellion (1952-1960) was a pivotal armed struggle against British colonial rule. The Kikuyu-led uprising demanded land freedom and independence. Although brutally suppressed, the rebellion accelerated Kenya's path to independence.",
        "category": "independence",
        "year": 1952
    },
    {
        "id": 7,
        "title": "Lamu Old Town",
        "content": "Lamu Old Town is the oldest continuously inhabited Swahili settlement in East Africa, dating back to the 14th century. It is a UNESCO World Heritage Site and remains a center for Swahili culture and Islamic learning.",
        "category": "culture",
        "year": None
    },
    {
        "id": 8,
        "title": "The Uganda Railway",
        "content": "The construction of the Uganda Railway between 1896 and 1901 transformed Kenya. The railway was built by Indian laborers, over 2,500 of whom died during construction. The railway depot at Mile 327 became the city of Nairobi.",
        "category": "colonial",
        "year": 1896
    },
]

class HistoryView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        category = request.query_params.get('category')
        if category and category != 'all':
            filtered = [f for f in KENYAN_HISTORY_FACTS if f['category'] == category]
            return Response(filtered)
        return Response(KENYAN_HISTORY_FACTS)

class RandomHistoryView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        import random
        random_fact = random.choice(KENYAN_HISTORY_FACTS)
        return Response(random_fact)

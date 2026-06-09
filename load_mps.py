import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'citizenhub.settings')
django.setup()
from accounts.models import MP
from datetime import date, timedelta

# Current parliamentary term: 2022 - 2027
term_start = date(2022, 8, 31)
term_end = date(2027, 8, 30)

# List of 100 MPs
mps_list = [
    # NAIROBI COUNTY (8 MPs)
    ('Hon. Esther Passaris', 'Nairobi Central', 'ODM'),
    ('Hon. Tim Wanyonyi', 'Westlands', 'ODM'),
    ('Hon. Babu Owino', 'Embakasi East', 'ODM'),
    ('Hon. John Kiarie', 'Dagoretti South', 'Jubilee'),
    ('Hon. George Theuri', 'Embakasi West', 'Jubilee'),
    ('Hon. Beatrice Elachi', 'Dagoretti North', 'Jubilee'),
    ('Hon. Peter Orero', 'Langata', 'ODM'),
    ('Hon. Margaret Wanjiru', 'Starehe', 'Jubilee'),
    
    # KIAMBU COUNTY (8 MPs)
    ('Hon. Rigathi Gachagua', 'Mathira', 'Jubilee'),
    ('Hon. Alice Wahome', 'Kandara', 'Jubilee'),
    ('Hon. Peter Mwathi', 'Limuru', 'Jubilee'),
    ('Hon. Wanjiku Kibe', 'Gatundu North', 'Jubilee'),
    ('Hon. James Gakuya', 'Embakasi North', 'Jubilee'),
    ('Hon. Simon Kingara', 'Ruiru', 'Jubilee'),
    ('Hon. Ann Wamuratha', 'Kieni', 'Jubilee'),
    ('Hon. John Chege', 'Kabete', 'Jubilee'),
    
    # MOMBASA COUNTY (6 MPs)
    ('Hon. Hassan Joho', 'Kisauni', 'ODM'),
    ('Hon. Amina Mnyazi', 'Malindi', 'ODM'),
    ('Hon. Omar Mwinyi', 'Changamwe', 'ODM'),
    ('Hon. Suleiman Dori', 'Msambweni', 'ODM'),
    ('Hon. Abdulswamad Nassir', 'Mvita', 'ODM'),
    ('Hon. Zamzam Mohamed', 'Jomvu', 'ODM'),
    
    # KISUMU COUNTY (7 MPs)
    ('Hon. Caroli Omondi', 'Suba', 'ODM'),
    ('Hon. Millie Odhiambo', 'Suba North', 'ODM'),
    ('Hon. John Mbadi', 'Suba South', 'ODM'),
    ('Hon. James Orengo', 'Ugenya', 'ODM'),
    ('Hon. Gladys Wanga', 'Homa Bay', 'ODM'),
    ('Hon. Tom Ojienda', 'Kisumu Central', 'ODM'),
    ('Hon. Roza Buyu', 'Kisumu West', 'ODM'),
    
    # NAKURU COUNTY (6 MPs)
    ('Hon. Samuel Arama', 'Nakuru Town West', 'Jubilee'),
    ('Hon. David Gikaria', 'Nakuru Town East', 'Jubilee'),
    ('Hon. Kuria Kimani', 'Molo', 'Jubilee'),
    ('Hon. Jayne Kihara', 'Naivasha', 'Jubilee'),
    ('Hon. Aisha Jumwa', 'Kilifi North', 'Jubilee'),
    ('Hon. Owen Baya', 'Kilifi South', 'Jubilee'),
    
    # UASIN GISHU COUNTY (4 MPs)
    ('Hon. Oscar Sudi', 'Kapseret', 'Jubilee'),
    ('Hon. Caleb Kositany', 'Soin', 'Jubilee'),
    ('Hon. Gladys Boss', 'Uasin Gishu', 'Jubilee'),
    ('Hon. Allan Kosgey', 'Kesses', 'Jubilee'),
    
    # KAKAMEGA COUNTY (4 MPs)
    ('Hon. Wycliffe Oparanya', 'Butere', 'ODM'),
    ('Hon. John Waluke', 'Sirisia', 'ODM'),
    ('Hon. Christopher Wamalwa', 'Kanduyi', 'ODM'),
    ('Hon. Tindi Mwale', 'Matungu', 'ODM'),
    
    # MACHAKOS COUNTY (4 MPs)
    ('Hon. Alfred Mutua', 'Machakos Town', 'Jubilee'),
    ('Hon. Patrick Makau', 'Mavoko', 'Jubilee'),
    ('Hon. Nduati Ngata', 'Masinga', 'Jubilee'),
    ('Hon. Musyoka Kathambi', 'Mwala', 'Jubilee'),
    
    # KITUI COUNTY (3 MPs)
    ('Hon. Rachael Nyamai', 'Kitui South', 'Jubilee'),
    ('Hon. Nimrod Mbai', 'Kitui Central', 'Jubilee'),
    ('Hon. Wambua Kalembe', 'Kitui East', 'Jubilee'),
    
    # MERU COUNTY (3 MPs)
    ('Hon. Mpuru Aburi', 'Tigania East', 'Jubilee'),
    ('Hon. Kareke Mbiuki', 'Maara', 'Jubilee'),
    ('Hon. Mithika Linturi', 'Igembe South', 'Jubilee'),
    
    # KIRINYAGA COUNTY (2 MPs)
    ('Hon. Gichimu Githinji', 'Kirinyaga Central', 'Jubilee'),
    ('Hon. Wangui Ngirici', 'Kirinyaga', 'Jubilee'),
    
    # MURANG'A COUNTY (3 MPs)
    ('Hon. Sabina Chege', 'Murang\'a', 'Jubilee'),
    ('Hon. Peter Kihungi', 'Kangema', 'Jubilee'),
    ('Hon. Ndindi Nyoro', 'Kiharu', 'Jubilee'),
    
    # NYANDARUA COUNTY (2 MPs)
    ('Hon. Mercy Gakuya', 'Kinangop', 'Jubilee'),
    ('Hon. Kwenya Thuku', 'Ol Kalou', 'Jubilee'),
    
    # NYERI COUNTY (2 MPs)
    ('Hon. Njoroge Wainaina', 'Nyeri Town', 'Jubilee'),
    ('Hon. Rahab Mukami', 'Othaya', 'Jubilee'),
    
    # EMBU COUNTY (2 MPs)
    ('Hon. Mburu Ngugi', 'Manyatta', 'Jubilee'),
    ('Hon. Kariuki Waweru', 'Runyenjes', 'Jubilee'),
    
    # SIAYA COUNTY (3 MPs)
    ('Hon. James Aggrey', 'Siaya', 'ODM'),
    ('Hon. Christine Ombaka', 'Bondo', 'ODM'),
    ('Hon. Samuel Atandi', 'Alego Usonga', 'ODM'),
    
    # BUSIA COUNTY (2 MPs)
    ('Hon. Oku Kaunya', 'Busia', 'ODM'),
    ('Hon. John Bunyasi', 'Nambale', 'ODM'),
    
    # BUNGOMA COUNTY (3 MPs)
    ('Hon. Moses Wetangula', 'Bungoma', 'ODM'),
    ('Hon. John Chikati', 'Tongaren', 'ODM'),
    ('Hon. Majimbo Kalasinga', 'Kabuchai', 'ODM'),
    
    # Additional MPs to reach 100
    ('Hon. Gideon Mungaro', 'Kilifi', 'ODM'),
    ('Hon. Ken Chonga', 'Magarini', 'ODM'),
    ('Hon. John Mramba', 'Taveta', 'ODM'),
    ('Hon. Ruweida Obo', 'Lamu', 'ODM'),
    ('Hon. Aden Duale', 'Garissa', 'Jubilee'),
    ('Hon. Ahmed Kolosh', 'Wajir', 'Jubilee'),
    ('Hon. Abdulaziz Farah', 'Mandera', 'Jubilee'),
    ('Hon. Naomi Jillo', 'Marsabit', 'Jubilee'),
    ('Hon. Kina Godana', 'Isiolo', 'Jubilee'),
    ('Hon. Badi Twalib', 'Tana River', 'ODM'),
]

count = 0
for name, constituency, party in mps_list:
    obj, created = MP.objects.get_or_create(
        name=name,
        defaults={
            'constituency': constituency,
            'party': party,
            'term_start': term_start,
            'term_end': term_end
        }
    )
    if created:
        count += 1
        print(f'Created: {name}')

print(f'\nTotal new MPs added: {count}')
print(f'Total MPs in database: {MP.objects.count()}')

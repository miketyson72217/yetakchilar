import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import Leader, Journal, Quote, Application

# 1. Superuser
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@yetakchilar.uz', 'admin123')
    print('Superuser created: admin / admin123')
else:
    print('Superuser admin already exists')

# 2. Leaders with full names (Ism Familiya Otasining ismi)
leaders_data = [
    {
        'name': 'Kamalova Maftuna Zoxirovna',
        'sphere': 'biznes',
        'region': 'Buxoro',
        'photo': 'images/leader2.png',
        'short_bio': 'Mehmonxona menejmentida yetakchi va ilhom baxsh etuvchi yosh mutaxassis',
        'full_bio': 'Maftuna Kamalova — 4 yulduzli mehmonxonada faoliyat yuritayotgan yosh mutaxassis. Karuta Taikai Respublika bosqichi 1-o‘rni sohibasi (2023), Kaizen sertifikati va Vatel Hotel Management mutaxassisi.',
        'birth_date': '1-oktabr 1999-yil',
        'birth_place': 'Buxoro shahri',
        'education': 'Oliy (Vatel Hotel Management)',
        'top100_rank': 1,
        'is_featured': True
    },
    {
        'name': 'Yusupova Malika Rustamovna',
        'sphere': 'biznes',
        'region': 'Toshkent',
        'photo': 'images/leader2.png',
        'short_bio': 'Tadbirkor & CEO',
        'full_bio': 'Muvaffaqiyatli tadbirkor, xalqaro startap muallifi va 100 dan ortiq yoshlarga ustozlik qilgan biznes yetakchisi.',
        'birth_date': '15-may 1998-yil',
        'birth_place': 'Toshkent shahri',
        'education': 'Oliy (WESTMINSTER)',
        'top100_rank': 2,
        'is_featured': True
    },
    {
        'name': 'Alimov Javohir Otabekovich',
        'sphere': 'texno',
        'region': 'Samarqand',
        'photo': 'images/leader1.png',
        'short_bio': 'Texnologiya & IT Innovatori',
        'full_bio': 'Sunʻiy intellekt va dasturlash sohasidagi innovator. Bir necha xalqaro hackathonlar gʻolibi va AI platformasi muallifi.',
        'birth_date': '10-iyun 2000-yil',
        'birth_place': 'Samarqand shahri',
        'education': 'Oliy (INHA)',
        'top100_rank': 3,
        'is_featured': True
    },
    {
        'name': 'Karimova Zebo Bobur qizi',
        'sphere': 'sport',
        'region': 'Toshkent',
        'photo': 'images/leader2.png',
        'short_bio': 'Olimpiya Chempioni',
        'full_bio': 'Xalqaro toifadagi sport ustasi, Olimpiya oʻyinlari oltin medali sohibasi.',
        'birth_date': '22-avgust 2001-yil',
        'birth_place': 'Toshkent shahri',
        'education': 'Oliy (Jismoniy Tarbiya Instituti)',
        'top100_rank': 4,
        'is_featured': True
    },
    {
        'name': 'Ismoilov Said Anvarovich',
        'sphere': 'biznes',
        'region': 'Buxoro',
        'photo': 'images/leader1.png',
        'short_bio': 'Moliya & Investitsiya Mutaxassisi',
        'full_bio': 'Venchur fondlar va yashil energetika loyihalari investori.',
        'birth_date': '5-fevral 1997-yil',
        'birth_place': 'Buxoro shahri',
        'education': 'Oliy (TDIU)',
        'top100_rank': 5,
        'is_featured': True
    },
    {
        'name': 'Umarova Dilnoza Sherzodovna',
        'sphere': 'tibbiyot',
        'region': 'Namangan',
        'photo': 'images/leader2.png',
        'short_bio': 'Fan & Tibbiyot Olima',
        'full_bio': 'Tibbiyot fanlari nomzodi, biotexnologiyalar va genom tadqiqotlari boʻyicha izlanuvchi.',
        'birth_date': '12-noyabr 1996-yil',
        'birth_place': 'Namangan shahri',
        'education': 'Oliy (Toshkent Tibbiyot Akademiyasi)',
        'top100_rank': 6,
        'is_featured': True
    }
]

for ldata in leaders_data:
    leader = Leader.objects.filter(name__icontains=ldata['name'].split()[0]).first()
    if leader:
        leader.name = ldata['name']
        leader.sphere = ldata['sphere']
        leader.region = ldata['region']
        leader.short_bio = ldata['short_bio']
        leader.full_bio = ldata['full_bio']
        leader.save() # Triggers Leader.save() to generate name-patronymic-uuid slug
        print(f'Leader updated: {leader.name} -> slug: {leader.slug}')
    else:
        new_leader = Leader.objects.create(
            name=ldata['name'],
            sphere=ldata['sphere'],
            region=ldata['region'],
            photo=ldata['photo'],
            short_bio=ldata['short_bio'],
            full_bio=ldata['full_bio'],
            birth_date=ldata['birth_date'],
            birth_place=ldata['birth_place'],
            education=ldata['education'],
            top100_rank=ldata['top100_rank'],
            is_featured=ldata['is_featured']
        )
        print(f'Leader created: {new_leader.name} -> slug: {new_leader.slug}')

# 3. Journal
if not Journal.objects.filter(issue_number=1).exists():
    Journal.objects.create(
        issue_number=1,
        title='YETAKCHILAR: Yangi avlod muvaffaqiyat sirlari',
        description='Ushbu jurnalda Oʻzbekistonning turli sohalarida ulkan zafarlarga erishgan eng faol va ilhomlantiruvchi yosh yetakchilarning hayotiy tajribalari aks etgan.',
        front_cover='images/journal_cover.png',
        back_cover='images/journal_back_cover.png',
        pdf_file='downloads/yetakchilar_jurnal_1_son.pdf',
        pages_count=48,
        issn='ISSN 2023-1234',
        release_date='Iyun 2024',
        is_active=True
    )
    print('Journal Issue 1 created')

# 4. Quotes
quotes_data = [
    {
        'quote_text': 'Muvaffaqiyat — bu tasodif emas, balki har kuni qilinadigan toʻgʻri tanlovlar natijasida.',
        'author_name': 'Yusupova Malika Rustamovna',
        'author_title': 'Tadbirkor & CEO',
        'is_featured': True
    },
    {
        'quote_text': 'Texnologiya — bu faqat vosita. Asosiy kuch — insonning aqli va ijodiy tafakkuridir.',
        'author_name': 'Alimov Javohir Otabekovich',
        'author_title': 'Texnologiya Innovatori',
        'is_featured': True
    },
    {
        'quote_text': 'Sport menga hayotda ham, kasbda ham oldinga intilishni oʻrgatdi. Har qanday toʻsiqni yengish mumkin.',
        'author_name': 'Karimova Zebo Bobur qizi',
        'author_title': 'Olimpiya Chempioni',
        'is_featured': True
    }
]

for qdata in quotes_data:
    quote, created = Quote.objects.get_or_create(
        author_name=qdata['author_name'],
        defaults={
            'quote_text': qdata['quote_text'],
            'author_title': qdata['author_title'],
            'is_featured': qdata['is_featured']
        }
    )
    if created:
        print(f'Quote created for {qdata["author_name"]}')

print("Demo data successfully updated!")

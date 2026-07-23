import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import Leader, Journal, Application

# 1. Superuser
admin_username = os.environ.get('SUPERUSER_NAME', 'admin_yt_8f9a2b')
admin_password = os.environ.get('SUPERUSER_PASS', 'P@ss_9k2m4x7q8v')

if not User.objects.filter(username=admin_username).exists():
    User.objects.create_superuser(admin_username, 'admin@yetakchilar.uz', admin_password)
    print(f'Superuser created: {admin_username} / {admin_password}')
else:
    u = User.objects.get(username=admin_username)
    u.set_password(admin_password)
    u.save()
    print(f'Superuser password updated for: {admin_username}')


# 2. Leaders with full names (Ism Familiya Otasining ismi)
leaders_data = [
    {
        'name': 'Kamalova Maftuna Zoxirovna',
        'sphere': 'biznes',
        'region': 'Buxoro',
        'photo': 'images/leader2.png',
        'short_bio': 'Mehmonxona menejmentida yetakchi va ilhom baxsh etuvchi yosh mutaxassis',
        'full_bio': 'Maftuna Kamalova — 4 yulduzli mehmonxonada faoliyat yuritayotgan yosh mutaxassis. Karuta Taikai Respublika bosqichi 1-oʻrni sohibasi (2023), Kaizen sertifikati va Vatel Hotel Management mutaxassisi.',
        'birth_date': '1-oktabr 1999-yil',
        'birth_place': 'Buxoro shahri',
        'education': 'Oliy (Vatel Hotel Management)',
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
        'is_featured': True
    },
    {
        'name': 'Alimov Javohir Otabekovich',
        'sphere': 'texno',
        'region': 'Samarqand',
        'photo': 'images/leader1.png',
        'short_bio': 'Texnologiya & IT Innovatori',
        'full_bio': 'Sunʼiy intellekt va dasturlash sohasidagi innovator. Bir necha xalqaro hackathonlar gʻolibi va AI platformasi muallifi.',
        'birth_date': '10-iyun 2000-yil',
        'birth_place': 'Samarqand shahri',
        'education': 'Oliy (INHA)',
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



print("Demo data successfully updated!")

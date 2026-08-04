import os
import django
from django.core.files import File
import sys

# Set up Django environment
sys.path.append('/home/lochinbek/Desktop/yetakchilar')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from core.models import Leader

mapping = {
    '1.png': "YUSUFJON YUSUFOV",
    '2.png': "ESHQULOVA MARJONA",
    '3.png': "AKROMOVA MO'MINAXON",
    '4.png': "SAFAROVA SHAHLO",
    '5.png': "ORIFJONOVA SHAHZODA",
    '6.png': "SHOKIROVA SHABNAM",
    '7.png': "ZILOLA QUDRATILLAYEVA",
    '8.png': "MAXSUDBEKOVA FAROG'AT",
    '9.png': "FARMONOVA MOHINUR",
    '10.png': "G'ULOMJONOVA SARVINOZ",
    '11.png': "AZADOVA MEHRIBON",
    '12.png': "ODILOVA MADINA",
    '13.png': "ZIYADULLAYEVA SABRINA",
    '14.png': "JUMANAZAROVA ZAYNABXON",
    '15.png': "SAPARBOYEVA LAYLO",
    '16.png': "SOBIROVA HUSNIRABONU",
}

base_dir = '/home/lochinbek/Desktop/yetakchilar/kvadratrasmlarniyangilash'

for filename, name_part in mapping.items():
    found = False
    for leader in Leader.objects.all():
        db_name = leader.name.lower().replace("‘", "'").replace("ʼ", "'")
        search_name = name_part.lower().replace("‘", "'").replace("ʼ", "'")
        
        parts = search_name.split()
        if all(part in db_name for part in parts):
            print(f"Match found: {leader.name} for {filename}")
            img_path = os.path.join(base_dir, filename)
            with open(img_path, 'rb') as f:
                # Use a cleaner filename or just keep it
                new_filename = f"{leader.slug}_1x1.png"
                leader.quote_poster_1x1.save(new_filename, File(f), save=True)
            found = True
            break
            
    if not found:
        print(f"Could not find match for {name_part} ({filename})")

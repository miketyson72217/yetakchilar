import os
import uuid
import django
import sys

# Setup Django environment
sys.path.append('/home/lochinbek/Desktop/yetakchilar')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from core.models import Leader
from django.core.files.base import ContentFile

def main():
    # mapping of (first_name or part of name) -> (16:9 filename, 1:1 filename)
    people_map = {
        "yusufjon": ("1.png", "1.png"),
        "safarova": ("2.png", "4.png"),
        "orifjonova": ("3.png", "5.png"),
        "akromova": ("4.png", "3.png"),
        "shokirova": ("5.png", "6.png"),
        "qudratillayeva": ("6.png", "7.png"), # Zilola Qudratillayeva
        "eshqulova": ("7.png", "2.png"),
        "maxsudbekova": ("8.png", "8.png"),
        "farmonova": ("9.png", "9.png"),
        "g‘ulomjonova": ("10.png", "10.png"), # Notice the '‘' instead of "'"
        "azadova": ("11.png", "11.png"),
        "odilova": ("12.png", "12.png"),
        "ziyadullayeva": ("13.png", "13.png"),
        "jumanazarova": ("14.png", "14.png"),
        "saparboyeva": ("15.png", "15.png"),
        "sobirova": ("16.png", "16.png"),
        "komiljanova": ("17.png", "17.png"),
        "yusupova": ("18.png", "18.png"),
        "muqimova": ("19.png", "19.png"),
    }

    dir_16_9 = '/home/lochinbek/Desktop/yetakchilar/16:9 iqtibos rasmi'
    dir_1_1 = '/home/lochinbek/Desktop/yetakchilar/1:1 iqtibos rasmi'
    
    leaders = Leader.objects.all()
    count = 0
    for leader in leaders:
        name_lower = leader.name.lower().replace("'", "‘").replace("’", "‘")
        
        matched_key = None
        for key in people_map.keys():
            # Handle possible apostrophe differences
            search_key = key.replace("'", "‘")
            if search_key in name_lower:
                matched_key = key
                break
        
        if matched_key:
            f_16_9, f_1_1 = people_map[matched_key]
            
            # Read 16:9
            path_16_9 = os.path.join(dir_16_9, f_16_9)
            if os.path.exists(path_16_9):
                with open(path_16_9, 'rb') as f:
                    content_16 = f.read()
                new_name_16 = f"leaders/quotes/{uuid.uuid4()}.png"
                leader.quote_poster.storage.save(new_name_16, ContentFile(content_16))
                
                # Delete old if exists
                if leader.quote_poster and leader.quote_poster.name:
                    try:
                        leader.quote_poster.storage.delete(leader.quote_poster.name)
                    except Exception:
                        pass
                        
                leader.quote_poster.name = new_name_16
            
            # Read 1:1
            path_1_1 = os.path.join(dir_1_1, f_1_1)
            if os.path.exists(path_1_1):
                with open(path_1_1, 'rb') as f:
                    content_1 = f.read()
                new_name_1 = f"leaders/quotes/1x1/{uuid.uuid4()}.png"
                leader.quote_poster_1x1.storage.save(new_name_1, ContentFile(content_1))
                
                # Delete old if exists
                if leader.quote_poster_1x1 and leader.quote_poster_1x1.name:
                    try:
                        leader.quote_poster_1x1.storage.delete(leader.quote_poster_1x1.name)
                    except Exception:
                        pass
                
                leader.quote_poster_1x1.name = new_name_1
            
            leader.save(update_fields=['quote_poster', 'quote_poster_1x1'])
            print(f"Updated quote images for {leader.name}")
            count += 1
            
    print(f"Total updated: {count}")

if __name__ == '__main__':
    main()

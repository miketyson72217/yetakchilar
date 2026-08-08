import os
import django
import re

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from core.models import Opportunity

for opp in Opportunity.objects.all():
    if opp.age_category:
        val = opp.age_category.strip()
        # if there is a number and no 'yosh' in it, append 'yosh'
        if re.search(r'\d', val) and 'yosh' not in val.lower():
            opp.age_category = val + ' yosh'
            opp.save()
            print(f"Updated '{opp.title}': '{val}' -> '{opp.age_category}'")

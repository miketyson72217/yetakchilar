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

def rename_photos():
    for leader in Leader.objects.all():
        if leader.photo:
            old_name = leader.photo.name
            if not old_name:
                continue
            
            try:
                if not leader.photo.storage.exists(old_name):
                    print(f"File not found in storage for {leader.name}: {old_name}")
                    continue
            except Exception as e:
                print(f"Error checking {old_name}: {e}")
                continue
            
            filename = os.path.basename(old_name)
            name_part = filename.rsplit('.', 1)[0]
            
            try:
                # Check if it's already a valid UUID
                uuid.UUID(name_part)
                print(f"Already UUID: {filename}")
                continue
            except ValueError:
                pass
            
            ext = old_name.split('.')[-1]
            new_filename = f"{uuid.uuid4()}.{ext}"
            new_name = os.path.join('leaders', new_filename)
            
            try:
                # Read content from old file
                with leader.photo.storage.open(old_name, 'rb') as old_file:
                    content = old_file.read()
                
                # Save to new file
                leader.photo.storage.save(new_name, ContentFile(content))
                
                # Delete old file
                leader.photo.storage.delete(old_name)
                
                # Update DB
                leader.photo.name = new_name
                leader.save(update_fields=['photo'])
                print(f"Renamed {old_name} to {new_name} for {leader.name}")
            except Exception as e:
                print(f"Error renaming {old_name}: {e}")

if __name__ == '__main__':
    rename_photos()

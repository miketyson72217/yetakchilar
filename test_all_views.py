import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.conf import settings
settings.ALLOWED_HOSTS = ['testserver']
settings.SECURE_SSL_REDIRECT = False

from django.test import Client
from django.urls import get_resolver

client = Client(enforce_csrf_checks=False)
resolver = get_resolver()

def get_all_urls(url_patterns, prefix=''):
    urls = []
    for pattern in url_patterns:
        if hasattr(pattern, 'url_patterns'):
            urls.extend(get_all_urls(pattern.url_patterns, prefix + str(pattern.pattern)))
        else:
            urls.append(prefix + str(pattern.pattern))
    return urls

all_urls = get_all_urls(resolver.url_patterns)

for url in all_urls:
    if '<' in url or '^' in url or '$' in url:
        continue
    
    if not url.startswith('/'):
        url = '/' + url

    if not url.endswith('/'):
        url += '/'

    print(f"Testing {url} ...")
    try:
        response = client.get(url, secure=True)
        print(f"  -> Status: {response.status_code}")
        if response.status_code >= 500:
            print(f"  -> ERROR on {url} !!")
    except Exception as e:
        print(f"  -> EXCEPTION on {url}: {e}")


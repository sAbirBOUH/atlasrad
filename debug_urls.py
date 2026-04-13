import os
import django
from django.urls import get_resolver
from django.urls.resolvers import URLResolver

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'atlasrad_backend.settings')
django.setup()

def show_urls(patterns, prefix=''):
    for pattern in patterns:
        if isinstance(pattern, URLResolver):
            show_urls(pattern.url_patterns, prefix + str(pattern.pattern))
        else:
            print(f"URL: {prefix}{str(pattern.pattern)}")

print("--- REGISTERED URLS ---")
show_urls(get_resolver().url_patterns)
print("-----------------------")

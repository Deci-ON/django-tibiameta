# myapp/sitemap.py

from django.contrib.sitemaps import Sitemap
from django.urls import reverse

class MySitemap(Sitemap):
    def items(self):
        # Retorne uma lista de URLs que você deseja incluir no sitemap
        return ['index', 'charactersearch', 'loot_split']
    
    def location(self, item):
        # Retorne a URL para cada item do sitemap
        return reverse(item)

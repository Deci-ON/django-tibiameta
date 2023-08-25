# sitemaps.py
from django.urls import reverse
from django.contrib.sitemaps import Sitemap

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = "daily"

    def items(self):
        urls = ["index", "characterinfo"]  # Adicione outras URLs aqui
        print("Returning URLs:", urls)
        return urls

    def location(self, item):
        return reverse(item)
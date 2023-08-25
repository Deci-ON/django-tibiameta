from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.sitemaps import Sitemap


def index(request):
  return render(request, 'tibiameta/index.html')

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = "daily"

    def items(self):
        urls = ["index", "characterinfo"]  # Adicione outras URLs aqui
        return urls

    def location(self, item):
        return reverse(item)

def sitemap(request):
    sitemap = StaticViewSitemap()
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for item in sitemap.items():
        xml += '<url>\n'
        xml += f'<loc>{request.build_absolute_uri(reverse(item))}</loc>\n'
        xml += f'<changefreq>{sitemap.changefreq}</changefreq>\n'
        xml += f'<priority>{sitemap.priority}</priority>\n'
        xml += '</url>\n'
    xml += '</urlset>'
    return HttpResponse(xml, content_type="application/xml")

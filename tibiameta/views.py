from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.sitemaps import Sitemap
from django.db import connections
import requests



def index(request):
    boss_link = 'https://api.tibiadata.com/v3/boostablebosses'
    creature_link = 'https://api.tibiadata.com/v3/creatures'
    timeout = 10
    try:
        response = requests.get(boss_link, timeout=timeout)
        if response.status_code == 200:
            data = response.json()
            data = data.get('boostable_bosses')
            data = data.get('boosted')
            boss_name = data.get('name')
            boss_url = data.get('image_url')
    except Exception:
        pass
    try:
        response = requests.get(creature_link, timeout=timeout)
        if response.status_code == 200:
            data = response.json()
            data = data.get('creatures')
            data = data.get('boosted')
            creature_name = data.get('name')
            creature_url = data.get('image_url')
    except Exception:
        pass
    
    try:
        with connections['tibia_meta'].cursor() as cursor:
            cursor.execute(f"SELECT rashid_day, rashid_city, rashid_location FROM tibia_stats.rashid_table where rashid_day in (SELECT IF(HOUR(NOW()) >= 5, DAYNAME(NOW() ), DAYNAME(NOW()+ INTERVAL 1 DAY )) AS day);")
            rows = cursor.fetchall()
            city = (rows[0][1])
            context = {
        'city': city,
        'boss_name': boss_name,
        'boss_url': boss_url,
        'creature_name': creature_name,
        'creature_url': creature_url
            }
    except Exception:
        pass

    return render(request, 'tibiameta/index.html', context )

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

from django.shortcuts import render
from django.http import HttpResponse
from django.db import connections
import requests
import json
from .forms import WorldForm
from datetime import date



# Create your views here.
def onopenpage(request):
    try:
        with connections['tibia_meta'].cursor() as cursor:
            cursor.execute(f"SELECT TIME_FORMAT(char_date, '%H:00') AS hora, ROUND(AVG(char_count)) AS media_char_count FROM tibia_stats.char_count_hist WHERE char_date >= CURDATE() AND char_date < CURDATE() + INTERVAL 1 DAY GROUP BY DATE(char_date), HOUR(char_date) ORDER BY hora;")
            rows = cursor.fetchall()
            hour = [row[0] for row in rows]
            average = [int(row[1]) for row in rows]

            cursor.execute(f"SELECT distinct char_world FROM tibia_stats.char_count_hist")
            worlds = cursor.fetchall()
            choices = [(world[0], world[0]) for world in worlds]
            world_form = WorldForm(choices=choices)
            context ={
                'on_open': True,
                'hour_list': json.dumps(hour),
                'average_list': json.dumps(average),
                'world_form': world_form,
            }
            return render(request, 'tibiameta/worldsinfos.html', context)
    except Exception as e:
        print(e)
    
    return render(request, 'tibiameta/worldsinfos.html')

def searchbyworld(request):
    if request.method == 'POST':
        world_form = WorldForm(request.POST)
        selected_world = request.POST.get('world')
        selected_date = request.POST.get('calendario')
        if selected_date == '':
            selected_date = str(date.today())
            print(selected_date)
        worldlink = f'https://api.tibiadata.com/v3/world/{selected_world}'
        timeout = 10
        with connections['tibia_meta'].cursor() as cursor:
            try:
                cursor.execute(f"SELECT TIME_FORMAT(char_date, '%H:00') AS hora, ROUND(AVG(char_count)) AS media_char_count FROM tibia_stats.char_count_hist WHERE convert(char_date, date) = '{selected_date}' and char_world = '{selected_world}' GROUP BY DATE(char_date), HOUR(char_date) ORDER BY hora;")
                rows = cursor.fetchall()
                hour = [row[0] for row in rows]
                average = [int(row[1]) for row in rows]
                cursor.execute(f"SELECT distinct char_world FROM tibia_stats.char_count_hist")
                worlds = cursor.fetchall()
                choices = [(world[0], world[0]) for world in worlds]
                world_form = WorldForm(choices=choices)
            except Exception:
                pass
            try:
                response = requests.get(worldlink, timeout=timeout)
                if response.status_code == 200:
                    data = response.json()
                    status = data['worlds']['world'].get('status')
                    players_online = data['worlds']['world'].get('players_online')
                    record_players = data['worlds']['world'].get('record_players')
                    record_date = data['worlds']['world'].get('record_date')
                    creation_date = data['worlds']['world'].get('creation_date')
                    location = data['worlds']['world'].get('location')
                    pvp_type = data['worlds']['world'].get('pvp_type')
                    premium_only = data['worlds']['world'].get('premium_only')
                    battleye_protected = data['worlds']['world'].get('battleye_protected')
                    battleye_date = data['worlds']['world'].get('battleye_date')
                    game_world_type = data['worlds']['world'].get('game_world_type')
                    
            except Exception:
                pass
            context ={
                'hour_list': json.dumps(hour),
                'average_list': json.dumps(average),
                'world_form': world_form,
                'selected_world': selected_world,
                'selected_date': selected_date,
                'status': status,
                'players_online': players_online,
                'record_players': record_players,
                'record_date': record_date,
                'creation_date': creation_date,
                'location': location,
                'pvp_type': pvp_type,
                'premium_only': premium_only,
                'battleye_protected': battleye_protected,
                'battleye_date': battleye_date,
                'game_world_type': game_world_type
                
            }
            return render(request, 'tibiameta/worldsinfos.html', context)            

from django.shortcuts import render
from django.http import HttpResponse
from django.db import connections
from django.http import JsonResponse
from datetime import timedelta, datetime
import requests
import json
import re
import time
import math

# Create your views here.
def characterinfo(request):
  char_info_ref_list = []  # Lista para armazenar char_info_ref
  char_exp_change_list = []  # Lista para armazenar char_exp_change
  timeout = 10
  character = request.GET.get('character')
  char_info = f'https://api.tibiadata.com/v3/character/{character}'
  MAX_RETRIES = 3
  api_status = True
  query_status = True
  ip_address = request.META.get('REMOTE_ADDR')  
  online = 'Offline'
  hitpoints = 0
  mana = 0
  cap = 0
  min_level = 0
  max_level = 0


  
  if character == '' or any(str.isdigit(c) for c in character) == True:
    error_message= 'Character Not Found'
    context = {
    'error': error_message
    }
    return render(request, 'tibiameta/index.html', context)
  else:
      padrao = re.compile(r'[^a-zA-Z0-9 \'-]+')
      if re.search(padrao, character):
        error_message= 'Character Not Found'
        context = {
        'error': error_message
        }
        return render(request, 'tibiameta/index.html', context)
    
    
  #Busca char na API.
  retries = 0
  while retries < MAX_RETRIES:
      try:
          response = requests.get(char_info, timeout=timeout)
          if response.status_code == 200:
            data = response.json()
            char_name = data['characters']['character'].get('name')
            if char_name !='':
              link = f'https://tibiameta.com/charactersearch/?character={char_name}'
              api_status = True
              level = data['characters']['character']['level']
              max_level = (level/2)
              max_level = math.ceil(max_level*3)
              min_level = (level/3)
              min_level = math.ceil(min_level*2)
              world = data['characters']['character']['world']
              vocation = data['characters']['character']['vocation']
              if vocation in ('Knight', 'Elite Knight'):
                hitpoints = (level-8) * 15 + 185
                mana = level * 5 + 50
                cap = (level-8) * 25 + 470
              elif vocation in ('Royal Paladin', 'Paladin'):
                hitpoints = (level-8) * 10 + 185
                mana = (level-8) * 15 + 90
                cap = (level-8) * 20 + 470
              elif vocation in ('Sorcerer', 'Master Sorcerer', 'Druid', 'Elder Druid'):
                hitpoints = level * 5 + 185
                mana = (level-8) * 30 + 90
                cap = level * 10 + 400
              else:
                hitpoints = level * 5 + 50
                mana = level * 5 + 145
                cap = level * 10 + 400                 
              #Busca se esta online
              try:
                response = requests.get(f'https://api.tibiadata.com//v3/world/{world}', timeout=timeout)
                if response.status_code == 200:
                  data_world = response.json()
                  online_players = data_world["worlds"]["world"]["online_players"]
                  online = 'Online' if any(player["name"] == char_name for player in online_players) else 'Offline'
              except requests.exceptions.RequestException as e:
                retries += 1
                wait_time = retries * 5  # Aumenta o tempo de espera a cada tentativa
                time.sleep(wait_time)
            else:
              api_status = False
              if retries == MAX_RETRIES:
                api_status == False
                break
              else:
                # Esperar um tempo antes de tentar novamente
                wait_time = retries * 1  # Aumenta o tempo de espera a cada tentativa
                time.sleep(wait_time)
          else:
            char_name = None
          if char_name == None:
            api_status = False
            retries += 1
            if retries == MAX_RETRIES:
              api_status == False
              break
            else:
              # Esperar um tempo antes de tentar novamente
              wait_time = retries * 1  # Aumenta o tempo de espera a cada tentativa
              time.sleep(wait_time)
                  
      except requests.exceptions.RequestException as e:
          api_status = False
          retries += 1
          if retries == MAX_RETRIES:
            api_status == False
          else:
            # Esperar um tempo antes de tentar novamente
            wait_time = retries * 5  # Aumenta o tempo de espera a cada tentativa
            time.sleep(wait_time)
      else:
        break
      
  #Busca char no banco
  try:
    character = character.replace("'","''")  
    with connections['tibia_meta'].cursor() as cursor:
      cursor.execute(f"select * FROM (SELECT char_info_ref, format(char_exp,0) as char_exp, format(char_exp_change,0) as char_exp_change, char_level, char_world, coalesce (SEC_TO_TIME(char_time*60),'00:00:00') as online_time, FORMAT(COALESCE(ROUND((char_exp_change / char_time ),2) * 60, CHAR_EXP_CHANGE),0) as exp_hour, char_world_rank, char_voc_rank FROM tibia_stats.char_experience_calc where char_name = '{character}' order by char_info_ref desc limit 31)a order by char_info_ref asc;")
      rows= cursor.fetchall()
      if rows:
          total_hours = 0
          columns = [col[0] for col in cursor.description]
          char_info_ref_list = [row[0].strftime('%m-%d') for row in rows]
          char_exp_change_list = [row[2].replace(',', '') for row in rows]
          lista_de_inteiros = [int(string) for string in char_exp_change_list]
          char_exp_change_avg = int(sum(lista_de_inteiros)/len(char_exp_change_list))
          char_exp_change_avg = "{:,}".format(char_exp_change_avg)
          total_char_change_exp = sum([int(x) for x in char_exp_change_list])
          total_char_change_exp_h = total_char_change_exp
          total_char_change_exp = "{:,}".format(total_char_change_exp)
          char_time_list = [row[5] for row in rows]  # assumindo que a coluna de horas é a coluna de índice 5
          tempos = [timedelta(hours=int(h[:2]), minutes=int(h[3:5]), seconds=int(h[6:8])) for h in char_time_list]
          # Somar todos os tempos
          soma_total = sum(tempos, timedelta())
          # Calcular a média
          media = soma_total / len(tempos)
          # Exibir a média no formato "horas e minutos"
          horas_media, segundos_media = divmod(media.seconds, 3600)
          minutos_media = segundos_media // 60
          char_hour_avg = horas_media
          char_minutes_avg = minutos_media
          for char_time in char_time_list:
            time_parts = char_time.split(":")
            hours = int(time_parts[0])
            minutes = int(time_parts[1])
            seconds = int(time_parts[2])
            
            total_seconds = hours * 3600 + minutes * 60 + seconds
            total_hours += total_seconds / 3600
            total_hours = round(total_hours)
          avg_exp_h = int(total_char_change_exp_h/total_hours)
          avg_exp_h = "{:,}".format(avg_exp_h)
          query_status: True
      else:
        query_status = False

  except Exception as e:
    print(e)
    query_status = False

  try:
    with connections['tibia_meta'].cursor() as cursor:    
      cursor.execute(f"SELECT char_level, char_killers_name, char_date, char_reason FROM tibia_stats.char_deaths where char_name= '{character}' ")
      deaths=cursor.fetchall()
      
      
  except Exception as e:
    print(e)
    
  try:
    with connections['tibia_meta'].cursor() as cursor:  
      cursor.execute(f"SELECT char_highscore, char_ref_date, char_level FROM tibia_stats.char_highscore_date where char_name= '{character}' order by char_ref_date desc limit 1;")
      highscore=cursor.fetchall()
      highscore_value = highscore[0][0]
      highscore_value = "{:,}".format(highscore_value)
      highscore_date = highscore[0][1]
      highscore_date = highscore_date.strftime("%d/%m/%Y")
      highscore_level = highscore[0][2]

  except Exception as e:
    print(e)
  
  try:
    with connections['tibia_meta'].cursor() as cursor:  
      cursor.execute(f"select * from (SELECT char_event_newlevel, convert(char_event_date, date) as char_event_date FROM tibia_stats.char_level_events where char_event_name = '{char_name}' order by char_event_date desc limit 30)a order by a.char_event_date asc")
      level_event = cursor.fetchall()
      level_hist = [row[0]  for row in level_event]
      date_hist = [row[1]  for row in level_event]
      pairs = list(zip(level_hist, date_hist))
  except Exception as e:
    print(e)
  #Monta Grafico
  option = {
  "title": {
    "text": "Experience in the last 30 days"
  },
  "dataZoom": [
    {
      "type": "inside",
        "trigger": "axis",
    }
  ],
  "xAxis": {
    "type": "category",
    "boundaryGap": "false",
    "data": char_info_ref_list
  },
  "yAxis": {
    "type": "value"
  },
  "series": [
    {
      "data": char_exp_change_list,
      "type": "line",
      "smooth": "true",
      "label": {
        "show": "true",
        "position": 'top',
        "textStyle":{
            "color": '#fff', 
            "fontSize": "10", 
            "fontStyle": "italic",
            "fontWeight": "bold"
        }
      },
      "areaStyle": {
        "color": "#0f0"
      },
      "itemStyle": {
        "color": "#00C853"
      }
    }
  ]
}
  print(api_status, query_status)
  if api_status == True and query_status == True:
    context = {
          'data': data,
          'link': link,
          'online': online,
          'objects_list': rows,
          'columns_list': columns,
          'hitpoints': hitpoints,
          'mana': mana,
          'cap': cap,
          'min_level': min_level,
          'max_level': max_level,
          'total_char_change_exp': total_char_change_exp,
          'char_exp_change_avg': char_exp_change_avg,
          'char_hour_avg': int(char_hour_avg),
          'char_minutes_avg': int(char_minutes_avg),
          'total_hours': total_hours,
          'highscore_value': highscore_value,
          'highscore_date': highscore_date,
          'highscore_level': highscore_level,
          'avg_exp_h': avg_exp_h,
          'deaths': deaths,
          'graph': json.dumps(option),
          'pairs': pairs
      }
    try:
      char_name = char_name.replace("'","''")
      with connections['tibia_meta'].cursor() as cursor:
        cursor.execute(f"INSERT INTO tibia_stats.char_search_hist(char_name, char_date, char_ip)VALUES('{char_name}', current_timestamp(), '{ip_address}');")
    except Exception:
      print('Falha no insert')
    return render(request, 'tibiameta/characterinfo.html', context)
  
  elif api_status != True and query_status == True:
    context = {
    'objects_list': rows,
    'link': link,
    'columns_list': columns,      
    'total_char_change_exp': total_char_change_exp,
    'total_hours': total_hours,
    'graph': json.dumps(option)
    }
    try:
      char_name = char_name.replace("'","''")
      with connections['tibia_meta'].cursor() as cursor:
        cursor.execute(f"INSERT INTO tibia_stats.char_search_hist(char_name, char_date, char_ip)VALUES('{char_name}', current_timestamp(), '{ip_address}');")
    except Exception:
      print('Falha no insert')
    return render(request, 'tibiameta/characterinfo.html', context)
  elif api_status == True and query_status != True:
    context = {
      'data': data,
      'online': online,
      'link': link,
      'hitpoints': hitpoints,
      'mana': mana,
      'cap': cap,
      'min_level': min_level,
      'max_level': max_level,
    }
    try:
      char_name = char_name.replace("'","''")
      with connections['tibia_meta'].cursor() as cursor:
        cursor.execute(f"INSERT INTO tibia_stats.char_search_hist(char_name, char_date, char_ip)VALUES('{char_name}', current_timestamp(), '{ip_address}');")
    except Exception:
      print('Falha no insert')
    return render(request, 'tibiameta/characterinfo.html', context)
  
  elif api_status == False and query_status == False:
    error_message= 'Character Not Found'
    context = {
    'error': error_message
    }
    try:
      char_name = char_name.replace("'","''")
      with connections['tibia_meta'].cursor() as cursor:
        cursor.execute(f"INSERT INTO tibia_stats.char_search_hist(char_name, char_date, char_ip)VALUES('{char_name}', current_timestamp(), '{ip_address}');")
    except Exception:
      print('Falha no insert')
    return render(request, 'tibiameta/index.html', context)



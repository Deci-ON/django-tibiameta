from django.shortcuts import render,  HttpResponse, redirect
from .forms import playersForm, ServerSearchForm
import requests
from django.templatetags.static import static
from django.db import connections
from datetime import timedelta
import tenacity
import math 
from operator import itemgetter

def get_img_path(vocation, sex):
    vocation_sex_map = {
        ('Royal Paladin', 'male'): 'Outfit_Hunter_Male_Addon_3.gif',
        ('Royal Paladin', 'female'): 'Outfit_Hunter_Female_Addon_3.gif',
        ('Paladin', 'male'): 'Outfit_Hunter_Male_Addon_3.gif',
        ('Paladin', 'female'): 'Outfit_Hunter_Female_Addon_3.gif',
        ('Elite Knight', 'male'): 'Outfit_Knight_Male_Addon_3.gif',
        ('Elite Knight', 'female'): 'Outfit_Knight_Female_Addon_3.gif',
        ('Knight', 'male'): 'Outfit_Knight_Male_Addon_3.gif',
        ('Knight', 'female'): 'Outfit_Knight_Female_Addon_3.gif',
        ('Elder Druid', 'male'): 'Outfit_Druid_Male_Addon_3.gif',
        ('Elder Druid', 'female'): 'Outfit_Druid_Female_Addon_3.gif',
        ('Druid', 'male'): 'Outfit_Druid_Male_Addon_3.gif',
        ('Druid', 'female'): 'Outfit_Druid_Female_Addon_3.gif',
        ('Master Sorcerer', 'male'): 'Outfit_Sorcerer_Male_Addon_3.gif',
        ('Master Sorcerer', 'female'): 'Outfit_Sorcerer_Female_Addon_3.gif',
        ('Sorcerer', 'male'): 'Outfit_Sorcerer_Male_Addon_3.gif',
        ('Sorcerer', 'female'): 'Outfit_Sorcerer_Female_Addon_3.gif',
        ('None', 'male'): 'Outfit_Citizen_Male_Addon_3.gif',
        ('None', 'female'): 'Outfit_Citizen_Female_Addon_3.gif',
    }
    return static(f"images/vocations/{vocation_sex_map.get((vocation, sex), 'default_image.gif')}")



def process_vocs(onlines, minl, maxl):

    min_level = minl
    max_level = maxl

    online_players = sorted(onlines, key=itemgetter('level'), reverse=True)

    premium_list = []
    free_list = []

    vocations = {
        vocation: {
            'players': [{
                'name': player['name'],
                'level': player['level']
            } for player in online_players if player['vocation'] == vocation
                    and min_level <= player['level'] <= max_level],
            'count': 0  # Inicializando o contador de jogadores
        }
        for vocation in set(player['vocation'] for player in online_players)
    }

    # Salvando jogadores em listas diferentes de acordo com a vocação e se o jogador é premium ou não
    for vocation, players in vocations.items():
        # Atualizando o contador de jogadores para a vocação atual
        count = vocations[vocation]['count'] = len(players['players'])
        if vocation in ('Elite Knight', 'Royal Paladin', 'Master Sorcerer',
                        'Elder Druid') and len(players['players']) > 0:
            premium_list.append({'vocation': vocation, 'players': players['players'], 'count': count})
        elif len(players['players']) > 0:
            free_list.append({'vocation': vocation, 'players': players['players'], 'count': count})
            
    return premium_list, free_list

def request_world(request, data, minl, maxl):
    try:
        response = requests.get(data, timeout=30)
        if response.status_code == 200:
            res = response.json()
            online_players = res['world']['online_players']
            request.session['online_players'] = res['world']['online_players']
            min_level = minl
            max_level = maxl
            process = process_vocs(online_players, min_level, max_level)
            return process
    except Exception as e:
        print(e)
        raise


#@tenacity.retry(wait=tenacity.wait_fixed(10), stop=tenacity.stop_after_attempt(5))
def request_info(data):
    try:
        response = requests.get(data, timeout=30)
        if response.status_code == 200:
            res = response.json()
            if 'character' in data:
                char_name = res['character']['character'].get('name')
                if char_name !='':
                    level = res['character']['character']['level']
                    vocation = res['character']['character']['vocation']
                    sex = res['character']['character']['sex']
                    img = get_img_path(vocation, sex)
                    world = res['character']['character']['world']
                    return level, vocation, char_name, img, world
    except Exception as e:
        print(e)
        raise

def calc_level_range(request):
    if isinstance(request, int) == True:
        max_level = (request/2)
        max_level = math.ceil(max_level*3)
        min_level = (request/3)
        min_level = math.ceil(min_level*2)
        return min_level, max_level
    else:
        level = request.GET.get('level')
        try:
            level = int(level)
            max_level = (level/2)
            max_level = math.ceil(max_level*3)
            min_level = (level/3)
            min_level = math.ceil(min_level*2)
            online_players = request.session.get('online_players')
            request_players_list = process_vocs(online_players, min_level, max_level)
            context = {
                    'min_level': min_level,
                    'max_level': max_level,
                    'request_players_list': request_players_list
                }
            print(context)
            return render(request, 'tibiameta/finder_result.html', context)
        except Exception as e:
            # print(e)
            return HttpResponse({'error': 'Invalid level value. Please provide an integer.'}, status=400)
        
        
def partyforms(request):
    if request.method == 'POST':
        form = playersForm(request.POST)
        worlds = ServerSearchForm(request.POST)

        if form.is_valid() and worlds.is_valid():
            # Processar os dados dos formulários
            level_value = form.cleaned_data['level']  # Obtém o valor do campo 'level' do formulário 'playersForm'
    else:
        form = playersForm()
        worlds = ServerSearchForm()

    return render(request, 'tibiameta/partyfinder.html', {'form': form, 'worlds': worlds})


#s@tenacity.retry(wait=tenacity.wait_fixed(60), stop=tenacity.stop_after_attempt(5))
def htmx_search_player(request):
    player1 = request.POST.get('player1')
    if player1 == '':
        return HttpResponse('<span style="color:red";> Character name should not be empty! <span>')
    if len(player1) > 1:
        char_info = f'https://api.tibiadata.com/v4/character/{player1}'
        request_player = request_info(char_info)
        level = request_player[0]
        vocation = request_player[1]
        char_name = request_player[2]
        img = request_player[3]
        world = request_player[4]
        level_range = calc_level_range(level)
        min_level = level_range[0]
        max_level = level_range[1]
        players_list = f"https://api.tibiadata.com/v4/world/{world}"
        request_players_list = request_world(request,players_list, min_level, max_level)
        context = {
            'char_name': char_name,
            'level': level,
            'vocation':vocation,
            'world': world,
            'img': img,
            'min_level': min_level,
            'max_level': max_level,
            'request_players_list': request_players_list
        }
        
        return render(request, 'tibiameta/finder_result.html', context)
        
def htmx_search_world(request):
    world = request.POST.get('server_name')
    level_field = request.POST.get('level_field')
    level_range = calc_level_range(int(level_field))
    players_list = f"https://api.tibiadata.com/v4/world/{world}"
    min_level = level_range[0]
    max_level = level_range[1]
    request_players_list = request_world(request,players_list, min_level, max_level)
    context = {
            'min_level': min_level,
            'max_level': max_level,
            'request_players_list': request_players_list
        }
        
    return render(request, 'tibiameta/finder_result.html', context)
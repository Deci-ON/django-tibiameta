from django.shortcuts import render
import math
from datetime import timedelta
from .forms import Calcform
from .models import Skills
from django.http import JsonResponse, HttpResponse
import json

skill = {
"1": 1600,
"2": 50,
"3": 25,
#"shielding": 100,
#"fishing": 20
}

# skill_choices = [(key, key) for key in skill.keys()]

constants_vocs = {
#   "Rookier": {
    # "Magic Level": 3.0,
    # "Axe/Sword/Club": 2.0,
    # "fist": 1.5,
    # "distance": 2.0,
    # "shielding": 1.5,
    # "fishing": 1.1
#   },
"Knight": {
    "Magic Level": 3.0,
    "Axe/Club/Sword": 1.1,
    "fist": 1.1,
    "distance": 1.4,
    "Shielding": 1.1,
    "fishing": 1.1
},
"Paladin": {
    "Magic Level": 1.4,
    "Axe/Club/Sword": 1.2,
    "fist": 1.2,
    "Distance": 1.1,
    "Shielding": 1.1,
    "fishing": 1.1
},
"Sorcerer": {
    "Magic Level": 1.1,
    "Axe/Club/Sword": 2.0,
    "fist": 1.5,
    "distance": 2.0,
    "Shielding": 1.5,
    "fishing": 1.1
},
"Druid": {
    "Magic Level": 1.1,
    "Axe/Club/Sword": 1.8,
    "fist": 1.5,
    "distance": 1.8,
    "Shielding": 1.5,
    "fishing": 1.1
}
}


weapon_type = {
"Lasting Weapon": {
    "Charges": 14400,
    "Using Time": 480,  #minutes
    "Gold": 7560000,
    "Tibia Coins": 720
},
"Durable Weapon": {
    "Charges": 1800,
    "Using Time": 60,  #minutes
    "Gold": 945000,
    "Tibia Coins": 90
},
"Exercise Weapon": {
    "Charges": 500,
    "Using Time": 16.40,  #minutes
    "Gold": 262500,
    "Tibia Coins": 25
},
"Training Weapon": {
    "Charges": 50,
    "Using Time": 1.40,  #minutes
    "Gold": 0,
    "Tibia Coins": 0
}
}

loyalt = {  #LOYALT?
"0": 1,
"1": 1.05,
"2": 1.10,
"3": 1.15,
"4": 1.20,
"5": 1.25,
"6": 1.30,
"7": 1.35,
"8": 1.40,
"9": 1.45,
"10": 1.50
}


def load_skills(request):
    vocations_id = request.GET.get("vocation")
    skills = Skills.objects.filter(vocations_id=vocations_id)
    return render(request, "tibiameta/skill_options.html", {"skills": skills})

def exercisecalculator(request):
    form = Calcform()
    return render(request, "tibiameta/exercisecalculator.html", context={'form': form})

def exerciseresult(request):
    context = {}
    context['form'] = Calcform()
    calculated_results = []
    melee = 7.22890777587891  #CONSTANT
    bow = 3.61445388793946  #CONSTANT
    wand = 600  #CONSTANT
    shielding_ek_rp = 16.59936523
    shielding_mages = 14.6618095362
    others = 1  #CONSTANT

    a = None  #Constant Melee 50 Magic Level 1600 Distance Fighting	25
    b = None  #Choose desired skill in constant vocs
    c = None  #IF Magic level 0 else 10
    # c_skill = 122  #CHOOSE CURRENT SKILL
    # d_skill = 123 #CHOOSE DESIRED SKILL
    # c_percent = 40  #CHOOSE CURRENT PERCENT
    t_skill = None
    double_xp = 1 #2 = DOUBLE?
    dummy = 1 #1.1 = DUMMY?

    if request.method == "POST":
        raw_data = request.body.decode('utf-8')
        # Converter o JSON bruto para um dicionário Python
        json_data = json.loads(raw_data)
        selected_vocation = int(json_data['vocation'])
        selected_skill = int(json_data['skills'])
        double_event_checked = json_data['double_event']
        private_dummy_checked = json_data['private_dummy']
        if double_event_checked:
        # O checkbox "Double Event" foi marcado
            double_xp = 2
        else:
            # O checkbox "Double Event" não foi marcado
            double_xp = 1
        
        if private_dummy_checked:
        # O checkbox "Double Event" foi marcado
            dummy = 1.1
        else:
            # O checkbox "Double Event" não foi marcado
            dummy = 1
                        
        if selected_vocation == 1: #Knight
            if selected_skill == 2: #Magic Level
                a = 1600
                b = constants_vocs["Knight"]["Magic Level"]
                t_skill = wand
                c = 0
                selected_weapon = "Magic Level"
            elif selected_skill == 1:
                a = 50
                b = constants_vocs["Knight"]["Axe/Club/Sword"]
                t_skill = melee
                c = 10
                selected_weapon = "Axe/Club/Sword"
            elif selected_skill == 6:
                a = 100
                b = constants_vocs["Knight"]["Shielding"]
                t_skill = shielding_ek_rp
                c = 10
                selected_weapon = "Shielding"
        elif selected_vocation == 2:
            if selected_skill == 4: #Magic Level
                a = 1600
                b = constants_vocs["Paladin"]["Magic Level"]
                t_skill = wand
                c = 0
                selected_weapon = "Magic Level"
            elif selected_skill == 3:
                a = 25
                b = constants_vocs["Paladin"]["Distance"]
                t_skill = bow
                c = 10
                selected_weapon = "Distance"
            elif selected_skill == 7:
                a = 100
                b = constants_vocs["Paladin"]["Shielding"]
                t_skill = shielding_ek_rp
                c = 10
                selected_weapon = "Shielding"
        elif selected_vocation == 3:
            if selected_skill == 5: #Magic Level
                a = 1600
                b = constants_vocs["Sorcerer"]["Magic Level"]
                t_skill = wand
                c = 0
                selected_weapon = "Magic Level"
            elif selected_skill == 8:
                a = 100
                b = constants_vocs["Sorcerer"]["Shielding"]
                t_skill = shielding_mages
                c = 10
                selected_weapon = "Shielding"
                                        
        selected_loyalty = (json_data['loyalty'])
        # print('loyalty', loyalt)
        selected_loyalty = loyalt[selected_loyalty]
        c_skill = int(json_data['current_skill'])
        d_skill = int(json_data['desired_skill'])
        c_percent = int(json_data['percent_skill'])
        # Your parameter values (a, b, c_skill, etc.) here
        calculated_results = []  # Initialize the list to store results
        
        tpc = a * ((b**(c_skill - c)) - 1) / (b - 1)
        tpd = a * (((b**(d_skill - c)) - 1) / (b - 1))
        tt = tpd - tpc
        p = a * (b**(c_skill - c))
        pp = p * (1 - (c_percent / 100))
        tc = (tt - pp)
        charges = tc / ((t_skill * double_xp * dummy) * selected_loyalty)
        
        for weapon_name, weapon_details in weapon_type.items():
            wp_result = {}  # Initialize the dictionary for each weapon type
            wp_result["weapon_type"] = weapon_name
            wp_result["d_skill"] = d_skill
            for key, value in weapon_details.items():
                if key == "Charges":
                    wp_result["weapons_needed"] = math.ceil(charges / value)
                elif key == "Using Time":
                    using_time = value
                    calculated_time_minutes = wp_result["weapons_needed"] * using_time
                    try:
                        duracao = timedelta(minutes=calculated_time_minutes)
                        wp_result["dias"] = duracao.days
                        wp_result["horas"] = duracao.seconds // 3600
                        wp_result["minutos"] = (duracao.seconds % 3600) // 60
                        wp_result["segundos"] = (duracao.seconds % 3600) % 60
                    except ValueError:
                        string = str(calculated_time_minutes)  # converte o valor em uma string
                        primeiros_8 = string[:5]  # obtém os 5 primeiros caracteres da string
                        calculated_time_minutes = int(float(primeiros_8) * 10**5)  # Converte para float, multiplica e converte para int
                        duracao = timedelta(minutes=calculated_time_minutes)
                        wp_result["dias"] = duracao.days
                        wp_result["horas"] = duracao.seconds // 3600
                        wp_result["minutos"] = (duracao.seconds % 3600) // 60
                        wp_result["segundos"] = (duracao.seconds % 3600) % 60
                    except OverflowError:
                        string = str(calculated_time_minutes) # converte o valor em uma string
                        primeiros_8 = string[:5] # obtém os 5 primeiros caracteres da string
                        calculated_time_minutes = int(float(primeiros_8) * 10**5)  # Converte para float, multiplica e converte para int
                        duracao = timedelta(minutes=calculated_time_minutes)
                        wp_result["dias"] = duracao.days
                        wp_result["horas"] = duracao.seconds // 3600
                        wp_result["minutos"] = (duracao.seconds % 3600) // 60
                        wp_result["segundos"] = (duracao.seconds % 3600) % 60

                elif key == "Gold":
                    wp_result["gold_spend"] = (wp_result["weapons_needed"] * value) / 1000000
                elif key == "Tibia Coins":
                    wp_result["coins_spend"] = wp_result["weapons_needed"] * value
                wp_result["selected_skill"] = selected_weapon.replace('/','')
            calculated_results.append(wp_result)  # Append the result for this weapon type
            response_data = {
            "message": "Processamento concluído com sucesso!",
            "data": calculated_results
        }
        return JsonResponse(response_data)
        
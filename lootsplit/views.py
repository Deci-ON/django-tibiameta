from django.shortcuts import render
from django.http import HttpResponse
from django.db import connections
from django.http import JsonResponse
from .forms import TextInputForm
import requests
import json
import re
import time
import math
from pprint import pprint
from collections import deque
payments = deque()

# Create your views here.
def loot_split(request):
	payments = []
	payment_details = []
	payment_transfer = []
	player_data = {}
	players = {}

	if request.method == 'POST':
		form = TextInputForm(request.POST)
		if form.is_valid():
			text_input = form.cleaned_data['text_input']
			try:
				data_string = re.sub(r"\s+", " ", text_input)
				data_string = " ".join(data_string.split())
				session_pattern = r"Session data: From (?P<start_date>\d{4}-\d{2}-\d{2}), (?P<start_time>\d{2}:\d{2}:\d{2}) to (?P<end_date>\d{4}-\d{2}-\d{2}), (?P<end_time>\d{2}:\d{2}:\d{2}) Session: (?P<session_time>[\d:]+)h Loot Type: (?P<loot_type>\w+) Loot: (?P<loot>[\d,]+) Supplies: (?P<supplies>[\d,]+) Balance: (?P<balance>[\d,-]+)"
				session_match = re.search(session_pattern, data_string)
				session_data = {
				"start_date": session_match.group("start_date"),
				"start_time": session_match.group("start_time"),
				"end_date": session_match.group("end_date"),
				"end_time": session_match.group("end_time"),
				"session_time": session_match.group("session_time"),
				"loot_type": session_match.group("loot_type"),
				"loot": session_match.group("loot"),
				"supplies": session_match.group("supplies"),
				"balance": session_match.group("balance")
				}
				session_time = session_data.get('session_time')
				partes = session_time.split(':')
				horas_em_minutos = int(partes[0]) * 60 if len(partes) > 1 else 0
				minutos = int(partes[1]) if len(partes) > 1 else int(partes[0])
				formated_session = (horas_em_minutos + minutos) * 60
				player_pattern = r"(?P<name>[A-Za-z\s'’\-]+?)(?: \([\w\s]+\))? Loot: (?P<loot>[\d,]+) Supplies: (?P<supplies>[\d,]+) Balance: (?P<balance>[\d,-]+) Damage: (?P<damage>[\d,]+) Healing: (?P<healing>[\d,]+)"
				player_matches = re.findall(player_pattern, data_string)
				players = {}
	
				for match in player_matches:
					name = match[0].strip()
					loot = int(match[1].replace(",", ""))
					supplies = int(match[2].replace(",", ""))
					balance = int(match[3].replace(",", ""))
					damage = int(match[4].replace(",", ""))
					healing = int(match[5].replace(",", ""))
					difference = 0
					players[name] = {
						"loot": loot,
						"supplies": supplies,
						"balance": balance,
						"damage": damage,
						"healing": healing,
						"difference": difference
					}
				player_list = list(players.keys())
				balance_total = sum(player["balance"] for player in players.values())
				num_people = len(players)
				balance_per_person = balance_total / num_people

				# Cálculo da diferença de cada jogador
				for player in players:
					players[player]["difference"] = balance_per_person - players[player]["balance"]

				# Criação de uma lista para armazenar os pagamentos
				payments = []

				# Verificação de quem deve pagar ou receber
				for payer in players:
					for receiver in players:
						# Se o pagador tem uma diferença negativa e o recebedor tem uma diferença positiva
						if players[payer]["difference"] < 0 and players[receiver]["difference"] > 0:
							# O valor do pagamento é a diferença do recebedor (em módulo)
							payment_value = abs(players[receiver]["difference"])
							# Adiciona o pagamento na lista
							payments.append((payer, receiver, payment_value))
							# Atualiza a diferença dos jogadores envolvidos
							players[payer]["difference"] += payment_value
							players[receiver]["difference"] -= payment_value
    
				payment_list = []
				for payment in payments:
					payer = payment[0]
					payee = payment[1]
					amount = int(payment[2])
					payment_details= f'{payer} have to pay {amount} to {payee}'
					payment_transfer= f'Transfer {amount} to {payee}'
					payment_data = {
						'payer': payer,
						'payee': payee,
						'amount': amount,
						'payment_details': payment_details,
						'payment_transfer': payment_transfer,
						'players_data': players
					}
					payment_list.append(payment_data)
				################# Setor Graficos ######################
				# Criar um dicionário para armazenar os dados de damage, healing e supplies de cada jogador
				players_data = {}
				for player_name, player_data in players.items():
					players_data[player_name] = {
					'damage': player_data['damage'],
					'damage_minute': int(player_data.get('damage') / formated_session),
					'percentage_damage': 0,  # Vamos calcular a porcentagem posteriormente
					'supplies': player_data['supplies'],
					'supplies_minute': int(player_data.get('supplies') / formated_session),
					'percentage_supplies': 0,  # Vamos calcular a porcentagem posteriormente
					'healing': player_data['healing'],
					'healing_minute': int(player_data.get('healing') / formated_session),
					'percentage_healing': 0,  # Vamos calcular a porcentagem posteriormente
					}


				# Calcular o total de dano, supplies e healing de todos os jogadores
				total_damage = sum(player['damage'] for player in players.values())
				total_supplies = sum(player['supplies'] for player in players.values())
				total_healing = sum(player['healing'] for player in players.values())
				
				# Calcular a porcentagem de dano, supplies e healing de cada jogador em relação ao total
				for player_name, player_data in players_data.items():
					player_data['percentage_damage'] = (player_data['damage'] / total_damage) * 100
					player_data['percentage_supplies'] = (player_data['supplies'] / total_supplies) * 100
					player_data['percentage_healing'] = (player_data['healing'] / total_healing) * 100
				
				damage_list = [players_data[player]['damage_minute'] for player in players_data]
				supplies_list = [players_data[player]['supplies_minute'] for player in players_data]
				healing_list = [players_data[player]['healing_minute'] for player in players_data]
    
				# Criar o contexto com a lista de pagamentos e o dicionário de dados dos jogadores
				context = {
				'payments': payment_list,
				'players_data': players_data,
				'player_list': json.dumps(player_list),
				'damage_list': json.dumps(damage_list),
    			'supplies_list': json.dumps(supplies_list),
				'healing_list': json.dumps(healing_list),
				}
				form = TextInputForm()
				with connections['tibia_meta'].cursor() as cursor:
					try:
						cursor.execute(f"select raw from tibia_stats.lootsplit_data ld where raw = '{data_string}'")
						existing_record = cursor.fetchone()
						if existing_record is None:
							# Montar a consulta SQL de inserção
							insert_query = """
								INSERT INTO lootsplit_data
								(start_date, start_time, end_date, end_time, session_time, loot_type, loot, supplies, balance, raw)
								VALUES
								(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
							"""
							values = (
								session_data["start_date"],
								session_data["start_time"],
								session_data["end_date"],
								session_data["end_time"],
								session_data["session_time"],
								session_data["loot_type"],
								session_data["loot"].replace(",", ""),  # Remova vírgulas para valores numéricos
								session_data["supplies"].replace(",", ""),  # Remova vírgulas para valores numéricos
								session_data["balance"].replace(",", ""),  # Remova vírgulas para valores numéricos
								data_string
							)

							# Executar a consulta SQL de inserção
							cursor.execute(insert_query, values)
							cursor.execute("SELECT LAST_INSERT_ID()")
							last_inserted_id = cursor.fetchone()[0]
							insert_hunt_query = """
							INSERT INTO lootsplit_hunt
							(lootsplit_data_id, player_name, damage, damage_minute, supplies, supplies_minute, healing, healing_minute)
							VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"""
							for player_name, player_data in players_data.items():
								values = (
									last_inserted_id,
									player_name,
									player_data['damage'],
									player_data['damage_minute'],
									player_data['supplies'],
									player_data['supplies_minute'],
									player_data['healing'],
									player_data['healing_minute'],
								)
								cursor.execute(insert_hunt_query, values)
		
							for payment_data in payment_list:
								payer = payment_data['payer']
								payee = payment_data['payee']
								amount = payment_data['amount']
								payment_details = payment_data['payment_details']
								payment_transfer = payment_data['payment_transfer']  # Defina a variável payment_transfer

								# Inserir os dados na tabela lootsplit_payments
								insert_payment_query = """
									INSERT INTO lootsplit_payments
									(lootsplit_data_id, payer, payee, amount, payment_details, payment_transfer)
									VALUES(%s, %s, %s, %s, %s, %s)
								"""
								values = (last_inserted_id, payer, payee, amount, payment_details, payment_transfer)
								cursor.execute(insert_payment_query, values)
								cursor.close()
       
					except Exception as e:
						print(e)
				return render(request, 'tibiameta/lootsplit.html', {'form': form, **context})

			except AttributeError:
				error = {
				'error': 'Error, check your Part Hunt.'
			}
				return render(request, 'tibiameta/lootsplit.html', {'form': form, 'error': error})
		else:
			error = {
				'error': 'Error, check your Part Hunt.'
			}
			return render(request, 'tibiameta/lootsplit.html', {'form': form, 'error': error})

	else:
		form = TextInputForm()
		return render(request, 'tibiameta/lootsplit.html', {'form': form})
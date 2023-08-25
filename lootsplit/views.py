from django.shortcuts import render
from django.http import HttpResponse
from django.db import connections
from django.http import JsonResponse
from .forms import TextInputForm
import requests
import json
import re
import time

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
        try:
          text_input = form.cleaned_data['text_input']
          data_string = re.sub(r"\s+", " ", text_input)
          data_string = " ".join(data_string.split())
          session_pattern = r"Session data: From (?P<start_date>\d{4}-\d{2}-\d{2}), (?P<start_time>\d{2}:\d{2}:\d{2}) to (?P<end_date>\d{4}-\d{2}-\d{2}), (?P<end_time>\d{2}:\d{2}:\d{2}) Session: (?P<session_time>[\d:]+)h Loot Type: (?P<loot_type>\w+)"
          session_match = re.search(session_pattern, data_string)
          session_data = {
          "start_date": session_match.group("start_date"),
          "start_time": session_match.group("start_time"),
          "end_date": session_match.group("end_date"),
          "end_time": session_match.group("end_time"),
          "session_time": session_match.group("session_time"),
          "loot_type": session_match.group("loot_type")
          }
          player_pattern = r"(?P<name>[A-Za-z\s]+?)(?: \([\w\s]+\))? Loot: (?P<loot>[\d,]+) Supplies: (?P<supplies>[\d,]+) Balance: (?P<balance>[\d,-]+) Damage: (?P<damage>[\d,]+) Healing: (?P<healing>[\d,]+)"
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
            # player_data[name] = {
            #     "damage": damage,
            #     "healing": healing,
            #     "supplies": supplies
            # }

          loot_total = sum(player["loot"] for player in players.values())
          supplies_total = sum(player["supplies"] for player in players.values())
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
                      'payment_details': payment_details,
                      'payment_transfer': payment_transfer,
                      'players_data': players
                  }
                  payment_list.append(payment_data)
        # Criar um dicionário para armazenar os dados de damage, healing e supplies de cada jogador
          players_data = {}
          for player_name, player_data in players.items():
            players_data[player_name] = {
            'damage': player_data['damage'],
            'percentage_damage': 0,  # Vamos calcular a porcentagem posteriormente
            'supplies': player_data['supplies'],
            'percentage_supplies': 0,  # Vamos calcular a porcentagem posteriormente
            'healing': player_data['healing'],
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

          # Criar o contexto com a lista de pagamentos e o dicionário de dados dos jogadores
          context = {
          'payments': payment_list,
          'players_data': players_data
          }
          form = TextInputForm()
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
# -*- coding: utf-8 -*-
"""Evento 10 — O Frio Chega (Inverno).

Cada opcao tem: councilor, action, cost {mel, operarias, relacao},
effects (deltas nos 5 eixos de Harmonia), affinity, puzzle.
"""

EVENT = {'id': 10,
 'season': 'Inverno',
 'title': 'O Frio Chega',
 'context': 'As primeiras geadas testam tudo o que foi construido no Outono. As '
            'reservas acumuladas -- ou a falta delas -- decidem o tom do inverno.',
 'options': [{'councilor': 'Melina',
              'action': 'Consumir as reservas de forma controlada, priorizando a '
                        'producao minima',
              'cost': {'mel': -38, 'operarias': 0, 'relacao': -4},
              'effects': {'producao': 6},
              'affinity': {'self': 2, 'others': -1},
              'puzzle': 'Rastro de Pólen'},
             {'councilor': 'Flora',
              'action': 'Manter parte da colonia ativa cuidando de plantas resistentes '
                        'ao frio',
              'cost': {'mel': -10, 'operarias': 0, 'relacao': 2},
              'effects': {'biodiversidade': 6},
              'affinity': {'self': 2, 'others': -1},
              'puzzle': 'Sob as Folhas'},
             {'councilor': 'Nectar',
              'action': 'Testar um metodo de aquecimento coletivo mais eficiente',
              'cost': {'mel': -16, 'operarias': 0, 'relacao': -1},
              'effects': {'inovacao': 6},
              'extra': 'Reduz perdas por frio no futuro.',
              'affinity': {'self': 2, 'others': -1},
              'puzzle': 'Rota de Voo'},
             {'councilor': 'Aurora',
              'action': 'Formar um circulo de aquecimento com todas as operarias '
                        'disponiveis',
              'cost': {'mel': -5, 'operarias': 0, 'relacao': 4},
              'effects': {'cooperacao': 6, 'populacao': 3},
              'affinity': {'self': 2, 'others': -1},
              'puzzle': 'Antes da Poda'}],
 'consequence': 'O saldo de Mel acumulado nos eventos 7 e 8 e o que realmente e gasto '
                'aqui -- colonias com pouca reserva sofrem perda automatica de '
                'Populacao, tornando visivel o resultado das decisoes do Outono.'}

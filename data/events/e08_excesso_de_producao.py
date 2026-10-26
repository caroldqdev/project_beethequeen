# -*- coding: utf-8 -*-
"""Evento 8 — Excesso de Producao (Outono).

Cada opcao tem: councilor, action, cost {mel, operarias, relacao},
effects (deltas nos 5 eixos de Harmonia), affinity, puzzle.
"""

EVENT = {'id': 8,
 'season': 'Outono',
 'title': 'Excesso de Producao',
 'context': 'A colheita do ano rendeu mais mel do que a estrutura atual comporta -- '
            'sem espaco, parte dele sera perdido.',
 'options': [{'councilor': 'Melina',
              'action': 'Expandir os favos as pressas para nao perder nada',
              'cost': {'mel': -22, 'operarias': 0, 'relacao': -2},
              'effects': {'producao': 8},
              'affinity': {'self': 2, 'others': -1},
              'puzzle': 'Rastro de Pólen'},
             {'councilor': 'Nectar',
              'action': 'Testar um novo formato hexagonal mais eficiente de '
                        'armazenamento',
              'cost': {'mel': -18, 'operarias': 0, 'relacao': -1},
              'effects': {'inovacao': 8, 'producao': 5},
              'affinity': {'self': 2, 'others': -1},
              'puzzle': 'Rota de Voo'},
             {'councilor': 'Flora',
              'action': 'Doar o excedente para polinizar areas que precisam de '
                        'recuperacao',
              'cost': {'mel': -6, 'operarias': 0, 'relacao': 3},
              'effects': {'biodiversidade': 8, 'producao': -4},
              'affinity': {'self': 2, 'others': -1},
              'puzzle': 'Sob as Folhas'},
             {'councilor': 'Aurora',
              'action': 'Repartir o excedente com colmeias vizinhas em dificuldade',
              'cost': {'mel': -6, 'operarias': 0, 'relacao': 4},
              'effects': {'cooperacao': 8, 'producao': -4},
              'affinity': {'self': 2, 'others': -1},
              'puzzle': 'Antes da Poda'}],
 'consequence': 'A capacidade de estoque construida aqui (Melina/Nectar) reduz o risco '
                'de fome no Inverno; doar ou repartir (Flora/Aurora) reduz a reserva '
                'mas fortalece bonus de biodiversidade ou cooperacao mais adiante.'}

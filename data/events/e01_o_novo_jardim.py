# -*- coding: utf-8 -*-
"""Evento 1 — O Novo Jardim (Primavera).

Cada opcao tem: councilor, action, cost {mel, operarias, relacao},
effects (deltas nos 5 eixos de Harmonia), affinity, puzzle.
"""

EVENT = {'id': 1,
 'season': 'Primavera',
 'title': 'O Novo Jardim',
 'context': 'Exploradoras encontram um jardim particular ainda não polinizado por '
            'ninguém, mas outros insetos também o notaram.',
 'options': [{'councilor': 'Flora',
              'action': 'Mapear com cuidado, respeitando as espécies nativas antes de '
                        'polinizar',
              'cost': {'mel': -15, 'operarias': 0, 'relacao': 3},
              'effects': {'biodiversidade': 8, 'producao': 3},
              'affinity': {'self': 2, 'others': -1},
              'puzzle': 'Sob as Folhas'},
             {'councilor': 'Melina',
              'action': 'Polinizar tudo!! Antes que outra espécie tome o jardim',
              'cost': {'mel': -5, 'operarias': -12, 'relacao': -4},
              'effects': {'producao': 8, 'biodiversidade': -5},
              'affinity': {'self': 2, 'others': -1},
              'puzzle': 'Rastro de Pólen'},
             {'councilor': 'Nectar',
              'action': 'Testar uma rota de voo experimental mais eficiente',
              'cost': {'mel': -22, 'operarias': 0, 'relacao': 0},
              'effects': {'inovacao': 8, 'producao': 4},
              'affinity': {'self': 2, 'others': -1},
              'puzzle': 'Rota de Voo'},
             {'councilor': 'Aurora',
              'action': 'Negociar com o jardineiro humano um plantio em conjunto',
              'cost': {'mel': -5, 'operarias': 0, 'relacao': 5},
              'effects': {'cooperacao': 8},
              'affinity': {'self': 2, 'others': -1},
              'puzzle': 'Antes da Poda'}],
 'consequence': 'O jardim passa a existir permanentemente no mapa \n'
                'A forma como foi ocupado define se ele aparecera depois como aliado '
                '(Aurora/Flora)ou como fonte de conflito com outros polinizadores '
                '(Melina/Nectar).'}

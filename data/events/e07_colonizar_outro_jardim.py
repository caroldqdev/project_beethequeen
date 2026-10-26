# -*- coding: utf-8 -*-
"""Evento 7 — Colonizar Outro Jardim (Outono).

Cada opcao tem: councilor, action, cost {mel, operarias, relacao},
effects (deltas nos 5 eixos de Harmonia), affinity, puzzle.
"""

EVENT = {'id': 7,
 'season': 'Outono',
 'title': 'Colonizar Outro Jardim',
 'context': 'Um jardim vizinho, ainda livre, pode se tornar uma extensao da colonia '
            'antes do inverno.',
 'options': [{'councilor': 'Melina',
              'action': 'Colonizar o jardim para garantir mais uma fonte de reservas',
              'cost': {'mel': -2, 'operarias': -8, 'relacao': -2},
              'effects': {'producao': 8},
              'affinity': {'self': 2, 'others': -1},
              'puzzle': 'Rastro de Pólen'},
             {'councilor': 'Flora',
              'action': 'Colonizar de forma gradual, preservando a vegetacao ja '
                        'existente',
              'cost': {'mel': -10, 'operarias': 0, 'relacao': 2},
              'effects': {'biodiversidade': 8, 'producao': 3},
              'affinity': {'self': 2, 'others': -1},
              'puzzle': 'Sob as Folhas'},
             {'councilor': 'Nectar',
              'action': 'Usar o novo jardim como posto avancado de pesquisa',
              'cost': {'mel': -18, 'operarias': 0, 'relacao': -1},
              'effects': {'inovacao': 8},
              'affinity': {'self': 2, 'others': -1},
              'puzzle': 'Rota de Voo'},
             {'councilor': 'Aurora',
              'action': 'Propor a colonizacao conjunta com outra colmeia amiga',
              'cost': {'mel': -5, 'operarias': 0, 'relacao': 3},
              'effects': {'cooperacao': 8, 'producao': 4},
              'affinity': {'self': 2, 'others': -1},
              'puzzle': 'Antes da Poda'}],
 'consequence': 'O novo territorio passa a contar como fonte de recursos todo inverno '
                '-- sua qualidade (diversa, eficiente ou compartilhada) depende de '
                'como foi colonizado agora.'}

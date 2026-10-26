# -*- coding: utf-8 -*-
"""Evento 11 — Teias na Entrada (Inverno).

Cada opcao tem: councilor, action, cost {mel, operarias, relacao},
effects (deltas nos 5 eixos de Harmonia), affinity, puzzle.
"""

EVENT = {'id': 11,
 'season': 'Inverno',
 'title': 'Teias na Entrada',
 'context': 'Uma aranha construiu teias perto da entrada da colmeia. Operarias '
            'forrageadoras estao presas.',
 'options': [{'councilor': 'Aurora',
              'action': 'Organizar um resgate coletivo, evitando as teias',
              'cost': {'mel': -10, 'operarias': 0, 'relacao': 4},
              'effects': {'cooperacao': 6},
              'extra': 'Salva a maioria das operarias.',
              'affinity': {'self': 2, 'others': -1},
              'puzzle': 'Antes da Poda'},
             {'councilor': 'Melina',
              'action': 'Sacrificar as presas e seguir em frente para nao perder mais '
                        'recursos',
              'cost': {'mel': 0, 'operarias': -10, 'relacao': -5},
              'effects': {'producao': 5, 'populacao': -4},
              'affinity': {'self': 2, 'others': -1},
              'puzzle': None},
             {'councilor': 'Nectar',
              'action': 'Testar uma rota alternativa de entrada que evite a area da '
                        'teia',
              'cost': {'mel': -14, 'operarias': 0, 'relacao': -1},
              'effects': {'inovacao': 6},
              'affinity': {'self': 2, 'others': -1},
              'puzzle': 'Rota de Voo'},
             {'councilor': 'Flora',
              'action': 'Deixar a aranha em paz e replantar arbustos que naturalmente '
                        'a afastem',
              'cost': {'mel': -10, 'operarias': 0, 'relacao': 2},
              'effects': {'biodiversidade': 6},
              'affinity': {'self': 2, 'others': -1},
              'puzzle': 'Sob as Folhas'}],
 'consequence': 'A entrada da colmeia e redesenhada visualmente conforme a escolha: '
                'rota de resgate marcada, nova entrada tecnica ou cinturao de arbustos '
                '-- cada uma altera o risco de eventos de predador em invernos '
                'futuros.'}

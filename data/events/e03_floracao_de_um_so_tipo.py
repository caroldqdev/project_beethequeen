# -*- coding: utf-8 -*-
"""Evento 3 — Floracao de Um So Tipo (Primavera).

Cada opcao tem: councilor, action, cost {mel, operarias, relacao},
effects (deltas nos 5 eixos de Harmonia), affinity, puzzle.
"""

EVENT = {'id': 3,
 'season': 'Primavera',
 'title': 'Floracao de Um So Tipo',
 'context': 'Um campo proximo floresce com uma unica especie, em grande quantidade -- '
            'tentador, mas uma monocultura empobrece o solo com o tempo.',
 'options': [{'councilor': 'Flora',
              'action': 'Recusar o excesso e priorizar campos diversos, mesmo rendendo menos agora',
              'cost': {'mel': -8, 'operarias': 0, 'relacao': 2},
              'effects': {'biodiversidade': 8, 'producao': -3},
              'affinity': {'self': 2, 'others': -1},
              'puzzle': 'Sob as Folhas'},
             {'councilor': 'Melina',
              'action': 'Explorar ao maximo enquanto a floracao dura',
              'cost': {'mel': 4, 'operarias': 0, 'relacao': -4},
              'effects': {'producao': 8, 'biodiversidade': -6},
              'affinity': {'self': 2, 'others': -1},
              'puzzle': 'Rastro de Pólen'},
             {'councilor': 'Nectar',
              'action': 'Desenvolver uma tecnica de estocagem para aproveitar picos sazonais',
              'cost': {'mel': -18, 'operarias': 0, 'relacao': -1},
              'effects': {'inovacao': 8, 'producao': 4},
              'affinity': {'self': 2, 'others': -1},
              'puzzle': 'Rota de Voo'},
             {'councilor': 'Aurora',
              'action': 'Compartilhar a descoberta com colmeias vizinhas',
              'cost': {'mel': -5, 'operarias': 0, 'relacao': 3},
              'effects': {'cooperacao': 8},
              'affinity': {'self': 2, 'others': -1},
              'puzzle': 'Antes da Poda'}],
 'consequence': 'Se explorada sem cuidado, a monocultura empobrece o solo e o campo se '
                'torna esteril nas proximas estacoes, reduzindo opcoes futuras de '
                'forrageamento naquela regiao do mapa.'}

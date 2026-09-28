# -*- coding: utf-8 -*-
"""Evento 4 — A Seca Chega (Verao).

Cada opcao tem: councilor, action, cost {mel, operarias, relacao},
effects (deltas nos 5 eixos de Harmonia), affinity, puzzle.
"""

EVENT = {'id': 4,
 'season': 'Verao',
 'title': 'A Seca Chega',
 'context': 'Semanas sem chuva deixam flores murchando e reservas de agua escassas.',
 'options': [{'councilor': 'Flora',
              'action': 'Priorizar o resgate das flores nativas mais ameacadas',
              'cost': {'mel': -16, 'operarias': 0, 'relacao': 2},
              'effects': {'biodiversidade': 8, 'producao': -4},
              'affinity': {'self': 2, 'others': -1},
              'puzzle': 'Sob as Folhas'},
             {'councilor': 'Melina',
              'action': 'Racionar as reservas de mel para garantir a sobrevivencia da '
                        'producao',
              'cost': {'mel': -26, 'operarias': 0, 'relacao': -5},
              'effects': {'producao': 8, 'populacao': -2},
              'affinity': {'self': 2, 'others': -1},
              'puzzle': 'Rastro de Pólen'},
             {'councilor': 'Nectar',
              'action': 'Pesquisar uma rota alternativa ate fontes de agua distantes',
              'cost': {'mel': -24, 'operarias': 0, 'relacao': -2},
              'effects': {'inovacao': 8},
              'affinity': {'self': 2, 'others': -1},
              'puzzle': 'Rota de Voo'},
             {'councilor': 'Aurora',
              'action': 'Pedir ajuda e agua a colmeias vizinhas',
              'cost': {'mel': -8, 'operarias': 0, 'relacao': 4},
              'effects': {'cooperacao': 8},
              'affinity': {'self': 2, 'others': -1},
              'puzzle': 'Antes da Poda'}],
 'consequence': 'Flores nao resgatadas nesta estacao nao voltam a florescer sozinhas '
                '-- precisarao ser replantadas em estacoes futuras, reduzindo a '
                'producao de base daquela regiao ate isso acontecer.'}

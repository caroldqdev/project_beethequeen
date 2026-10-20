# -*- coding: utf-8 -*-
"""Evento 2 — Enxame Errante (Primavera).

Cada opcao tem: councilor, action, cost {mel, operarias, relacao},
effects (deltas nos 5 eixos de Harmonia), affinity, puzzle.

Este arquivo NAO sabe (e nao precisa saber) que o resultado do Evento 1
influencia a frase de introducao e o custo daqui -- essa "ponte" mora
inteira em results/r01_para_e02.py, orquestrada por game/orchestrator.py.
"""

EVENT = {'id': 2,
 'season': 'Primavera',
 'title': 'Enxame Errante',
 'context': 'Um enxame de abelhas selvagens sem colmeia pede abrigo. Aceita-las muda a '
            'composicao genetica e social da colonia.',
 'options': [{'councilor': 'Flora',
              'action': 'Acolher e integrar respeitando a diversidade genetica do enxame',
              'cost': {'mel': -22, 'operarias': 0, 'relacao': 3},
              'effects': {'biodiversidade': 8, 'populacao': 5},
              'affinity': {'self': 2, 'others': -1},
              'puzzle': 'Sob as Folhas'},
             {'councilor': 'Melina',
              'action': 'Recruta-las como forca de trabalho extra imediatamente',
              'cost': {'mel': -8, 'operarias': 25, 'relacao': -3},
              'effects': {'producao': 8, 'populacao': 6},
              'affinity': {'self': 2, 'others': -1},
              'puzzle': 'Rastro de Pólen'},
             {'councilor': 'Nectar',
              'action': 'Usar o encontro para testar uma nova tecnica de comunicacao '
                        'entre colmeias',
              'cost': {'mel': -14, 'operarias': 0, 'relacao': 0},
              'effects': {'inovacao': 8},
              'affinity': {'self': 2, 'others': -1},
              'puzzle': 'Rota de Voo'},
             {'councilor': 'Aurora',
              'action': 'Formar uma colmeia satelite aliada, sem anexacao total',
              'cost': {'mel': -5, 'operarias': 0, 'relacao': 4},
              'effects': {'cooperacao': 8, 'populacao': 3},
              'affinity': {'self': 2, 'others': -1},
              'puzzle': 'Antes da Poda'}],
 'consequence': 'O enxame se torna uma faccao interna permanente. Dependendo da '
                'escolha, reaparece como reforco numa crise futura (alianca) ou como '
                'fonte de atrito por recursos (anexacao forcada).'}
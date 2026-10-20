# -*- coding: utf-8 -*-
"""Evento 5 — A Fazenda com Pesticidas (Verao).

Cada opcao tem: councilor, action, cost {mel, operarias, relacao},
effects (deltas nos 5 eixos de Harmonia), affinity, puzzle.
"""

EVENT = {'id': 5,
 'season': 'Verao',
 'title': 'A Fazenda com Pesticidas',
 'context': 'Uma fazenda vizinha comecou a usar pesticidas. O Conselho se reune com '
            'urgencia -- cada conselheira ve o problema de um angulo diferente.',
 'options': [{'councilor': 'Flora',
              'action': 'Restaurar habitats alternativos, afastando a colonia da area contaminada',
              'cost': {'mel': -20, 'operarias': 0, 'relacao': 2},
              'effects': {'biodiversidade': 8, 'producao': -3},
              'affinity': {'self': 2, 'others': -1},
              'puzzle': 'Sob as Folhas'},
             {'councilor': 'Melina',
              'action': 'Aproveitar o campo intensamente antes da proxima pulverizacao',
              'cost': {'mel': 6, 'operarias': -6, 'relacao': -4},
              'effects': {'producao': 8},
              'extra': 'Perda de saude da colonia por exposicao aos pesticidas.',
              'affinity': {'self': 2, 'others': -1},
              'puzzle': 'Rastro de Pólen'},
             {'councilor': 'Nectar',
              'action': 'Desenvolver novas rotas de forrageamento que evitem a area tratada',
              'cost': {'mel': -18, 'operarias': 0, 'relacao': -1},
              'effects': {'inovacao': 8, 'producao': 3},
              'affinity': {'self': 2, 'others': -1},
              'puzzle': 'Rota de Voo'},
             {'councilor': 'Aurora',
              'action': 'Negociar diretamente com os agricultores por uma faixa livre de pesticidas',
              'cost': {'mel': -12, 'operarias': 0, 'relacao': 5},
              'effects': {'cooperacao': 8, 'biodiversidade': 3},
              'affinity': {'self': 2, 'others': -1},
              'puzzle': 'Antes da Poda'}],
 'consequence': 'A relacao com a fazenda fica marcada: negociar (Aurora) cria uma '
                'faixa segura permanente; ignorar ou explorar (Melina) deixa uma zona '
                'de risco que reaparece em eventos futuros de contaminacao.'}

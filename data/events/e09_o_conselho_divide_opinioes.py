# -*- coding: utf-8 -*-
"""Evento 9 — O Conselho Divide Opinioes (Outono).

Cada opcao tem: councilor, action, cost {mel, operarias, relacao},
effects (deltas nos 5 eixos de Harmonia), affinity, puzzle.
"""

EVENT = {'id': 9,
 'season': 'Outono',
 'title': 'O Conselho Divide Opinioes',
 'context': 'Pela primeira vez, duas conselheiras discordam abertamente na frente da '
            'colonia sobre qual prioridade definira o preparo para o inverno.',
 'options': [{'councilor': 'Flora',
              'action': 'Dar prioridade total a recuperacao do ecossistema antes do '
                        'frio',
              'cost': {'mel': -14, 'operarias': 0, 'relacao': -1},
              'effects': {'biodiversidade': 8},
              'affinity': {'self': 2, 'others': -2},
              'puzzle': 'Sob as Folhas'},
             {'councilor': 'Melina',
              'action': 'Dar prioridade total ao acumulo de reservas',
              'cost': {'mel': -8, 'operarias': 0, 'relacao': -3},
              'effects': {'producao': 8},
              'affinity': {'self': 2, 'others': -2},
              'puzzle': 'Rastro de Pólen'},
             {'councilor': 'Nectar',
              'action': 'Propor uma solucao tecnica que tente equilibrar as duas '
                        'demandas',
              'cost': {'mel': -22, 'operarias': 0, 'relacao': -1},
              'effects': {'inovacao': 8, 'biodiversidade': 2, 'producao': 2},
              'affinity': {'self': 2, 'others': -1},
              'puzzle': 'Rota de Voo'},
             {'councilor': 'Aurora',
              'action': 'Mediar o debate publicamente e buscar consenso entre as '
                        'conselheiras',
              'cost': {'mel': -5, 'operarias': 0, 'relacao': 5},
              'effects': {'cooperacao': 8},
              'affinity': {'self': 2, 'others': 0},
              'puzzle': 'Antes da Poda'}],
 'consequence': 'Este e o primeiro evento em que a afinidade das conselheiras nao '
                'escolhidas pode cair alem do padrao -- se alguma afinidade ja estiver '
                'baixa, ela passa a discordar abertamente em eventos futuros, '
                'reduzindo bonus.'}

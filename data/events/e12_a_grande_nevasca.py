# -*- coding: utf-8 -*-
"""Evento 12 — A Grande Nevasca (Inverno).

Cada opcao tem: councilor, action, cost {mel, operarias, relacao},
effects (deltas nos 5 eixos de Harmonia), affinity, puzzle.
"""

EVENT = {'id': 12,
 'season': 'Inverno',
 'title': 'A Grande Nevasca',
 'context': 'O evento culminante do ano: uma nevasca severa ameaca tudo o que foi '
            'construido. A resposta da colonia reflete diretamente o equilibrio (ou '
            'desequilibrio) acumulado no painel de Harmonia e na Relacao com a '
            'Colmeia.',
 'mirror_event': True,
 'options': [{'councilor': 'Melina',
              'action': 'Fechar a colmeia e sobreviver apenas com o que foi guardado',
              'cost': {'mel': 'all', 'operarias': 0, 'relacao': 0},
              'mirror_axis': 'mel_reserve',
              'affinity': {'self': 2, 'others': -1},
              'puzzle': 'Rastro de Pólen'},
             {'councilor': 'Flora',
              'action': 'Confiar nos corredores ecologicos criados ao longo do ano '
                        'para abrigo extra',
              'cost': {'mel': 0, 'operarias': 0, 'relacao': 0},
              'mirror_axis': 'biodiversidade',
              'affinity': {'self': 2, 'others': -1},
              'puzzle': 'Sob as Folhas'},
             {'councilor': 'Nectar',
              'action': 'Ativar as inovacoes desenvolvidas ao longo do ano',
              'cost': {'mel': 0, 'operarias': 0, 'relacao': 0},
              'mirror_axis': 'inovacao',
              'affinity': {'self': 2, 'others': -1},
              'puzzle': 'Rota de Voo'},
             {'councilor': 'Aurora',
              'action': 'Pedir abrigo as colonias aliadas formadas durante o ano',
              'cost': {'mel': 0, 'operarias': 0, 'relacao': 0},
              'mirror_axis': 'relacao',
              'affinity': {'self': 2, 'others': -1},
              'puzzle': 'Antes da Poda'}],
 'consequence': 'Este e o evento-espelho do ano: cada opcao so funciona bem se o '
                'jogador investiu naquele eixo ao longo das estacoes anteriores. E '
                "aqui que a 'Harmonia da Colmeia' e a 'Relacao com a Colmeia' deixam "
                'de ser numeros e viram sobrevivencia real -- reforcando a mensagem '
                'central de que nao existe atalho para o equilibrio.'}

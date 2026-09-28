# -*- coding: utf-8 -*-
"""Evento 6 — Incendio nas Redondezas (Verao).

Cada opcao tem: councilor, action, cost {mel, operarias, relacao},
effects (deltas nos 5 eixos de Harmonia), affinity, puzzle.
"""

EVENT = {'id': 6,
 'season': 'Verao',
 'title': 'Incendio nas Redondezas',
 'context': 'Fumaca no horizonte -- um incendio se aproxima da colmeia. E preciso '
            'decidir agora.',
 'options': [{'councilor': 'Melina',
              'action': 'Apagar o fogo agora com o que houver disponivel',
              'cost': {'mel': -5, 'operarias': -35, 'relacao': -6},
              'effects': {'populacao': -10},
              'extra': 'Alto risco, mas salva o territorio.',
              'affinity': {'self': 2, 'others': -1},
              'puzzle': 'Rastro de Pólen'},
             {'councilor': 'Aurora',
              'action': 'Salvar as operarias do local, abandonando parte do territorio',
              'cost': {'mel': -15, 'operarias': -5, 'relacao': 3},
              'effects': {'producao': -6, 'populacao': 4},
              'affinity': {'self': 2, 'others': -1},
              'puzzle': 'Antes da Poda'},
             {'councilor': 'Nectar',
              'action': 'Investir em colmeias a prova de fogo para o futuro',
              'cost': {'mel': -20, 'operarias': -8, 'relacao': -2},
              'effects': {'inovacao': 8},
              'extra': 'Reduz dano de incendios futuros.',
              'affinity': {'self': 2, 'others': -1},
              'puzzle': 'Rota de Voo'},
             {'councilor': 'Flora',
              'action': 'Restaurar a area queimada depois, criando uma barreira verde '
                        'natural',
              'cost': {'mel': -15, 'operarias': 0, 'relacao': 2},
              'effects': {'biodiversidade': 6},
              'affinity': {'self': 2, 'others': -1},
              'puzzle': 'Sob as Folhas'}],
 'consequence': "A opcao escolhida define a 'cicatriz' visual do mapa: area queimada "
                'permanente (Melina), colmeia realocada (Aurora), estrutura reforcada '
                '(Nectar) ou barreira verde (Flora) -- cada uma altera o risco de '
                'incendios futuros.'}

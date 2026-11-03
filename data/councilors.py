# -*- coding: utf-8 -*-
"""As 4 conselheiras (falas, cores, emoji) e a penalidade de falha de cada uma.

O campo 'emoji' continua aqui so como referencia/texto alternativo (por
exemplo para logs ou um eventual modo texto). Para DESENHAR o emoji na
tela, o jogo usa o campo 'emoji_file', que aponta para um PNG em
assets/emoji/ -- pygame nao consegue renderizar emoji colorido a partir
de fonte de texto, entao usamos imagens prontas (Twemoji, licenca CC-BY 4.0).
Se quiser trocar o emoji de uma conselheira, troque o PNG em assets/emoji/
com o mesmo nome de arquivo (ou aponte 'emoji_file' para um novo arquivo).
"""

COUNCILORS = {'Flora': {'emoji': '🌼',
           'emoji_file': 'flora.png',
           'motto': 'Sem diversidade, não há futuro.',
           'title': 'Guardiã da Biodiversidade',
           'axis': 'biodiversidade',
           'intro': 'Pensa em decadas, não em estações. Prioriza reflorestamento e corredores ecológicos. '
           'Suas soluções são lentas, mas regenerativas.',
           'color': (110, 179, 92)},
 'Melina': {'emoji': '🍯',
            'emoji_file': 'melina.png',
            'motto': 'O inverno sempre chega.',
            'title': 'Guardiã da Produção',
            'axis': 'producao',
            'intro': 'Prioriza reservas e produção hoje, não depois. '
            'Suas soluções são rápidas e pragmáticas, as vezes às custas do ecossistema e da confiança da colônia.',
            'color': (214, 158, 46)},
 'Nectar': {'emoji': '🚀',
            'emoji_file': 'nectar.png',
            'motto': 'Quem evolui primeiro sobrevive.',
            'title': 'Guardiã da Inovação',
            'axis': 'inovacao',
            'intro': 'Aposta em soluções novas, mesmo sem garantia. '
            'O investimento é sempre alto, e o retorno só aparece quando a ideia é posta à prova.',
            'color': (86, 130, 214)},
 'Aurora': {'emoji': '🤝',
            'emoji_file': 'aurora.png',
            'motto': 'Nenhuma colmeia floresce sozinha.',
            'title': 'Guardiã da Cooperação',
            'axis': 'cooperacao',
            'intro': 'Acredita que alianças valem mais que recursos. Barata em recurso, cara em tempo e produção perdida, '
            'mas sempre fortalece a confiança da colmeia.',
            'color': (196, 108, 196)}}

FAIL_PENALTY = {'Melina': {'operarias': -10,
            'text': 'ação apressada machuca gente: -10 operarias extras.'},
 'Flora': {'mel': -10, 'text': 'tempo perdido / replantio: -10 mel extra.'},
 'Nectar': {'relacao': -8,
            'text': 'a colonia perde confiança em experimentos que não deram certo: -8 '
                    'de Relacao.'},
 'Aurora': {'relacao': -4,
            'weaken_next_cooperacao': 0.5,
            'text': 'a promessa feita não foi cumprida: -4 de Relação e o próximo '
                    'ganho de Cooperação vale metade.'}}


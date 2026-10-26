# -*- coding: utf-8 -*-
"""AS CONSELHEIRAS: o texto de cada uma (tela de apresentação), a cor, o emoji
e a PENALIDADE EXTRA que ela sofre quando o minigame não vai bem.

  apresentacao      texto da tela da conselheira
  penalidade_falha  o que se perde, além do normal, quando o minigame dela dá
                    abaixo de "sucesso" (valores negativos tiram; "texto" é o
                    que aparece na tela de resultado)

O emoji é uma imagem em assets/emoji/ (o pygame não desenha emoji de fonte).
"""

# a ordem em que as conselheiras aparecem na apresentação
ORDEM = ["Flora", "Melina", "Nectar", "Aurora"]

CONSELHEIRAS = {
    "Flora": {
        "emoji": "🌼",
        "arquivo_emoji": "flora.png",
        "lema": "Sem diversidade, não há futuro.",
        "titulo": "Guardiã da Biodiversidade",
        "eixo": "biodiversidade",
        "apresentacao":
            "Pensa em décadas, não em estações. Prioriza reflorestamento e "
            "corredores ecológicos. Suas soluções são lentas, mas regenerativas.",
        "cor": (110, 179, 92),
        "penalidade_falha": {
            "mel": -10,
            "texto": "tempo perdido / replantio: -10 mel extra.",
        },
    },
    "Melina": {
        "emoji": "🍯",
        "arquivo_emoji": "melina.png",
        "lema": "O inverno sempre chega.",
        "titulo": "Guardiã da Produção",
        "eixo": "producao",
        "apresentacao":
            "Prioriza reservas e produção hoje, não depois. Suas soluções são "
            "rápidas e pragmáticas, às vezes às custas do ecossistema e da confiança "
            "da colônia.",
        "cor": (214, 158, 46),
        "penalidade_falha": {
            "operarias": -10,
            "texto": "ação apressada machuca gente: -10 operárias extras.",
        },
    },
    "Nectar": {
        "emoji": "🚀",
        "arquivo_emoji": "nectar.png",
        "lema": "Quem evolui primeiro sobrevive.",
        "titulo": "Guardiã da Inovação",
        "eixo": "inovacao",
        "apresentacao":
            "Aposta em soluções novas, mesmo sem garantia. O investimento é sempre "
            "alto, e o retorno só aparece quando a ideia é posta à prova.",
        "cor": (86, 130, 214),
        "penalidade_falha": {
            "relacao": -8,
            "texto":
                "a colônia perde confiança em experimentos que não deram certo: -8 "
                "de Relação.",
        },
    },
    "Aurora": {
        "emoji": "🤝",
        "arquivo_emoji": "aurora.png",
        "lema": "Nenhuma colmeia floresce sozinha.",
        "titulo": "Guardiã da Cooperação",
        "eixo": "cooperacao",
        "apresentacao":
            "Acredita que alianças valem mais que recursos. Barata em recurso, cara "
            "em tempo e produção perdida, mas sempre fortalece a confiança da "
            "colmeia.",
        "cor": (196, 108, 196),
        "penalidade_falha": {
            "relacao": -4,
            "enfraquece_proxima_cooperacao": 0.5,
            "texto":
                "a promessa feita não foi cumprida: -4 de Relação e o próximo ganho "
                "de Cooperação vale metade.",
        },
    },
}

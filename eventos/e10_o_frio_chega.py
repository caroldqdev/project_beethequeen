# -*- coding: utf-8 -*-
"""Evento 10 — O Frio Chega (Inverno).

SÓ a situação: o texto de abertura, as 4 opções e o PREÇO de cada uma.
  - qual minigame cada conselheira joga   -> minigames/e10_o_frio_chega.py
  - o que acontece depois (efeitos etc.)  -> resultados/e10_o_frio_chega.py

custo: valores NEGATIVOS saem do bolso; positivos entram. "tudo" = todo o mel.
"""

EVENTO = {
    "id": 10,
    "estacao": "Inverno",
    "titulo": "O Frio Chega",
    "contexto":
        "As primeiras geadas testam tudo o que foi construido no Outono. As reservas "
        "acumuladas -- ou a falta delas -- decidem o tom do inverno.",
    "opcoes": [
        {
            "conselheira": "Melina",
            "acao":
                "Consumir as reservas de forma controlada, priorizando a producao "
                "minima",
            "custo": {"mel": -38, "operarias": 0, "relacao": -4},
        },
        {
            "conselheira": "Flora",
            "acao":
                "Manter parte da colonia ativa cuidando de plantas resistentes ao "
                "frio",
            "custo": {"mel": -10, "operarias": 0, "relacao": 2},
        },
        {
            "conselheira": "Nectar",
            "acao": "Testar um metodo de aquecimento coletivo mais eficiente",
            "custo": {"mel": -16, "operarias": 0, "relacao": -1},
        },
        {
            "conselheira": "Aurora",
            "acao":
                "Formar um circulo de aquecimento com todas as operarias disponiveis",
            "custo": {"mel": -5, "operarias": 0, "relacao": 4},
        },
    ],
}

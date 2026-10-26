# -*- coding: utf-8 -*-
"""Evento 2 — Enxame Errante (Primavera).

SÓ a situação: o texto de abertura, as 4 opções e o PREÇO de cada uma.
  - qual minigame cada conselheira joga   -> minigames/e02_enxame_errante.py
  - o que acontece depois (efeitos etc.)  -> resultados/e02_enxame_errante.py

custo: valores NEGATIVOS saem do bolso; positivos entram. "tudo" = todo o mel.
"""

EVENTO = {
    "id": 2,
    "estacao": "Primavera",
    "titulo": "Enxame Errante",
    "contexto":
        "Um enxame de abelhas selvagens sem colmeia pede abrigo. Aceita-las muda a "
        "composicao genetica e social da colonia.",
    "opcoes": [
        {
            "conselheira": "Flora",
            "acao": "Acolher e integrar respeitando a diversidade genetica do enxame",
            "custo": {"mel": -22, "operarias": 0, "relacao": 3},
        },
        {
            "conselheira": "Melina",
            "acao": "Recruta-las como forca de trabalho extra imediatamente",
            "custo": {"mel": -8, "operarias": 25, "relacao": -3},
        },
        {
            "conselheira": "Nectar",
            "acao":
                "Usar o encontro para testar uma nova tecnica de comunicacao entre "
                "colmeias",
            "custo": {"mel": -14, "operarias": 0, "relacao": 0},
        },
        {
            "conselheira": "Aurora",
            "acao": "Formar uma colmeia satelite aliada, sem anexacao total",
            "custo": {"mel": -5, "operarias": 0, "relacao": 4},
        },
    ],
}

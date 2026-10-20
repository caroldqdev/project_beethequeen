# -*- coding: utf-8 -*-
"""Evento 7 — Colonizar Outro Jardim (Outono).

SÓ a situação: o texto de abertura, as 4 opções e o PREÇO de cada uma.
  - qual minigame cada conselheira joga   -> minigames/e07_colonizar_outro_jardim.py
  - o que acontece depois (efeitos etc.)  -> resultados/e07_colonizar_outro_jardim.py

custo: valores NEGATIVOS saem do bolso; positivos entram. "tudo" = todo o mel.
"""

EVENTO = {
    "id": 7,
    "estacao": "Outono",
    "titulo": "Colonizar Outro Jardim",
    "contexto":
        "Um jardim vizinho, ainda livre, pode se tornar uma extensao da colonia "
        "antes do inverno.",
    "opcoes": [
        {
            "conselheira": "Melina",
            "acao": "Colonizar o jardim para garantir mais uma fonte de reservas",
            "custo": {"mel": -2, "operarias": -8, "relacao": -2},
        },
        {
            "conselheira": "Flora",
            "acao": "Colonizar de forma gradual, preservando a vegetacao ja existente",
            "custo": {"mel": -10, "operarias": 0, "relacao": 2},
        },
        {
            "conselheira": "Nectar",
            "acao": "Usar o novo jardim como posto avancado de pesquisa",
            "custo": {"mel": -18, "operarias": 0, "relacao": -1},
        },
        {
            "conselheira": "Aurora",
            "acao": "Propor a colonizacao conjunta com outra colmeia amiga",
            "custo": {"mel": -5, "operarias": 0, "relacao": 3},
        },
    ],
}

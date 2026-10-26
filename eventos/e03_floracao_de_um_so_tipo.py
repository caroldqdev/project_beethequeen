# -*- coding: utf-8 -*-
"""Evento 3 — Floracao de Um So Tipo (Primavera).

SÓ a situação: o texto de abertura, as 4 opções e o PREÇO de cada uma.
  - qual minigame cada conselheira joga   -> minigames/e03_floracao_de_um_so_tipo.py
  - o que acontece depois (efeitos etc.)  -> resultados/e03_floracao_de_um_so_tipo.py

custo: valores NEGATIVOS saem do bolso; positivos entram. "tudo" = todo o mel.
"""

EVENTO = {
    "id": 3,
    "estacao": "Primavera",
    "titulo": "Floracao de Um So Tipo",
    "contexto":
        "Um campo proximo floresce com uma unica especie, em grande quantidade -- "
        "tentador, mas uma monocultura empobrece o solo com o tempo.",
    "opcoes": [
        {
            "conselheira": "Flora",
            "acao":
                "Recusar o excesso e priorizar campos diversos, mesmo rendendo menos "
                "agora",
            "custo": {"mel": -8, "operarias": 0, "relacao": 2},
        },
        {
            "conselheira": "Melina",
            "acao": "Explorar ao maximo enquanto a floracao dura",
            "custo": {"mel": 4, "operarias": 0, "relacao": -4},
        },
        {
            "conselheira": "Nectar",
            "acao":
                "Desenvolver uma tecnica de estocagem para aproveitar picos sazonais",
            "custo": {"mel": -18, "operarias": 0, "relacao": -1},
        },
        {
            "conselheira": "Aurora",
            "acao": "Compartilhar a descoberta com colmeias vizinhas",
            "custo": {"mel": -5, "operarias": 0, "relacao": 3},
        },
    ],
}

# -*- coding: utf-8 -*-
"""Evento 9 — O Conselho Divide Opinioes (Outono).

SÓ a situação: o texto de abertura, as 4 opções e o PREÇO de cada uma.
  - qual minigame cada conselheira joga   -> minigames/e09_o_conselho_divide_opinioes.py
  - o que acontece depois (efeitos etc.)  -> resultados/e09_o_conselho_divide_opinioes.py

custo: valores NEGATIVOS saem do bolso; positivos entram. "tudo" = todo o mel.
"""

EVENTO = {
    "id": 9,
    "estacao": "Outono",
    "titulo": "O Conselho Divide Opinioes",
    "contexto":
        "Pela primeira vez, duas conselheiras discordam abertamente na frente da "
        "colonia sobre qual prioridade definira o preparo para o inverno.",
    "opcoes": [
        {
            "conselheira": "Flora",
            "acao": "Dar prioridade total a recuperacao do ecossistema antes do frio",
            "custo": {"mel": -14, "operarias": 0, "relacao": -1},
        },
        {
            "conselheira": "Melina",
            "acao": "Dar prioridade total ao acumulo de reservas",
            "custo": {"mel": -8, "operarias": 0, "relacao": -3},
        },
        {
            "conselheira": "Nectar",
            "acao": "Propor uma solucao tecnica que tente equilibrar as duas demandas",
            "custo": {"mel": -22, "operarias": 0, "relacao": -1},
        },
        {
            "conselheira": "Aurora",
            "acao":
                "Mediar o debate publicamente e buscar consenso entre as conselheiras",
            "custo": {"mel": -5, "operarias": 0, "relacao": 5},
        },
    ],
}

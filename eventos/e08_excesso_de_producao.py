# -*- coding: utf-8 -*-
"""Evento 8 — Excesso de Producao (Outono).

SÓ a situação: o texto de abertura, as 4 opções e o PREÇO de cada uma.
  - qual minigame cada conselheira joga   -> minigames/e08_excesso_de_producao.py
  - o que acontece depois (efeitos etc.)  -> resultados/e08_excesso_de_producao.py

custo: valores NEGATIVOS saem do bolso; positivos entram. "tudo" = todo o mel.
"""

EVENTO = {
    "id": 8,
    "estacao": "Outono",
    "titulo": "Excesso de Producao",
    "contexto":
        "A colheita do ano rendeu mais mel do que a estrutura atual comporta -- sem "
        "espaco, parte dele sera perdido.",
    "opcoes": [
        {
            "conselheira": "Melina",
            "acao": "Expandir os favos as pressas para nao perder nada",
            "custo": {"mel": -22, "operarias": 0, "relacao": -2},
        },
        {
            "conselheira": "Nectar",
            "acao": "Testar um novo formato hexagonal mais eficiente de armazenamento",
            "custo": {"mel": -18, "operarias": 0, "relacao": -1},
        },
        {
            "conselheira": "Flora",
            "acao": "Doar o excedente para polinizar areas que precisam de recuperacao",
            "custo": {"mel": -6, "operarias": 0, "relacao": 3},
        },
        {
            "conselheira": "Aurora",
            "acao": "Repartir o excedente com colmeias vizinhas em dificuldade",
            "custo": {"mel": -6, "operarias": 0, "relacao": 4},
        },
    ],
}

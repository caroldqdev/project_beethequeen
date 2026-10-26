# -*- coding: utf-8 -*-
"""Evento 11 — Teias na Entrada (Inverno).

SÓ a situação: o texto de abertura, as 4 opções e o PREÇO de cada uma.
  - qual minigame cada conselheira joga   -> minigames/e11_teias_na_entrada.py
  - o que acontece depois (efeitos etc.)  -> resultados/e11_teias_na_entrada.py

custo: valores NEGATIVOS saem do bolso; positivos entram. "tudo" = todo o mel.
"""

EVENTO = {
    "id": 11,
    "estacao": "Inverno",
    "titulo": "Teias na Entrada",
    "contexto":
        "Uma aranha construiu teias perto da entrada da colmeia. Operarias "
        "forrageadoras estao presas.",
    "opcoes": [
        {
            "conselheira": "Aurora",
            "acao": "Organizar um resgate coletivo, evitando as teias",
            "custo": {"mel": -10, "operarias": 0, "relacao": 4},
        },
        {
            "conselheira": "Melina",
            "acao":
                "Sacrificar as presas e seguir em frente para nao perder mais "
                "recursos",
            "custo": {"mel": 0, "operarias": -10, "relacao": -5},
        },
        {
            "conselheira": "Nectar",
            "acao": "Testar uma rota alternativa de entrada que evite a area da teia",
            "custo": {"mel": -14, "operarias": 0, "relacao": -1},
        },
        {
            "conselheira": "Flora",
            "acao":
                "Deixar a aranha em paz e replantar arbustos que naturalmente a "
                "afastem",
            "custo": {"mel": -10, "operarias": 0, "relacao": 2},
        },
    ],
}

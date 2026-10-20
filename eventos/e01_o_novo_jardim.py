# -*- coding: utf-8 -*-
"""Evento 1 — O Novo Jardim (Primavera).

SÓ a situação: o texto de abertura, as 4 opções e o PREÇO de cada uma.
  - qual minigame cada conselheira joga   -> minigames/e01_o_novo_jardim.py
  - o que acontece depois (efeitos etc.)  -> resultados/e01_o_novo_jardim.py

custo: valores NEGATIVOS saem do bolso; positivos entram. "tudo" = todo o mel.
"""

EVENTO = {
    "id": 1,
    "estacao": "Primavera",
    "titulo": "O Novo Jardim",
    "contexto":
        "Exploradoras encontram um jardim particular ainda não polinizado por "
        "ninguém, mas outros insetos também o notaram.",
    "opcoes": [
        {
            "conselheira": "Flora",
            "acao":
                "Mapear com cuidado, respeitando as espécies nativas antes de "
                "polinizar",
            "custo": {"mel": -15, "operarias": 0, "relacao": 3},
        },
        {
            "conselheira": "Melina",
            "acao": "Polinizar tudo!! Antes que outra espécie tome o jardim",
            "custo": {"mel": -5, "operarias": -12, "relacao": -4},
        },
        {
            "conselheira": "Nectar",
            "acao": "Testar uma rota de voo experimental mais eficiente",
            "custo": {"mel": -22, "operarias": 0, "relacao": 0},
        },
        {
            "conselheira": "Aurora",
            "acao": "Negociar com o jardineiro humano um plantio em conjunto",
            "custo": {"mel": -5, "operarias": 0, "relacao": 5},
        },
    ],
}

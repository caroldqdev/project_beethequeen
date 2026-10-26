# -*- coding: utf-8 -*-
"""Evento 4 — A Seca Chega (Verao).

SÓ a situação: o texto de abertura, as 4 opções e o PREÇO de cada uma.
  - qual minigame cada conselheira joga   -> minigames/e04_a_seca_chega.py
  - o que acontece depois (efeitos etc.)  -> resultados/e04_a_seca_chega.py

custo: valores NEGATIVOS saem do bolso; positivos entram. "tudo" = todo o mel.
"""

EVENTO = {
    "id": 4,
    "estacao": "Verao",
    "titulo": "A Seca Chega",
    "contexto":
        "Semanas sem chuva deixam flores murchando e reservas de agua escassas.",
    "opcoes": [
        {
            "conselheira": "Flora",
            "acao": "Priorizar o resgate das flores nativas mais ameacadas",
            "custo": {"mel": -16, "operarias": 0, "relacao": 2},
        },
        {
            "conselheira": "Melina",
            "acao":
                "Racionar as reservas de mel para garantir a sobrevivencia da "
                "producao",
            "custo": {"mel": -26, "operarias": 0, "relacao": -5},
        },
        {
            "conselheira": "Nectar",
            "acao": "Pesquisar uma rota alternativa ate fontes de agua distantes",
            "custo": {"mel": -24, "operarias": 0, "relacao": -2},
        },
        {
            "conselheira": "Aurora",
            "acao": "Pedir ajuda e agua a colmeias vizinhas",
            "custo": {"mel": -8, "operarias": 0, "relacao": 4},
        },
    ],
}

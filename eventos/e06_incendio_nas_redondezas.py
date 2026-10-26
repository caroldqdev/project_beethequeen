# -*- coding: utf-8 -*-
"""Evento 6 — Incendio nas Redondezas (Verao).

SÓ a situação: o texto de abertura, as 4 opções e o PREÇO de cada uma.
  - qual minigame cada conselheira joga   -> minigames/e06_incendio_nas_redondezas.py
  - o que acontece depois (efeitos etc.)  -> resultados/e06_incendio_nas_redondezas.py

custo: valores NEGATIVOS saem do bolso; positivos entram. "tudo" = todo o mel.
"""

EVENTO = {
    "id": 6,
    "estacao": "Verao",
    "titulo": "Incendio nas Redondezas",
    "contexto":
        "Fumaca no horizonte -- um incendio se aproxima da colmeia. E preciso "
        "decidir agora.",
    "opcoes": [
        {
            "conselheira": "Melina",
            "acao": "Apagar o fogo agora com o que houver disponivel",
            "custo": {"mel": -5, "operarias": -35, "relacao": -6},
        },
        {
            "conselheira": "Aurora",
            "acao": "Salvar as operarias do local, abandonando parte do territorio",
            "custo": {"mel": -15, "operarias": -5, "relacao": 3},
        },
        {
            "conselheira": "Nectar",
            "acao": "Investir em colmeias a prova de fogo para o futuro",
            "custo": {"mel": -20, "operarias": -8, "relacao": -2},
        },
        {
            "conselheira": "Flora",
            "acao":
                "Restaurar a area queimada depois, criando uma barreira verde natural",
            "custo": {"mel": -15, "operarias": 0, "relacao": 2},
        },
    ],
}

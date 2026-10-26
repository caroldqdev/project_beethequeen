# -*- coding: utf-8 -*-
"""Evento 5 — A Fazenda com Pesticidas (Verao).

SÓ a situação: o texto de abertura, as 4 opções e o PREÇO de cada uma.
  - qual minigame cada conselheira joga   -> minigames/e05_a_fazenda_com_pesticidas.py
  - o que acontece depois (efeitos etc.)  -> resultados/e05_a_fazenda_com_pesticidas.py

custo: valores NEGATIVOS saem do bolso; positivos entram. "tudo" = todo o mel.
"""

EVENTO = {
    "id": 5,
    "estacao": "Verao",
    "titulo": "A Fazenda com Pesticidas",
    "contexto":
        "Uma fazenda vizinha comecou a usar pesticidas. O Conselho se reune com "
        "urgencia -- cada conselheira ve o problema de um angulo diferente.",
    "opcoes": [
        {
            "conselheira": "Flora",
            "acao":
                "Restaurar habitats alternativos, afastando a colonia da area "
                "contaminada",
            "custo": {"mel": -20, "operarias": 0, "relacao": 2},
        },
        {
            "conselheira": "Melina",
            "acao": "Aproveitar o campo intensamente antes da proxima pulverizacao",
            "custo": {"mel": 6, "operarias": -6, "relacao": -4},
        },
        {
            "conselheira": "Nectar",
            "acao":
                "Desenvolver novas rotas de forrageamento que evitem a area tratada",
            "custo": {"mel": -18, "operarias": 0, "relacao": -1},
        },
        {
            "conselheira": "Aurora",
            "acao":
                "Negociar diretamente com os agricultores por uma faixa livre de "
                "pesticidas",
            "custo": {"mel": -12, "operarias": 0, "relacao": 5},
        },
    ],
}

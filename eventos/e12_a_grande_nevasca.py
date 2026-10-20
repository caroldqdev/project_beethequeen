# -*- coding: utf-8 -*-
"""Evento 12 — A Grande Nevasca (Inverno).

SÓ a situação: o texto de abertura, as 4 opções e o PREÇO de cada uma.
  - qual minigame cada conselheira joga   -> minigames/e12_a_grande_nevasca.py
  - o que acontece depois (efeitos etc.)  -> resultados/e12_a_grande_nevasca.py

custo: valores NEGATIVOS saem do bolso; positivos entram. "tudo" = todo o mel.
"""

EVENTO = {
    "id": 12,
    "estacao": "Inverno",
    "titulo": "A Grande Nevasca",
    "contexto":
        "O evento culminante do ano: uma nevasca severa ameaca tudo o que foi "
        "construido. A resposta da colonia reflete diretamente o equilibrio (ou "
        "desequilibrio) acumulado no painel de Harmonia e na Relacao com a Colmeia.",
    "opcoes": [
        {
            "conselheira": "Melina",
            "acao": "Fechar a colmeia e sobreviver apenas com o que foi guardado",
            "custo": {"mel": "tudo", "operarias": 0, "relacao": 0},
        },
        {
            "conselheira": "Flora",
            "acao":
                "Confiar nos corredores ecologicos criados ao longo do ano para "
                "abrigo extra",
            "custo": {"mel": 0, "operarias": 0, "relacao": 0},
        },
        {
            "conselheira": "Nectar",
            "acao": "Ativar as inovacoes desenvolvidas ao longo do ano",
            "custo": {"mel": 0, "operarias": 0, "relacao": 0},
        },
        {
            "conselheira": "Aurora",
            "acao": "Pedir abrigo as colonias aliadas formadas durante o ano",
            "custo": {"mel": 0, "operarias": 0, "relacao": 0},
        },
    ],
}

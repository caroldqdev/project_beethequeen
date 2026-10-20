# -*- coding: utf-8 -*-
"""Resultado do Evento 9 — O Conselho Divide Opinioes.

O que ACONTECE depois da escolha e do minigame:
  consequencia  o texto da tela de consequência
  efeitos       por conselheira: o que muda na Harmonia ("harmonia"), a afinidade
                ("propria" = dela, "demais" = das outras) e um "extra" opcional
  proximo       o que este resultado muda no PRÓXIMO evento (texto, desconto, frase)

Os efeitos valem por inteiro num sucesso; no parcial e na falha são reduzidos
(multiplicador do minigame, em minigames/jogos/base.py).
O preço de cada opção está em eventos/e09_o_conselho_divide_opinioes.py.
"""

RESULTADO = {
    "consequencia":
        "Este e o primeiro evento em que a afinidade das conselheiras nao escolhidas "
        "pode cair alem do padrao -- se alguma afinidade ja estiver baixa, ela passa "
        "a discordar abertamente em eventos futuros, reduzindo bonus.",
    "efeitos": {
        "Flora": {
            "harmonia": {"biodiversidade": 8},
            "afinidade": {"propria": 2, "demais": -2},
        },
        "Melina": {
            "harmonia": {"producao": 8},
            "afinidade": {"propria": 2, "demais": -2},
        },
        "Nectar": {
            "harmonia": {"inovacao": 8, "biodiversidade": 2, "producao": 2},
            "afinidade": {"propria": 2, "demais": -1},
        },
        "Aurora": {
            "harmonia": {"cooperacao": 8},
            "afinidade": {"propria": 2, "demais": 0},
        },
    },
    # --- O QUE ESTE RESULTADO MUDA NO PROXIMO EVENTO ------------------------
    # Ainda sem ponte: o proximo evento aparece com o texto e o custo normais.
    # Para criar uma, troque o None por um bloco assim (o e01_o_novo_jardim.py
    # ja tem uma pronta, com tudo preenchido):
    #
    #   "proximo": {
    #       # texto que SUBSTITUI a abertura do proximo evento, por (conselheira, resultado)
    #       "frases": {("Flora", "super_sucesso"): "texto..."},
    #       # quanto o custo da escolha do proximo evento muda (0.5 = metade, 1.5 = +50%)
    #       "fator_custo": {"super_sucesso": 0.5, "sucesso": 1.0, "falha": 1.5},
    #       "moedas_afetadas": ["mel", "operarias"],
    #       # frase na tela de resultado do minigame do proximo evento; pode usar
    #       # {mel_normal} {mel_final} {mel_diferenca} (e o mesmo com operarias/relacao)
    #       "notas": {"super_sucesso": "Você pagaria {mel_normal} e pagou {mel_final}."},
    #   },
    "proximo": None,
}

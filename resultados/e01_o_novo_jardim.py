# -*- coding: utf-8 -*-
"""Resultado do Evento 1 — O Novo Jardim.

O que ACONTECE depois da escolha e do minigame:
  consequencia  o texto da tela de consequência
  efeitos       por conselheira: o que muda na Harmonia ("harmonia"), a afinidade
                ("propria" = dela, "demais" = das outras) e um "extra" opcional
  proximo       o que este resultado muda no PRÓXIMO evento (texto, desconto, frase)

Os efeitos valem por inteiro num sucesso; no parcial e na falha são reduzidos
(multiplicador do minigame, em minigames/jogos/base.py).
O preço de cada opção está em eventos/e01_o_novo_jardim.py.
"""

RESULTADO = {
    "consequencia":
        "O jardim passa a existir permanentemente no mapa \nA forma como foi ocupado "
        "define se ele aparecerá depois como aliado (Aurora/Flora) ou como fonte de "
        "conflito com outros polinizadores (Melina/Nectar).",
    "efeitos": {
        "Flora": {
            "harmonia": {"biodiversidade": 8, "producao": 3},
            "afinidade": {"propria": 2, "demais": -1},
        },
        "Melina": {
            "harmonia": {"producao": 8, "biodiversidade": -5},
            "afinidade": {"propria": 2, "demais": -1},
        },
        "Nectar": {
            "harmonia": {"inovacao": 8, "producao": 4},
            "afinidade": {"propria": 2, "demais": -1},
        },
        "Aurora": {
            "harmonia": {"cooperacao": 8},
            "afinidade": {"propria": 2, "demais": -1},
        },
    },
    "proximo": {
        "frases": {
            ("Flora", "super_sucesso"):
                "O jardim recém-mapeado por Flora virou um verdadeiro mosaico de "
                "espécies -- não é à toa que o enxame errante escolheu pousar bem "
                "ali perto, atraído pela diversidade que a colônia ajudou a manter.",
            ("Flora", "sucesso"):
                "O cuidado de Flora com o jardim deixou um rastro de flores variadas "
                "pela região -- talvez seja por isso que o enxame decidiu se "
                "aproximar da colmeia.",
            ("Flora", "falha"):
                "Mesmo com boas intenções, o mapeamento não rendeu o refúgio florido "
                "que Flora esperava -- o enxame que aparece agora encontra pouco "
                "além do que já havia antes.",
            ("Melina", "super_sucesso"):
                "A polinização acelerada de Melina lotou os arredores de mel "
                "disponível -- e foi essa fartura que atraiu o enxame errante até a "
                "porta da colmeia.",
            ("Melina", "sucesso"):
                "A pressa de Melina rendeu fartura no jardim, mesmo à custa de "
                "alguma bagunça -- fartura o bastante pra chamar a atenção de um "
                "enxame sem lar.",
            ("Melina", "falha"):
                "A polinização apressada deixou o jardim mais pobre do que Melina "
                "esperava -- o enxame que chega agora não encontra fartura nenhuma, "
                "só uma colônia já cansada.",
            ("Nectar", "super_sucesso"):
                "A nova rota de voo testada por Nectar funcionou tão bem que abelhas "
                "de fora começaram a segui-la -- foi assim que o enxame errante "
                "encontrou o caminho até aqui.",
            ("Nectar", "sucesso"):
                "A rota experimental de Nectar deixou um rastro de feromônio pelo ar "
                "-- não perfeito, mas o bastante pra guiar um enxame perdido até a "
                "colmeia.",
            ("Nectar", "falha"):
                "O experimento de rota de Nectar não deu em nada além de abelhas "
                "confusas -- o enxame que chega agora encontrou a colmeia por puro "
                "acaso, não por causa de nada que a colônia fez.",
            ("Aurora", "super_sucesso"):
                "A aliança que Aurora fechou com o jardineiro deixou a região tão "
                "acolhedora que a notícia se espalhou rápido -- foi assim que um "
                "enxame sem lar soube que havia espaço aqui.",
            ("Aurora", "sucesso"):
                "A negociação de Aurora garantiu um cantinho seguro no jardim -- "
                "pequeno, mas o suficiente pra um enxame errante notar e se "
                "interessar.",
            ("Aurora", "falha"):
                "A conversa com o jardineiro não rendeu o espaço que Aurora esperava "
                "-- o enxame que aparece agora chega sem saber que já houve uma "
                "tentativa de acolhida ali.",
        },
        "fator_custo": {"super_sucesso": 0.5, "sucesso": 1.0, "falha": 1.5},
        "moedas_afetadas": ["mel", "operarias"],
        "notas": {
            "super_sucesso":
                "Graças ao que aconteceu no Jardim, esta escolha saiu mais barata: "
                "você pagaria {mel_normal} de mel e pagou só {mel_final} (economia "
                "de {mel_diferenca}).",
            "sucesso":
                "O Jardim não mudou nada aqui: esta escolha custou o valor de "
                "sempre, {mel_final} de mel.",
            "falha":
                "Por causa do que aconteceu no Jardim, esta escolha saiu mais cara: "
                "você pagaria {mel_normal} de mel e pagou {mel_final} "
                "({mel_diferenca} a mais).",
        },
    },
}

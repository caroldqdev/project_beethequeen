# -*- coding: utf-8 -*-
"""
PONTE: Evento 1 (O Novo Jardim) -> Evento 2 (Enxame Errante).

Este arquivo descreve o que muda no EVENTO 2 por causa do que aconteceu
no EVENTO 1 -- quem foi a conselheira escolhida e como foi o minigame dela
('super_sucesso' | 'sucesso' | 'falha'). Ele tem 3 partes:

  1) TEXTO     'variants'  -> a frase que SUBSTITUI o texto de abertura
                              do Evento 2.
  2) DESCONTO  'cost_factor' + 'scale_resources'
                           -> quanto o custo da escolha feita no Evento 2
                              muda (0.5 = metade, 1.0 = normal,
                              1.5 = 50% a mais) e em quais moedas.
                              So atua em custos, nunca em ganhos.
  3) VISUAL    'notes'     -> a frase na tela de resultado do minigame do
                              Evento 2, explicando o desconto. Pode usar
                              estes campos (sempre sem sinal):
                                {mel_normal}  {mel_final}  {mel_diferenca}
                              ("normal" = quanto seria pago sem o desconto,
                              "final" = quanto foi pago de verdade).
                              Troque 'mel' por 'operarias' ou 'relacao'
                              para as outras moedas.

Quem le este arquivo e o main.py (ele importa esta ponte no topo e
registra na lista BRIDGES).
"""

RESULT = {
    "for_event_id": 2,   # o evento que RECEBE o efeito

    # ---------------------------------------------------------- 1) TEXTO
    "variants": {
        ("Flora", "super_sucesso"):
            "O jardim recém-mapeado por Flora virou um verdadeiro mosaico de espécies -- "
            "não é à toa que o enxame errante escolheu pousar bem ali perto, atraído pela "
            "diversidade que a colônia ajudou a manter.",
        ("Flora", "sucesso"):
            "O cuidado de Flora com o jardim deixou um rastro de flores variadas pela "
            "região -- talvez seja por isso que o enxame decidiu se aproximar da colmeia.",
        ("Flora", "falha"):
            "Mesmo com boas intenções, o mapeamento não rendeu o refúgio florido que Flora "
            "esperava -- o enxame que aparece agora encontra pouco além do que já havia antes.",

        ("Melina", "super_sucesso"):
            "A polinização acelerada de Melina lotou os arredores de mel disponível -- e "
            "foi essa fartura que atraiu o enxame errante até a porta da colmeia.",
        ("Melina", "sucesso"):
            "A pressa de Melina rendeu fartura no jardim, mesmo à custa de alguma bagunça -- "
            "fartura o bastante pra chamar a atenção de um enxame sem lar.",
        ("Melina", "falha"):
            "A polinização apressada deixou o jardim mais pobre do que Melina esperava -- o "
            "enxame que chega agora não encontra fartura nenhuma, só uma colônia já cansada.",

        ("Nectar", "super_sucesso"):
            "A nova rota de voo testada por Nectar funcionou tão bem que abelhas de fora "
            "começaram a segui-la -- foi assim que o enxame errante encontrou o caminho até "
            "aqui.",
        ("Nectar", "sucesso"):
            "A rota experimental de Nectar deixou um rastro de feromônio pelo ar -- não "
            "perfeito, mas o bastante pra guiar um enxame perdido até a colmeia.",
        ("Nectar", "falha"):
            "O experimento de rota de Nectar não deu em nada além de abelhas confusas -- o "
            "enxame que chega agora encontrou a colmeia por puro acaso, não por causa de "
            "nada que a colônia fez.",

        ("Aurora", "super_sucesso"):
            "A aliança que Aurora fechou com o jardineiro deixou a região tão acolhedora "
            "que a notícia se espalhou rápido -- foi assim que um enxame sem lar soube que "
            "havia espaço aqui.",
        ("Aurora", "sucesso"):
            "A negociação de Aurora garantiu um cantinho seguro no jardim -- pequeno, mas o "
            "suficiente pra um enxame errante notar e se interessar.",
        ("Aurora", "falha"):
            "A conversa com o jardineiro não rendeu o espaço que Aurora esperava -- o "
            "enxame que aparece agora chega sem saber que já houve uma tentativa de "
            "acolhida ali.",
    },

    # ------------------------------------------------------- 2) DESCONTO
    "cost_factor": {
        "super_sucesso": 0.5,
        "sucesso": 1.0,
        "falha": 1.5,
    },
    "scale_resources": ["mel", "operarias"],

    # -------------------------------------------------------- 3) VISUAL
    "notes": {
        "super_sucesso": "Graças ao que aconteceu no Jardim, esta escolha saiu mais barata: "
                         "você pagaria {mel_normal} de mel e pagou só {mel_final} "
                         "(economia de {mel_diferenca}).",
        "sucesso": "O Jardim não mudou nada aqui: esta escolha custou o valor de sempre, "
                   "{mel_final} de mel.",
        "falha": "Por causa do que aconteceu no Jardim, esta escolha saiu mais cara: "
                 "você pagaria {mel_normal} de mel e pagou {mel_final} "
                 "({mel_diferenca} a mais).",
    },
}
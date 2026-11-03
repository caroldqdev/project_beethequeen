# -*- coding: utf-8 -*-
"""
Resultado da transicao Evento 1 (O Novo Jardim) -> Evento 2 (Enxame Errante).

Isso e a "ponte" entre os dois eventos: dado quem foi a conselheira
escolhida e qual foi o resultado do minigame dela no Evento 1
('super_sucesso' | 'sucesso' | 'falha'), este arquivo decide:

  - 'variants'        -> qual frase substitui o 'context' padrao do
                          Evento 2 (a introducao que o jogador le antes
                          de escolher).
  - 'cost_factor'      -> por quanto multiplicar o custo da escolha do
                          jogador NO EVENTO 2 (0.5 = mais barato, 1.0 =
                          normal, 1.5 = mais caro). Revelado na tela de
                          resultado do minigame do Evento 2, nao antes.
  - 'scale_resources'  -> em quais recursos do 'cost' esse fator se
                          aplica (por enquanto so o que e de fato GASTO,
                          nunca o que e ganho).

Quem le este arquivo e game/orchestrator.py -- nunca o resto do jogo
direto. Para mudar so os numeros ou so as frases, mexa aqui; a regra de
COMO isso e aplicado mora no orchestrator.
"""

RESULT = {
    "for_event_id": 2,

    "variants": {
        ("Flora", "super_sucesso"):
            "O jardim recem-mapeado por Flora virou um verdadeiro mosaico de especies -- "
            "nao e a toa que o enxame errante escolheu pousar bem ali perto, atraido pela "
            "diversidade que a colonia ajudou a manter.",
        ("Flora", "sucesso"):
            "O cuidado de Flora com o jardim deixou um rastro de flores variadas pela "
            "regiao -- talvez seja por isso que o enxame decidiu se aproximar da colmeia.",
        ("Flora", "falha"):
            "Mesmo com boas intencoes, o mapeamento nao rendeu o refugio florido que Flora "
            "esperava -- o enxame que aparece agora encontra pouco alem do que ja havia antes.",

        ("Melina", "super_sucesso"):
            "A polinizacao acelerada de Melina lotou os arredores de mel disponivel -- e "
            "foi essa fartura que atraiu o enxame errante ate a porta da colmeia.",
        ("Melina", "sucesso"):
            "A pressa de Melina rendeu fartura no jardim, mesmo a custa de alguma bagunca -- "
            "fartura o bastante pra chamar a atencao de um enxame sem lar.",
        ("Melina", "falha"):
            "A polinizacao apressada deixou o jardim mais pobre do que Melina esperava -- o "
            "enxame que chega agora nao encontra fartura nenhuma, so uma colonia ja cansada.",

        ("Nectar", "super_sucesso"):
            "A nova rota de voo testada por Nectar funcionou tao bem que abelhas de fora "
            "comecaram a segui-la -- foi assim que o enxame errante encontrou o caminho ate "
            "aqui.",
        ("Nectar", "sucesso"):
            "A rota experimental de Nectar deixou um rastro de feromonio pelo ar -- nao "
            "perfeito, mas o bastante pra guiar um enxame perdido ate a colmeia.",
        ("Nectar", "falha"):
            "O experimento de rota de Nectar nao deu em nada alem de abelhas confusas -- o "
            "enxame que chega agora encontrou a colmeia por puro acaso, nao por causa de "
            "nada que a colonia fez.",

        ("Aurora", "super_sucesso"):
            "A alianca que Aurora fechou com o jardineiro deixou a regiao tao acolhedora "
            "que a noticia se espalhou rapido -- foi assim que um enxame sem lar soube que "
            "havia espaco aqui.",
        ("Aurora", "sucesso"):
            "A negociacao de Aurora garantiu um cantinho seguro no jardim -- pequeno, mas o "
            "suficiente pra um enxame errante notar e se interessar.",
        ("Aurora", "falha"):
            "A conversa com o jardineiro nao rendeu o espaco que Aurora esperava -- o "
            "enxame que aparece agora chega sem saber que ja houve uma tentativa de "
            "acolhida ali.",
    },

    "cost_factor": {
        "super_sucesso": 0.5,
        "sucesso": 1.0,
        "falha": 1.5,
    },

    "scale_resources": ["mel", "operarias"],
}
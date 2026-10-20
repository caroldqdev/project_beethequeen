# -*- coding: utf-8 -*-
"""A APRESENTAÇÃO DAS CONSELHEIRAS: o texto da tela de cada uma.

  titulo        a linha de baixo do nome ("Guardiã da ...")
  lema          a frase entre aspas (as aspas o jogo coloca)
  apresentacao  o parágrafo que descreve a conselheira

A ORDEM em que elas aparecem na tela é a de ORDEM, em dados/conselheiras.py.
A cor, o emoji e a penalidade de falha de cada uma também estão lá.
O "Pressione ENTER..." do fim desta tela está em telas/textos.py (DICA_CONSELHEIRA).
Alinhamento, fonte, cor e posição destes textos: telas/estilos.py, card "conselheira".
"""

CONSELHEIRAS = {
    "Flora": {
        "titulo": "Guardiã da Biodiversidade",
        "lema": "Sem diversidade, não há futuro.",
        "apresentacao":
            "Pensa em décadas, não em estações. Prioriza reflorestamento e "
            "corredores ecológicos. Suas soluções são lentas, mas regenerativas.",
    },
    "Melina": {
        "titulo": "Guardiã da Produção",
        "lema": "O inverno sempre chega.",
        "apresentacao":
            "Prioriza reservas e produção hoje, não depois. Suas soluções são "
            "rápidas e pragmáticas, às vezes às custas do ecossistema e da confiança "
            "da colônia.",
    },
    "Nectar": {
        "titulo": "Guardiã da Inovação",
        "lema": "Quem evolui primeiro sobrevive.",
        "apresentacao":
            "Aposta em soluções novas, mesmo sem garantia. O investimento é sempre "
            "alto, e o retorno só aparece quando a ideia é posta à prova.",
    },
    "Aurora": {
        "titulo": "Guardiã da Cooperação",
        "lema": "Nenhuma colmeia floresce sozinha.",
        "apresentacao":
            "Acredita que alianças valem mais que recursos. Barata em recurso, cara "
            "em tempo e produção perdida, mas sempre fortalece a confiança da "
            "colmeia.",
    },
}

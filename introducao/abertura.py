# -*- coding: utf-8 -*-
"""A ABERTURA: os textos da primeira tela do jogo ("BEE THE QUEEN").

  titulo      o nome do jogo, grande
  subtitulo   a linha logo abaixo ("Ano 1")
  texto_1     o parágrafo de cima (quem é você)
  nomes       a linha em negrito com o nome das conselheiras
  texto_2     o parágrafo de baixo (como o jogo funciona)

Para quebrar a linha no meio de um texto, escreva \\n.
O "Pressione ENTER..." do fim desta tela está em telas/textos.py (DICA_ABERTURA).
Alinhamento, fonte, cor e posição destes textos: telas/estilos.py, card "abertura".
"""

ABERTURA = {
    "titulo": "BEE THE QUEEN",
    "subtitulo": "Ano 1",
    "texto_1":
        "A Rainha Anciã se aposenta e escolhe você como sucessora.\nVocê governa por "
        "4 estações, apoiada por quatro conselheiras:",
    "nomes": "Flora, Melina, Nectar e Aurora",
    "texto_2":
        "Cada escolha altera o painel de Harmonia da Colmeia, a Relação\ncom a "
        "Colmeia, consome recursos e muda a afinidade das\nconselheiras. Não existe "
        "final único! existe o reino que você constrói.",
}

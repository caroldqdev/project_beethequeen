ESPERA NAS TELAS DO JOGO -- a dica do ENTER só aparece depois de 10 segundos

1) SUBSTITUA estes 3 arquivos no seu projeto:
     main.py
     telas/minigame.py
     telas/final.py

2) NÃO precisa mudar o config.py: o jogo já usa 10 segundos e "o minigame só começa
   no ENTER" como padrão. Se quiser mudar, ACRESCENTE no config.py (seção 3, logo antes
   de "MOSTRAR_BARRA_DE_TEMPO"):

     ATRASO_DA_DICA_NO_JOGO = 10          # segundos até aparecer o "Pressione ENTER..."
     COMECAR_O_MINIGAME_SOZINHO = False   # True = o preparo conta e começa o jogo sozinho

O que muda no jogo:
  - Texto do evento, preparo, minigame (depois de terminar), resultado e consequência:
    a tela NÃO passa sozinha e o "Pressione ENTER..." só aparece depois de 10 s.
    O ENTER funciona a qualquer momento.
  - O preparo do minigame não conta mais 5 s nem começa o jogo sozinho: espera o ENTER.
  - Na introdução continua como antes (a dica aos 5 s, ATRASO_DA_DICA).

A INTRODUÇÃO NUM LUGAR SÓ (pasta introducao/)

1) COLOQUE na pasta do projeto a pasta introducao/ (3 arquivos novos):
     introducao/abertura.py        os textos da abertura
     introducao/conselheiras.py    título, lema e descrição de cada conselheira
     introducao/nova_rainha.py     os textos da Nova Rainha

2) SUBSTITUA estes 2 arquivos:
     catalogo.py
     telas/abertura.py
   (Se você acrescentou eventos na lista NOMES_DOS_EVENTOS do seu catalogo.py,
    copie essa lista para o catalogo.py novo.)

3) LIMPEZA (opcional; enquanto não fizer, o jogo avisa uma vez no terminal):
   - em dados/conselheiras.py, apague "titulo", "lema" e "apresentacao" de cada
     conselheira (ficam só emoji, cor, eixo e penalidade_falha)
   - em telas/textos.py, apague TITULO_DO_JOGO, SUBTITULO_DO_JOGO, ABERTURA_1,
     ABERTURA_CONSELHEIRAS, ABERTURA_2, NOVA_RAINHA_TITULO e NOVA_RAINHA_TEXTO
   ATENÇÃO: se você mudou algum desses textos nos lugares antigos depois de
   baixar o projeto, copie a mudança para introducao/ antes de apagar. O jogo
   passa a ler SÓ de introducao/.

SOB AS FOLHAS -- visual novo, com os desenhos do Aseprite

1) COLOQUE estes 2 arquivos na pasta minigames/jogos/ do projeto
   (o sob_as_folhas.py substitui o que já está lá; o aseprite.py é novo):
     sob_as_folhas.py
     aseprite.py

2) OS DESENHOS ficam na pasta assets/ (na raiz do projeto), com estes nomes:
     Folha.ase  Borboleta.ase  Joaninha.ase  Vespa.ase  Pernilongo.ase  Minhoca.ase
   Se algum faltar, estiver vazio ou estragado, o jogo avisa no terminal e usa um
   desenho provisório no lugar (não trava).

3) NÃO PRECISA mudar mais nada. A pasta antiga puzzles/ (se ainda existir no seu
   projeto) não é usada por nada: o arquivo que vale é minigames/jogos/sob_as_folhas.py.

4) PARA AJUSTAR: o começo do sob_as_folhas.py tem um painel de ajustes
   (tamanho da folha e dos bichos, quantas folhas, tempo, escurecer as camadas de baixo,
   sombra, girar os bichos...).

5) O aseprite.py lê o .ase do jeito que ele sai do Aseprite: dá pra editar o desenho
   lá, salvar, e o jogo usa a versão nova na próxima vez que abrir. Camadas escondidas
   no Aseprite não aparecem no jogo.

# -*- coding: utf-8 -*-
"""
JOGA O JOGO INTEIRO SOZINHO, de várias maneiras, e confere que nada quebra.

Rode depois de qualquer mudança (um evento novo, um texto, um número):

    python testes/jogar_tudo.py

Ele abre o jogo numa janela invisível, joga do começo ao fim escolhendo cada
conselheira com cada resultado de minigame (sucesso, parcial, falha), mais 50
partidas aleatórias, e DESENHA cada tela do caminho. Se um arquivo de evento
tiver um erro, ou uma tela não souber desenhar algo, o erro aparece aqui.
"""
import itertools
import os
import random
import sys
import time

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")      # janela invisível
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config
import catalogo
import main
from telas import desenho

RESULTADOS_DO_MINIGAME = ("sucesso", "parcial", "falha")


def jogar(escolher_opcao, resultado_do_minigame):
    """Uma partida inteira. `escolher_opcao(jogo)` devolve o índice da opção;
    `resultado_do_minigame(jogo)` devolve 'sucesso', 'parcial' ou 'falha'."""
    jogo = main.Jogo()
    telas_vistas = set()
    passos = 0
    while jogo.tela != config.FINAL:
        passos += 1
        if passos > 5000:
            raise RuntimeError(f"o jogo travou na tela {jogo.tela!r}, evento {jogo.evento['id']}")
        desenho.desenhar(jogo.visual, jogo, (0, 0))        # a tela precisa saber se desenhar
        telas_vistas.add(jogo.tela)
        tela = jogo.tela
        if tela in config.TELAS_QUE_AVANCAM:
            jogo.avancar_tela()
        elif tela == config.ESCOLHA:
            jogo.escolher(jogo.evento["opcoes"][escolher_opcao(jogo)])
        elif tela == config.PREPARO:
            jogo.iniciar_minigame()
        elif tela == config.MINIGAME:
            jogo.minigame.done = True
            jogo.minigame.result = resultado_do_minigame(jogo)
            jogo.concluir_escolha(jogo.minigame.effect_multiplier())
        elif tela == config.RESULTADO_DO_MINIGAME:
            jogo.tela = config.CONSEQUENCIA
        elif tela == config.CONSEQUENCIA:
            jogo.proximo_evento()
    desenho.desenhar(jogo.visual, jogo, (0, 0))            # a tela final
    telas_vistas.add(jogo.tela)
    return jogo, telas_vistas


def main_do_teste():
    inicio = time.time()
    catalogo.verificar()
    print(f"catálogo conferido: {len(catalogo.EVENTOS)} eventos, cada um com evento + minigame + resultado\n")

    partidas = []
    # 1) sempre a mesma conselheira, com cada resultado de minigame
    for conselheira, resultado in itertools.product(("Flora", "Melina", "Nectar", "Aurora"), RESULTADOS_DO_MINIGAME):
        def escolher(jogo, c=conselheira):
            return [o["conselheira"] for o in jogo.evento["opcoes"]].index(c)
        partidas.append((f"sempre {conselheira}, minigame {resultado}", escolher, lambda jogo, r=resultado: r))
    # 2) partidas aleatórias
    for semente in range(50):
        sorteio = random.Random(semente)
        partidas.append((f"aleatória #{semente}",
                         lambda jogo, s=sorteio: s.randrange(len(jogo.evento["opcoes"])),
                         lambda jogo, s=sorteio: s.choice(RESULTADOS_DO_MINIGAME)))

    todas_as_telas = set()
    for nome, escolher, resultado in partidas:
        jogo, telas = jogar(escolher, resultado)
        todas_as_telas |= telas
        e = jogo.estado
        if nome.startswith("sempre") or nome.endswith("#0"):
            print(f"  {nome:34s} -> mel {e.mel:>3}  operárias {e.operarias:>3}  relação {e.relacao:>3}")
    print(f"\n{len(partidas)} partidas jogadas até a tela final, sem nenhum erro")
    print(f"telas desenhadas: {len(todas_as_telas)} -> {', '.join(sorted(todas_as_telas))}")
    print(f"tempo: {time.time() - inicio:.1f}s")


if __name__ == "__main__":
    main_do_teste()

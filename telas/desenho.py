# -*- coding: utf-8 -*-
"""O ROTEADOR DAS TELAS: dado qual tela o jogo está mostrando, chama a função
que a desenha. Para uma tela nova: escreva a função (em abertura.py,
evento.py, minigame.py ou final.py) e acrescente uma linha aqui."""
import pygame

import config
from telas import abertura, evento, minigame, final
from telas.componentes import barra_de_tempo


def desenhar(v, j, mouse):
    """Desenha a tela atual do jogo `j` (o que o main.py mantém)."""
    v.desenhar_fundo()
    tela = j.tela
    if tela == config.ABERTURA:
        abertura.abertura(v, j)
    elif tela == config.CONSELHEIRA:
        abertura.conselheira(v, j)
    elif tela == config.NOVA_RAINHA:
        abertura.nova_rainha(v, j)
    elif tela == config.ESTACAO:
        abertura.estacao(v, j)
    elif tela == config.CONTEXTO:
        evento.contexto(v, j)
    elif tela == config.ESCOLHA:
        evento.escolha(v, j, mouse)
    elif tela == config.PREPARO:
        minigame.preparo(v, j)
    elif tela == config.MINIGAME:
        minigame.jogo(v, j)
    elif tela == config.RESULTADO_DO_MINIGAME:
        minigame.resultado_do_minigame(v, j)
    elif tela == config.CONSEQUENCIA:
        final.consequencia(v, j)
    elif tela == config.FINAL:
        final.final(v, j)
    if config.MOSTRAR_BARRA_DE_TEMPO:
        barra_de_tempo(v, j)
    pygame.display.flip()

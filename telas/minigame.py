# -*- coding: utf-8 -*-
"""AS TELAS DO MINIGAME: o preparo (a contagem e a instrução), o jogo em si e o
resultado dele. (O jogo desenha a si mesmo, dentro da moldura, em minigames/jogos/.)

Onde mudar o quê:
  - a posição de cada coisa ............ telas/layout.py
  - o alinhamento, o padding, a fonte e a cor de cada texto ... telas/estilos.py ("o CSS")
  - o que está escrito ................. telas/textos.py (e a instrução, em minigames/jogos/)
"""
import math

import pygame

import config
from config import LARGURA
from telas import layout as L, textos
from telas.componentes import (painel, linha, paragrafo, card_de_texto, dica_aparece,
                               linhas_de_efeitos, linhas_de_custos)


def preparo(v, j):
    caixa = L.retangulo(L.PAINEL_PREPARO)
    painel(v.tela, caixa)

    def conteudo():
        linha(v, textos.PREPARO_TITULO.format(nome=j.nome_do_minigame), "preparo", "titulo", caixa, L.PREPARO_TITULO_Y)
        proposta = textos.PROPOSTA.format(conselheira=j.opcao["conselheira"], acao=j.opcao["acao"])
        paragrafo(v, proposta, "preparo", "proposta", L.retangulo(L.PREPARO_PROPOSTA))
        paragrafo(v, j.instrucao_do_minigame, "preparo", "instrucao", L.retangulo(L.PREPARO_INSTRUCAO))
        if getattr(config, "COMECAR_O_MINIGAME_SOZINHO", False):      # a contagem só existe se o jogo começa sozinho
            segundos = max(1, math.ceil(j.tempo_de_preparo))
            linha(v, str(segundos), "preparo", "contagem", caixa, L.PREPARO_CONTAGEM_Y)
        if dica_aparece(v, j):
            linha(v, textos.DICA_PREPARO, "preparo", "dica", caixa, L.PREPARO_DICA_Y)

    card_de_texto(v, "preparo", caixa, conteudo)
    v.abelha(L.ABELHA_NO_PREPARO)


def jogo(v, j):
    caixa = L.retangulo(L.PAINEL_MINIGAME)
    painel(v.tela, caixa)
    nome = j.minigame.name if j.minigame is not None else textos.MINIGAME_SEM_JOGO

    def conteudo():
        linha(v, textos.MINIGAME_TITULO.format(nome=nome), "minigame", "titulo", caixa, L.MINIGAME_TITULO_Y)
        proposta = textos.PROPOSTA.format(conselheira=j.opcao["conselheira"], acao=j.opcao["acao"])
        paragrafo(v, proposta, "minigame", "proposta", L.retangulo(L.MINIGAME_PROPOSTA))
        if j.minigame is not None and not v.medindo:
            j.minigame.draw(v.tela)           # o jogo em si não se mexe (e a dica vai POR CIMA dele)
        if j.minigame is not None and j.minigame.done and dica_aparece(v, j):
            linha(v, textos.DICA_MINIGAME, "minigame", "dica", caixa, L.MINIGAME_DICA_Y)

    card_de_texto(v, "minigame", caixa, conteudo)
    v.abelha(L.ABELHA_NO_MINIGAME)


def resultado_do_minigame(v, j):
    resolucao = j.resolucao
    p = L.retangulo(L.PAINEL_RESULTADO_DO_MINIGAME)
    painel(v.tela, p)
    resultado = j.minigame.result if j.minigame is not None else "sucesso"
    porcentagem = int(round(j.minigame.effect_multiplier() * 100)) if j.minigame is not None else 100
    m = L.RESULTADO_MARGEM

    def conteudo():
        linha(v, textos.RESULTADO_TITULO[resultado], "resultado_do_minigame", "titulo", p,
              p.top + L.RESULTADO_TITULO_DO_TOPO, cor_automatica=L.COR_RESULTADO[resultado])
        linha(v, textos.RESULTADO_DETALHE[resultado].format(pct=porcentagem), "resultado_do_minigame", "detalhe", p,
              p.top + L.RESULTADO_DETALHE_DO_TOPO)

        y = p.top + L.RESULTADO_TEXTOS_DO_TOPO

        def bloco(y):
            return pygame.Rect(p.left + m, y, p.width - 2 * m, L.RESULTADO_LINHA_ALTURA)

        efeitos = "   ".join(linhas_de_efeitos(resolucao)) if resolucao.efeitos else textos.RESULTADO_SEM_EFEITOS
        y = paragrafo(v, textos.RESULTADO_EFEITOS.format(linhas=efeitos), "resultado_do_minigame", "efeitos", bloco(y))
        y += 6
        if resolucao.custos:
            y = paragrafo(v, textos.RESULTADO_CUSTO.format(linhas="   ".join(linhas_de_custos(resolucao))),
                          "resultado_do_minigame", "custo", bloco(y))
            y += 6
        if resolucao.nota_da_ponte:
            y = paragrafo(v, resolucao.nota_da_ponte, "resultado_do_minigame", "nota", bloco(y))
            y += 10
        if resolucao.penalidade:
            paragrafo(v, textos.RESULTADO_PENALIDADE.format(conselheira=j.opcao["conselheira"],
                                                            texto=resolucao.penalidade),
                      "resultado_do_minigame", "penalidade", bloco(y))
        if dica_aparece(v, j):
            linha(v, textos.DICA_RESULTADO_DO_MINIGAME, "resultado_do_minigame", "dica", p,
                  p.bottom - L.RESULTADO_DICA_DA_BASE, ancora_y="topo")

    card_de_texto(v, "resultado_do_minigame", p, conteudo)
    v.abelha((p.right + L.ABELHA_DO_PAINEL[0], p.top + L.ABELHA_DO_PAINEL[1]))

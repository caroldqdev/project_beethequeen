# -*- coding: utf-8 -*-
"""AS TELAS DE APRESENTAÇÃO: a abertura, cada conselheira, A Nova Rainha e o
cartão da estação.

Onde mudar o quê:
  - a posição de cada coisa ............ telas/layout.py
  - o alinhamento, o padding, a fonte e a cor de cada texto ... telas/estilos.py ("o CSS")
  - o que está escrito ................. introducao/ (abertura.py, conselheiras.py, nova_rainha.py);
                                         as dicas "Pressione ENTER..." estão em telas/textos.py
"""
import pygame

import catalogo
from config import LARGURA, ALTURA
from dados.conselheiras import CONSELHEIRAS, ORDEM
from telas import layout as L, textos
from telas.componentes import (painel, linha, linha_com_emoji, paragrafo, card_de_texto, dica_aparece)


def abertura(v, j):
    caixa = L.retangulo(L.PAINEL_APRESENTACAO)
    painel(v.tela, caixa)
    intro = catalogo.INTRODUCAO["abertura"]          # os textos: introducao/abertura.py

    def conteudo():
        linha(v, intro["titulo"], "abertura", "titulo", caixa, L.ABERTURA_TITULO_Y)
        linha(v, intro["subtitulo"], "abertura", "subtitulo", caixa, L.ABERTURA_SUBTITULO_Y)
        margem = L.ABERTURA_TEXTO_MARGEM
        largura = LARGURA - 2 * margem
        y = L.ABERTURA_TEXTO_Y
        y = paragrafo(v, intro["texto_1"], "abertura", "texto_1",
                      pygame.Rect(margem, y, largura, L.ABERTURA_TEXTO_1_ALTURA))
        y = paragrafo(v, intro["nomes"], "abertura", "nomes",
                      pygame.Rect(margem, y, largura, L.ABERTURA_CONSELHEIRAS_ALTURA))
        y += L.ABERTURA_ESPACO_ANTES_DO_ULTIMO
        # a dica faz parte deste bloco; antes da hora ela vira uma linha em branco,
        # assim o resto do texto não "pula" quando ela aparece
        dica = textos.DICA_ABERTURA if dica_aparece(v, j) else " "
        paragrafo(v, intro["texto_2"] + "\n\n" + dica, "abertura", "texto_2",
                  pygame.Rect(margem, y, largura, L.ABERTURA_TEXTO_2_ALTURA))

    card_de_texto(v, "abertura", caixa, conteudo)
    v.abelha(L.ABELHA_NA_ABERTURA)


def conselheira(v, j):
    nome = ORDEM[j.indice_conselheira]
    dados = CONSELHEIRAS[nome]                       # cor, emoji, penalidade: dados/conselheiras.py
    intro = catalogo.INTRODUCAO["conselheiras"][nome]    # os textos: introducao/conselheiras.py
    caixa = L.retangulo(L.PAINEL_APRESENTACAO)
    painel(v.tela, caixa)

    def conteudo():
        linha_com_emoji(v, nome, dados, v.emojis.get(nome), "conselheira", "nome", caixa, L.CONSELHEIRA_NOME_Y)
        linha(v, intro["titulo"], "conselheira", "titulo", caixa, L.CONSELHEIRA_TITULO_Y)
        linha(v, f'"{intro["lema"]}"', "conselheira", "lema", caixa, L.CONSELHEIRA_LEMA_Y)
        paragrafo(v, intro["apresentacao"], "conselheira", "texto", L.retangulo(L.CONSELHEIRA_TEXTO))
        if dica_aparece(v, j):
            linha(v, textos.DICA_CONSELHEIRA, "conselheira", "dica", caixa, L.CONSELHEIRA_DICA_Y)

    card_de_texto(v, "conselheira", caixa, conteudo)
    v.abelha(L.ABELHA_NA_CONSELHEIRA)


def nova_rainha(v, j):
    caixa = L.retangulo(L.PAINEL_APRESENTACAO)
    painel(v.tela, caixa)
    intro = catalogo.INTRODUCAO["nova_rainha"]       # os textos: introducao/nova_rainha.py

    def conteudo():
        linha(v, intro["titulo"], "nova_rainha", "titulo", caixa, L.NOVA_RAINHA_TITULO_Y)
        paragrafo(v, intro["texto"], "nova_rainha", "texto", L.retangulo(L.NOVA_RAINHA_TEXTO))
        if dica_aparece(v, j):
            linha(v, textos.DICA_NOVA_RAINHA, "nova_rainha", "dica", caixa, L.NOVA_RAINHA_DICA_Y)

    card_de_texto(v, "nova_rainha", caixa, conteudo)
    v.abelha(L.ABELHA_NA_ABERTURA)


def estacao(v, j):
    veu = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
    veu.fill(L.VEU_ESCURO)
    v.tela.blit(veu, (0, 0))
    tela = pygame.Rect(0, 0, LARGURA, ALTURA)        # (esta tela não tem card: alinha na tela toda)
    nome = textos.NOMES_DAS_ESTACOES.get(j.estacao_atual, j.estacao_atual).upper()

    def conteudo():
        linha(v, nome, "estacao", "nome", tela, L.ESTACAO_NOME_Y)
        if dica_aparece(v, j):
            linha(v, textos.DICA_ESTACAO, "estacao", "dica", tela, L.ESTACAO_DICA_Y)

    card_de_texto(v, "estacao", tela, conteudo)

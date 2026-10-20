# -*- coding: utf-8 -*-
"""AS TELAS DO EVENTO: o texto de abertura e a escolha (os 4 cards).

Onde mudar o quê:
  - a posição de cada coisa ............ telas/layout.py
  - o alinhamento, o padding, a fonte e a cor de cada texto ... telas/estilos.py ("o CSS")
  - o que está escrito ................. telas/textos.py, e o texto de cada evento em eventos/
"""
import pygame

from config import LARGURA, ALTURA
from dados.conselheiras import CONSELHEIRAS
from telas import layout as L, textos
from telas.componentes import hud, painel, linha, paragrafo, card_de_texto, dica_aparece


def _nome_da_estacao(evento):
    return textos.NOMES_DAS_ESTACOES.get(evento["estacao"], evento["estacao"])


def contexto(v, j):
    evento = j.evento
    hud(v, j.estado)
    p = L.retangulo(L.PAINEL_CONTEXTO)
    painel(v.tela, p)
    m = L.CONTEXTO_MARGEM

    def conteudo():
        cabecalho = textos.CABECALHO_DO_EVENTO.format(
            estacao=_nome_da_estacao(evento), id=evento["id"], titulo=evento["titulo"])
        linha(v, cabecalho, "contexto", "cabecalho", p, p.top + L.CONTEXTO_TITULO_DO_TOPO, ancora_y="topo")
        paragrafo(v, j.texto_de_abertura(), "contexto", "texto",
                  pygame.Rect(p.left + m, p.top + L.CONTEXTO_TEXTO_TOPO, p.width - 2 * m, L.CONTEXTO_TEXTO_ALTURA))
        if dica_aparece(v, j):
            linha(v, textos.DICA_CONTEXTO, "contexto", "dica", p, p.bottom - L.CONTEXTO_DICA_DA_BASE, ancora_y="topo")

    card_de_texto(v, "contexto", p, conteudo)
    v.abelha((p.right - L.CONTEXTO_ABELHA_DA_DIREITA, p.bottom - L.CONTEXTO_ABELHA_DA_BASE))


def _texto_do_custo(custo):
    """A linha de preço do card: 'Mel -15  Relação +3'."""
    partes = []
    if custo.get("mel"):
        partes.append(textos.CARD_CUSTO_MEL_TUDO if custo["mel"] == "tudo"
                      else textos.CARD_CUSTO_MEL.format(valor=custo["mel"]))
    if custo.get("operarias"):
        partes.append(textos.CARD_CUSTO_OPERARIAS.format(valor=custo["operarias"]))
    if custo.get("relacao"):
        partes.append(textos.CARD_CUSTO_RELACAO.format(valor=custo["relacao"]))
    return "  ".join(partes) if partes else textos.CARD_SEM_CUSTO


def escolha(v, j, mouse):
    evento = j.evento
    hud(v, j.estado)
    tela = pygame.Rect(0, 0, LARGURA, ALTURA)
    linha(v, textos.CABECALHO_DA_ESCOLHA.format(titulo=evento["titulo"]), "escolha", "titulo", tela, L.ESCOLHA_TITULO_Y)

    for opcao, card in zip(evento["opcoes"], L.retangulos_dos_cards(len(evento["opcoes"]))):
        cor_da_conselheira = CONSELHEIRAS[opcao["conselheira"]]["cor"]
        fundo = L.COR_CARD_COM_MOUSE if card.collidepoint(mouse) else L.COR_CARD
        pygame.draw.rect(v.tela, fundo, card, border_radius=L.CARD_RAIO)
        pygame.draw.rect(v.tela, cor_da_conselheira, card, 3, border_radius=L.CARD_RAIO)
        m = L.CARD_MARGEM
        linha(v, opcao["conselheira"], "escolha", "card_nome", card, card.top + L.CARD_NOME_TOPO,
              ancora_y="topo", cor_automatica=cor_da_conselheira)
        linha(v, _texto_do_custo(opcao["custo"]), "escolha", "card_custo", card, card.top + L.CARD_CUSTO_TOPO,
              ancora_y="topo")
        paragrafo(v, opcao["acao"], "escolha", "card_acao",
                  pygame.Rect(card.left + m, card.top + L.CARD_ACAO_TOPO, card.width - 2 * m, L.CARD_ACAO_ALTURA))

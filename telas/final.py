# -*- coding: utf-8 -*-
"""A CONSEQUÊNCIA do evento e a TELA FINAL (o legado da colmeia)."""
import pygame

import catalogo
import config
import regras
from config import LARGURA
from dados.conselheiras import CONSELHEIRAS
from dados.perfis import PERFIS, MENSAGEM_ECOLOGIA
from telas import layout as L, textos
from telas.componentes import (painel, texto, escrever, radar, hud, linhas_de_efeitos, linha, paragrafo,
                               card_de_texto)


def consequencia(v, j):
    evento, resolucao = j.evento, j.resolucao
    hud(v, j.estado)
    p = L.retangulo(L.PAINEL_CONSEQUENCIA)
    painel(v.tela, p)
    m = L.CONSEQUENCIA_MARGEM

    def conteudo():
        linha(v, textos.CONSEQUENCIA_TITULO.format(titulo=evento["titulo"]), "consequencia", "titulo", p,
              p.top + L.CONSEQUENCIA_TITULO_DO_TOPO, ancora_y="topo")
        y = p.top + L.CONSEQUENCIA_TEXTO_DO_TOPO
        if not j.teve_minigame:
            # escolha sem minigame (ação direta): os efeitos ainda não apareceram em outra tela
            efeitos = "   ".join(linhas_de_efeitos(resolucao)) if resolucao.efeitos else textos.RESULTADO_SEM_EFEITOS
            linha(v, textos.CONSEQUENCIA_EFEITOS.format(linhas=efeitos), "consequencia", "efeitos", p, y,
                  ancora_y="topo")
            y += 40
        largura = p.width - 2 * m
        if resolucao.extra:
            y = paragrafo(v, resolucao.extra, "consequencia", "extra",
                          pygame.Rect(p.left + m, y, largura, L.CONSEQUENCIA_EXTRA_ALTURA))
            y += 6
        paragrafo(v, catalogo.RESULTADOS[evento["id"]]["consequencia"], "consequencia", "texto",
                  pygame.Rect(p.left + m, y, largura, L.CONSEQUENCIA_TEXTO_ALTURA))
        if regras.harmonia_desequilibrada(j.estado):
            paragrafo(v, textos.AVISO_DE_DESEQUILIBRIO, "consequencia", "aviso",
                      pygame.Rect(p.left + m, p.bottom - L.CONSEQUENCIA_AVISO_DA_BASE, largura,
                                  L.CONSEQUENCIA_AVISO_ALTURA))
        linha(v, textos.DICA_CONSEQUENCIA, "consequencia", "dica", p, p.bottom - L.CONSEQUENCIA_DICA_DA_BASE,
              ancora_y="topo")

    card_de_texto(v, "consequencia", p, conteudo)
    v.abelha((p.right - L.CONSEQUENCIA_ABELHA_DA_DIREITA, p.top + L.ABELHA_DO_PAINEL[1]))


def final(v, j):
    estado = j.estado
    p = L.retangulo(L.PAINEL_FINAL)
    painel(v.tela, p)
    escrever(v, textos.FINAL_TITULO, "titulo", L.ESCURO, centro=(LARGURA // 2, p.top + L.FINAL_TITULO_DO_TOPO))
    radar(v.tela, (p.left + L.FINAL_RADAR_CENTRO[0], p.top + L.FINAL_RADAR_CENTRO[1]), L.FINAL_RADAR_RAIO,
          estado.harmonia, v.fontes["pequena"])

    x = p.left + L.FINAL_COLUNA_X
    y = p.top + L.FINAL_COLUNA_TOPO
    escrever(v, textos.FINAL_RECURSOS, "subtitulo", L.ESCURO, canto=(x, y))
    y += 26
    escrever(v, textos.HUD_MEL.format(valor=estado.mel), "pequena", L.ESCURO, canto=(x, y))
    y += 20
    escrever(v, textos.HUD_OPERARIAS.format(valor=estado.operarias), "pequena", L.ESCURO, canto=(x, y))
    y += 20
    escrever(v, textos.HUD_RELACAO.format(valor=estado.relacao), "pequena", L.ESCURO, canto=(x, y))
    y += 30

    escrever(v, textos.FINAL_AFINIDADE, "subtitulo", L.ESCURO, canto=(x, y))
    y += 24
    for nome, dados in CONSELHEIRAS.items():
        valor = estado.afinidade[nome]
        if valor >= config.AFINIDADE_ALIADA:
            situacao = textos.FINAL_SITUACAO["aliada"]
        elif valor <= config.AFINIDADE_AFASTADA:
            situacao = textos.FINAL_SITUACAO["afastada"]
        else:
            situacao = textos.FINAL_SITUACAO["neutra"]
        escrever(v, textos.FINAL_LINHA_DE_AFINIDADE.format(nome=nome, valor=valor, situacao=situacao),
                 "pequena", dados["cor"], canto=(x, y))
        y += 18

    perfil = regras.perfil_dominante(estado)
    y += 8
    escrever(v, textos.FINAL_PERFIL.format(nome=perfil), "subtitulo", L.DOURADO, canto=(x, y))
    y += 24
    texto(v, PERFIS[perfil], pygame.Rect(x, y, p.width - (x - p.left) - 24, L.FINAL_PERFIL_TEXTO_ALTURA), "pequena")

    caixa = pygame.Rect(p.left + L.CAIXA_ECOLOGIA_MARGEM, p.bottom - L.CAIXA_ECOLOGIA_DA_BASE,
                        p.width - 2 * L.CAIXA_ECOLOGIA_MARGEM, L.CAIXA_ECOLOGIA_ALTURA)
    pygame.draw.rect(v.tela, L.COR_CAIXA_ECOLOGIA, caixa, border_radius=10)
    pygame.draw.rect(v.tela, L.DOURADO, caixa, 2, border_radius=10)
    texto(v, MENSAGEM_ECOLOGIA, pygame.Rect(caixa.left + 14, caixa.top + 10, caixa.width - 28, caixa.height - 20),
          "pequena", L.COR_TEXTO_ECOLOGIA, espaco=3)

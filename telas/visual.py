# -*- coding: utf-8 -*-
"""
O VISUAL: a janela, as fontes e as imagens que todas as telas usam.
(As fontes se ajustam em config.py; as imagens estão em assets/.)
"""
import os
import pygame

import config
from dados.conselheiras import CONSELHEIRAS
from telas import layout

PASTA_DE_IMAGENS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")


class Visual:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(config.TITULO_DA_JANELA)
        self.tela = pygame.display.set_mode((config.LARGURA, config.ALTURA))
        self.relogio = pygame.time.Clock()
        # usados pelos cards de escrita (veja componentes.card_de_texto): quando
        # `medindo`, o texto não é desenhado, só medido (em `tinta`); depois ele é
        # desenhado já deslocado em `deslocamento_y`
        self.medindo = False
        self.tinta = None
        self.deslocamento_y = 0

        self.fontes = {nome: pygame.font.SysFont(familia, tamanho, bold=negrito)
                       for nome, (familia, tamanho, negrito) in config.FONTES.items()}

        fundo = pygame.image.load(os.path.join(PASTA_DE_IMAGENS, "bg_scene.png")).convert()
        self.fundo = pygame.transform.scale(fundo, (config.LARGURA, config.ALTURA))

        self.quadros_da_abelha = []
        for i in range(9):
            imagem = pygame.image.load(os.path.join(PASTA_DE_IMAGENS, f"bee_frame_{i}.png")).convert_alpha()
            self.quadros_da_abelha.append(pygame.transform.scale(imagem, (96, 96)))
        self.quadro_atual = 0
        self._tempo_do_quadro = 0.0

        # um emoji por conselheira (imagem: o pygame não desenha emoji de fonte)
        self.emojis = {}
        for nome, dados in CONSELHEIRAS.items():
            caminho = os.path.join(PASTA_DE_IMAGENS, "emoji", dados["arquivo_emoji"])
            if os.path.isfile(caminho):
                imagem = pygame.image.load(caminho).convert_alpha()
                self.emojis[nome] = pygame.transform.smoothscale(
                    imagem, (config.EMOJI_TAMANHO, config.EMOJI_TAMANHO))

    def atualizar(self, dt):
        """Chamado a cada quadro: faz a abelha bater as asas."""
        self._tempo_do_quadro += dt
        if self._tempo_do_quadro >= config.ABELHA_SEGUNDOS_POR_QUADRO:
            self._tempo_do_quadro = 0.0
            self.quadro_atual = (self.quadro_atual + 1) % len(self.quadros_da_abelha)

    def abelha(self, posicao):
        self.tela.blit(self.quadros_da_abelha[self.quadro_atual], posicao)

    def desenhar_fundo(self):
        """O fundo, com um véu claro por cima (igual em todas as telas)."""
        self.tela.blit(self.fundo, (0, 0))
        veu = pygame.Surface((config.LARGURA, config.ALTURA), pygame.SRCALPHA)
        veu.fill(layout.VEU_BRANCO)
        self.tela.blit(veu, (0, 0))

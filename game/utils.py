# -*- coding: utf-8 -*-
"""Funcoes utilitarias de desenho que nao dependem do estado do jogo:
carregar sprites, quebrar texto em linhas e desenhar o card/painel
translucido usado em quase toda tela."""
import os
import pygame

from .constants import ASSETS


def load_bee_frames():
    frames = []
    for i in range(9):
        img = pygame.image.load(os.path.join(ASSETS, f"bee_frame_{i}.png")).convert_alpha()
        frames.append(pygame.transform.scale(img, (96, 96)))
    return frames


def load_emoji_images(councilors, size=48):
    """Carrega o PNG de emoji de cada conselheira (assets/emoji/<emoji_file>)
    e devolve um dict {nome_da_conselheira: Surface}, ja no tamanho pedido.

    Pygame nao renderiza emoji colorido a partir de fonte de texto -- por
    isso usamos imagens prontas em vez do caractere unicode. Se o arquivo
    de uma conselheira nao existir, ela simplesmente fica sem imagem (o
    texto do motto/titulo continua aparecendo normalmente)."""
    images = {}
    emoji_dir = os.path.join(ASSETS, "emoji")
    for name, data in councilors.items():
        filename = data.get("emoji_file")
        if not filename:
            continue
        path = os.path.join(emoji_dir, filename)
        if not os.path.isfile(path):
            continue
        img = pygame.image.load(path).convert_alpha()
        images[name] = pygame.transform.smoothscale(img, (size, size))
    return images


def wrap_text(text, font, max_width):
    words = text.split(" ")
    lines, current = [], ""
    for w in words:
        trial = (current + " " + w).strip()
        if font.size(trial)[0] <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = w
    if current:
        lines.append(current)
    return lines


def draw_panel(surface, rect, radius=16, alpha=235):
    panel = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    pygame.draw.rect(panel, (255, 255, 255, alpha), panel.get_rect(), border_radius=radius)
    pygame.draw.rect(panel, (120, 120, 120, 255), panel.get_rect(), 2, border_radius=radius)
    surface.blit(panel, rect.topleft)

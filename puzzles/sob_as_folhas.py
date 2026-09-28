# -*- coding: utf-8 -*-
"""Sob as Folhas (Flora, Evento 1 — O Novo Jardim).

Um terreno cheio de folhas cobre o chão. Embaixo de 6 delas (sempre 6,
não importa a dificuldade) há insetos escondidos. O objetivo é remover
TODAS as folhas sem acertar os insetos.

Regras de resultado:
  - Removeu todas as folhas, 0 insetos atingidos        -> sucesso
  - Removeu todas as folhas, 1 a 3 insetos atingidos     -> parcial
  - Removeu todas as folhas, 4+ insetos atingidos        -> falha
  - Tempo acabou com folhas sobrando                     -> falha
"""
import random
import pygame

from .base import BasePuzzle, difficulty_scale, TEXT_DARK

LEAF_COLOR = (110, 150, 70)
LEAF_EDGE = (80, 115, 50)
GRASS_COLOR = (170, 205, 130)
INSECT_HIT_COLOR = (200, 90, 80)
INSECT_SAFE_COLOR = (90, 90, 90)

TOTAL_INSECTS = 6


class SobAsFolhas(BasePuzzle):
    name = "Sob as Folhas"

    def __init__(self, rect, difficulty=1, relacao=100):
        self.rect = rect
        self.difficulty = difficulty
        self.done = False
        self.result = None

        # grade de folhas: mais dificil = grade maior (mais cliques, mesmo
        # numero fixo de 6 insetos misturados no meio)
        cols = int(difficulty_scale(difficulty, relacao, 5, 7))
        rows = int(difficulty_scale(difficulty, relacao, 4, 5))
        self.cols, self.rows = cols, rows
        cell_w = rect.width / cols
        cell_h = rect.height / rows
        self.cell_size = (cell_w, cell_h)

        total_cells = cols * rows
        insect_indices = set(random.sample(range(total_cells), min(TOTAL_INSECTS, total_cells)))
        self.cells = []
        for i in range(total_cells):
            r, c = divmod(i, cols)
            cx = rect.left + c * cell_w + cell_w / 2
            cy = rect.top + r * cell_h + cell_h / 2
            self.cells.append({
                "center": (cx, cy),
                "removed": False,
                "has_insect": i in insect_indices,
            })

        self.leaves_left = total_cells
        self.insects_hit = 0
        self.time_left = difficulty_scale(difficulty, relacao, 22.0, 15.0)

    def update(self, dt):
        if self.done:
            return
        self.time_left -= dt
        if self.time_left <= 0:
            self._finish()

    def handle_key(self, key):
        pass

    def handle_click(self, pos):
        if self.done:
            return
        for cell in self.cells:
            if cell["removed"]:
                continue
            cx, cy = cell["center"]
            hw, hh = self.cell_size[0] / 2, self.cell_size[1] / 2
            if abs(pos[0] - cx) <= hw and abs(pos[1] - cy) <= hh:
                cell["removed"] = True
                self.leaves_left -= 1
                if cell["has_insect"]:
                    self.insects_hit += 1
                break
        if self.leaves_left <= 0:
            self._finish()

    def _finish(self):
        self.done = True
        if self.leaves_left > 0:
            # tempo acabou com folhas sobrando
            self.result = "falha"
        elif self.insects_hit == 0:
            self.result = "sucesso"
        elif self.insects_hit <= 3:
            self.result = "parcial"
        else:
            self.result = "falha"

    def draw(self, surface):
        pygame.draw.rect(surface, GRASS_COLOR, self.rect, border_radius=8)
        pygame.draw.rect(surface, (150, 150, 150), self.rect, 2, border_radius=8)
        hw, hh = self.cell_size[0] / 2 - 3, self.cell_size[1] / 2 - 3
        for cell in self.cells:
            cx, cy = cell["center"]
            if cell["removed"]:
                if cell["has_insect"]:
                    color = INSECT_HIT_COLOR
                    pygame.draw.circle(surface, color, (int(cx), int(cy)), 8)
                continue
            leaf_rect = pygame.Rect(0, 0, hw * 2, hh * 2)
            leaf_rect.center = (cx, cy)
            pygame.draw.ellipse(surface, LEAF_COLOR, leaf_rect)
            pygame.draw.ellipse(surface, LEAF_EDGE, leaf_rect, 2)
        font = pygame.font.SysFont("verdana", 13)
        txt = font.render(
            f"Folhas restantes: {self.leaves_left}  Insetos atingidos: {self.insects_hit}  "
            f"Tempo: {max(0, self.time_left):.1f}s", True, TEXT_DARK)
        surface.blit(txt, (self.rect.left, self.rect.bottom + 16))

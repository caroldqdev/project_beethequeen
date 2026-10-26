# -*- coding: utf-8 -*-
"""Rastro de Polen (Melina, Evento 1 — O Novo Jardim).

Arraste o mouse para 'pintar' o campo de amarelo (polinizar) antes que o
tempo acabe. Quanto mais area coberta, melhor o resultado.

Regras de resultado (fracao do campo coberta quando o tempo acaba):
  - < 60%          -> falha
  - 60% a 70%      -> parcial (sucesso)
  - > 70%          -> sucesso (sucesso total)
"""
import pygame

from .base import BasePuzzle, difficulty_scale, TEXT_DARK, GOLD_LINE

GRASS_COLOR = (170, 205, 130)
POLLEN_COLOR = (240, 200, 60)
BRUSH_RADIUS_CELLS = 1  # quantas celulas ao redor do cursor sao pintadas de uma vez


class RastroDePolen(BasePuzzle):
    name = "Rastro de Pólen"
    # texto da tela de preparo (os segundos antes de jogar)
    instrucao = (
        "Arraste o mouse (mantendo o botão pressionado) para polinizar o campo de "
        "amarelo. Cubra o máximo possível antes que o tempo acabe."
    )

    def __init__(self, rect, difficulty=1, relacao=100):
        self.rect = rect
        self.difficulty = difficulty
        self.done = False
        self.result = None

        self.cell_size = 18
        self.cols = max(1, int(rect.width // self.cell_size))
        self.rows = max(1, int(rect.height // self.cell_size))
        self.covered = [[False] * self.cols for _ in range(self.rows)]
        self.total_cells = self.cols * self.rows
        self.covered_count = 0

        self.time_left = difficulty_scale(difficulty, relacao, 10.0, 6.5)

    def _cell_at(self, pos):
        gx = int((pos[0] - self.rect.left) // self.cell_size)
        gy = int((pos[1] - self.rect.top) // self.cell_size)
        if 0 <= gx < self.cols and 0 <= gy < self.rows:
            return gx, gy
        return None

    def _paint(self, pos):
        cell = self._cell_at(pos)
        if cell is None:
            return
        gx, gy = cell
        for dy in range(-BRUSH_RADIUS_CELLS, BRUSH_RADIUS_CELLS + 1):
            for dx in range(-BRUSH_RADIUS_CELLS, BRUSH_RADIUS_CELLS + 1):
                x, y = gx + dx, gy + dy
                if 0 <= x < self.cols and 0 <= y < self.rows and not self.covered[y][x]:
                    self.covered[y][x] = True
                    self.covered_count += 1

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
        self._paint(pos)

    def handle_drag(self, pos, pressed):
        if self.done or not pressed:
            return
        self._paint(pos)

    def _finish(self):
        self.done = True
        ratio = self.covered_count / max(1, self.total_cells)
        if ratio > 0.70:
            self.result = "sucesso"
        elif ratio >= 0.60:
            self.result = "parcial"
        else:
            self.result = "falha"

    def draw(self, surface):
        pygame.draw.rect(surface, GRASS_COLOR, self.rect, border_radius=8)
        pygame.draw.rect(surface, (150, 150, 150), self.rect, 2, border_radius=8)
        for gy in range(self.rows):
            for gx in range(self.cols):
                if self.covered[gy][gx]:
                    x = self.rect.left + gx * self.cell_size
                    y = self.rect.top + gy * self.cell_size
                    pygame.draw.rect(surface, POLLEN_COLOR,
                                      (x, y, self.cell_size, self.cell_size))
        ratio = self.covered_count / max(1, self.total_cells)
        bar_rect = pygame.Rect(self.rect.left, self.rect.bottom + 34, self.rect.width, 12)
        pygame.draw.rect(surface, (230, 230, 230), bar_rect, border_radius=6)
        pygame.draw.rect(surface, GOLD_LINE,
                          (bar_rect.left, bar_rect.top, int(bar_rect.width * ratio), bar_rect.height),
                          border_radius=6)
        font = pygame.font.SysFont("verdana", 13)
        txt = font.render(
            f"Arraste o mouse para polinizar  Coberto: {ratio*100:.0f}%  "
            f"Tempo: {max(0, self.time_left):.1f}s", True, TEXT_DARK)
        surface.blit(txt, (self.rect.left, self.rect.bottom + 12))

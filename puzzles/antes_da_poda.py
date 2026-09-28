# -*- coding: utf-8 -*-
"""Antes da Poda (Aurora, Evento 1 — O Novo Jardim).

Mesma ideia de "pintar" do Rastro de Polen, mas agora e uma corrida:
enquanto voce poliniza de amarelo arrastando o mouse, o jardineiro vai
avancando (sem querer) de vermelho, sozinho, cortando a grama. A ideia
NAO e vencer o jardineiro -- e garantir uma zona polinizada segura antes
que ele chegue perto demais das abelhas.

Regras de resultado (quem cobre 70% do campo primeiro):
  - Jardineiro cobre 70% primeiro          -> falha
  - Voce cobre 70% em menos de 1 minuto    -> sucesso (sucesso total)
  - Voce cobre 70% depois de 1 minuto      -> parcial (sucesso)
"""
import random
import pygame

from .base import BasePuzzle, TEXT_DARK

GRASS_COLOR = (170, 205, 130)
PLAYER_COLOR = (240, 200, 60)
GARDENER_COLOR = (200, 90, 80)
TARGET_RATIO = 0.70


class AntesDaPoda(BasePuzzle):
    name = "Antes da Poda"

    def __init__(self, rect, difficulty=1, relacao=100):
        self.rect = rect
        self.difficulty = difficulty
        self.done = False
        self.result = None

        self.cell_size = 18
        self.cols = max(1, int(rect.width // self.cell_size))
        self.rows = max(1, int(rect.height // self.cell_size))
        self.total_cells = self.cols * self.rows
        # 0 = livre, 1 = jogador, 2 = jardineiro
        self.grid = [[0] * self.cols for _ in range(self.rows)]
        self.player_count = 0
        self.gardener_count = 0

        # jardineiro fica mais rapido quanto maior a dificuldade
        d = max(1, min(5, difficulty))
        self.gardener_interval = max(0.05, 0.22 - 0.03 * d)  # segundos por celula
        self.gardener_timer = self.gardener_interval

        self.elapsed = 0.0

    def _cell_at(self, pos):
        gx = int((pos[0] - self.rect.left) // self.cell_size)
        gy = int((pos[1] - self.rect.top) // self.cell_size)
        if 0 <= gx < self.cols and 0 <= gy < self.rows:
            return gx, gy
        return None

    def _paint_player(self, pos):
        cell = self._cell_at(pos)
        if cell is None:
            return
        gx, gy = cell
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                x, y = gx + dx, gy + dy
                if 0 <= x < self.cols and 0 <= y < self.rows and self.grid[y][x] == 0:
                    self.grid[y][x] = 1
                    self.player_count += 1

    def _gardener_step(self):
        free = [(x, y) for y in range(self.rows) for x in range(self.cols)
                if self.grid[y][x] == 0]
        if not free:
            return
        x, y = random.choice(free)
        self.grid[y][x] = 2
        self.gardener_count += 1

    def update(self, dt):
        if self.done:
            return
        self.elapsed += dt
        self.gardener_timer -= dt
        while self.gardener_timer <= 0:
            self._gardener_step()
            self.gardener_timer += self.gardener_interval

        gardener_ratio = self.gardener_count / self.total_cells
        player_ratio = self.player_count / self.total_cells

        if gardener_ratio >= TARGET_RATIO:
            self.done = True
            self.result = "falha"
        elif player_ratio >= TARGET_RATIO:
            self.done = True
            self.result = "sucesso" if self.elapsed < 60 else "parcial"
        elif self.player_count + self.gardener_count >= self.total_cells:
            # campo todo ocupado sem ninguem bater 70% -- decide por quem tem mais
            self.done = True
            self.result = "parcial" if player_ratio > gardener_ratio else "falha"

    def handle_key(self, key):
        pass

    def handle_click(self, pos):
        if self.done:
            return
        self._paint_player(pos)

    def handle_drag(self, pos, pressed):
        if self.done or not pressed:
            return
        self._paint_player(pos)

    def draw(self, surface):
        pygame.draw.rect(surface, GRASS_COLOR, self.rect, border_radius=8)
        pygame.draw.rect(surface, (150, 150, 150), self.rect, 2, border_radius=8)
        for gy in range(self.rows):
            for gx in range(self.cols):
                state = self.grid[gy][gx]
                if state == 0:
                    continue
                color = PLAYER_COLOR if state == 1 else GARDENER_COLOR
                x = self.rect.left + gx * self.cell_size
                y = self.rect.top + gy * self.cell_size
                pygame.draw.rect(surface, color, (x, y, self.cell_size, self.cell_size))

        player_ratio = self.player_count / self.total_cells
        gardener_ratio = self.gardener_count / self.total_cells
        bar_y = self.rect.bottom + 34
        bar_w = self.rect.width
        pygame.draw.rect(surface, (230, 230, 230), (self.rect.left, bar_y, bar_w, 12), border_radius=6)
        pygame.draw.rect(surface, PLAYER_COLOR,
                          (self.rect.left, bar_y, int(bar_w * player_ratio), 12), border_radius=6)
        pygame.draw.rect(surface, GARDENER_COLOR,
                          (self.rect.left, bar_y + 16, int(bar_w * gardener_ratio), 12), border_radius=6)

        font = pygame.font.SysFont("verdana", 13)
        txt = font.render(
            f"Voce (amarelo): {player_ratio*100:.0f}%   Jardineiro (vermelho): "
            f"{gardener_ratio*100:.0f}%   Meta: {int(TARGET_RATIO*100)}%   "
            f"Tempo: {self.elapsed:.0f}s", True, TEXT_DARK)
        surface.blit(txt, (self.rect.left, bar_y + 34))

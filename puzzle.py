# -*- coding: utf-8 -*-
"""
Puzzle de execucao (placeholder para o MVP).

O Roteiro Narrativo define 8 puzzles distintos no GDD (Espalhar Polen,
Corredores Verdes, Organizar os Favos, Salvar Flores, Danca das Abelhas,
Resgatar Operarias, Flores Resistentes, Defesa da Colmeia). Implementar
os 8 mecanicamente e trabalho de Sprint 3+.

Para este MVP, todos eles sao representados por UM mini-jogo generico de
"execucao com risco" -- uma barra com um alvo em movimento. O jogador
aperta ESPACO para travar o marcador dentro da barra:

  - Acerto no alvo (verde)   -> execucao BEM-SUCEDIDA: efeito completo
  - Acerto na borda (amarelo)-> execucao PARCIAL: metade do efeito
  - Fora do alvo             -> execucao FALHOU: 25% do efeito, custo integral

Isso mantem o padrao pedido (evento -> escolha -> puzzle -> consequencia)
sem ter que codificar 8 mecanicas diferentes agora. O nome do puzzle do
GDD ainda e mostrado na tela, como referencia para o proximo sprint.
"""
import random
import pygame

BAR_COLOR = (230, 230, 230)
TARGET_GOOD = (120, 200, 120)
TARGET_OK = (230, 200, 90)
MARKER_COLOR = (60, 60, 60)


class PuzzleState:
    def __init__(self, rect):
        self.rect = rect  # pygame.Rect da barra
        self.marker_x = rect.left
        self.speed = random.choice([-1, 1]) * random.uniform(320, 480)
        good_w = rect.width * 0.16
        ok_w = rect.width * 0.30
        center = random.uniform(rect.left + ok_w / 2, rect.right - ok_w / 2)
        self.good_zone = pygame.Rect(0, rect.top, good_w, rect.height)
        self.good_zone.centerx = center
        self.ok_zone = pygame.Rect(0, rect.top, ok_w, rect.height)
        self.ok_zone.centerx = center
        self.done = False
        self.result = None  # "sucesso" | "parcial" | "falha"

    def update(self, dt):
        if self.done:
            return
        self.marker_x += self.speed * dt
        if self.marker_x <= self.rect.left:
            self.marker_x = self.rect.left
            self.speed *= -1
        elif self.marker_x >= self.rect.right:
            self.marker_x = self.rect.right
            self.speed *= -1

    def lock(self):
        if self.done:
            return
        self.done = True
        if self.good_zone.left <= self.marker_x <= self.good_zone.right:
            self.result = "sucesso"
        elif self.ok_zone.left <= self.marker_x <= self.ok_zone.right:
            self.result = "parcial"
        else:
            self.result = "falha"

    def effect_multiplier(self):
        return {"sucesso": 1.0, "parcial": 0.5, "falha": 0.25}.get(self.result, 0.25)

    def draw(self, surface):
        pygame.draw.rect(surface, BAR_COLOR, self.rect, border_radius=8)
        pygame.draw.rect(surface, TARGET_OK, self.ok_zone, border_radius=6)
        pygame.draw.rect(surface, TARGET_GOOD, self.good_zone, border_radius=6)
        pygame.draw.rect(surface, (120, 120, 120), self.rect, 2, border_radius=8)
        pygame.draw.line(surface, MARKER_COLOR,
                          (self.marker_x, self.rect.top - 10),
                          (self.marker_x, self.rect.bottom + 10), 4)

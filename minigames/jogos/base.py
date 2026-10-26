# -*- coding: utf-8 -*-
"""Classe base dos minigames + helper de escala de dificuldade.

Todo minigame novo deve herdar de BasePuzzle e reimplementar:
    update(dt), handle_key(key), handle_click(pos), draw(surface)
e definir self.done / self.result ("sucesso"|"parcial"|"falha") quando acabar.
"""
import random
import pygame

BAR_COLOR = (230, 230, 230)
TARGET_GOOD = (120, 200, 120)
TARGET_OK = (230, 200, 90)
TARGET_BAD = (210, 90, 90)
MARKER_COLOR = (60, 60, 60)
TEXT_DARK = (40, 40, 40)
GOLD_LINE = (214, 158, 46)


def difficulty_scale(difficulty, relacao, lo, hi):
    """Interpola um valor entre lo (facil) e hi (dificil) segundo difficulty 1-5,
    e aplica penalidade extra se a relacao com a colmeia estiver baixa."""
    d = max(1, min(5, difficulty))
    t = (d - 1) / 4.0
    val = lo + (hi - lo) * t
    if relacao is not None and relacao < 25:
        val += (hi - lo) * 0.2  # empurra em direcao ao mais dificil
    return val


class BasePuzzle:
    """Fallback generico: barra + zona alvo + travar com ESPACO."""

    name = "Acao Direta"
    # texto da tela de preparo (os segundos antes de jogar)
    instrucao = "Pressione ESPAÇO para travar o marcador na zona certa."

    def __init__(self, rect, difficulty=1, relacao=100):
        self.rect = rect
        self.difficulty = difficulty
        self.relacao = relacao
        self.done = False
        self.result = None
        self.marker_x = rect.left
        self.speed = random.choice([-1, 1]) * difficulty_scale(difficulty, relacao, 260, 520)
        good_w = rect.width * difficulty_scale(difficulty, relacao, 0.22, 0.10)
        ok_w = rect.width * difficulty_scale(difficulty, relacao, 0.38, 0.22)
        center = random.uniform(rect.left + ok_w / 2, rect.right - ok_w / 2)
        self.good_zone = pygame.Rect(0, rect.top, good_w, rect.height)
        self.good_zone.centerx = center
        self.ok_zone = pygame.Rect(0, rect.top, ok_w, rect.height)
        self.ok_zone.centerx = center

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

    def handle_key(self, key):
        if key == pygame.K_SPACE and not self.done:
            self.done = True
            if self.good_zone.left <= self.marker_x <= self.good_zone.right:
                self.result = "sucesso"
            elif self.ok_zone.left <= self.marker_x <= self.ok_zone.right:
                self.result = "parcial"
            else:
                self.result = "falha"

    def handle_click(self, pos):
        pass

    def handle_drag(self, pos, pressed):
        """Chamado a cada movimento do mouse (arrastar). `pressed` indica se
        o botao esquerdo esta pressionado. So os minigames que precisam de
        'pintar'/'arrastar' (Rastro de Polen, Antes da Poda, Rota de Voo)
        reimplementam isso -- os demais ignoram."""
        pass

    def handle_release(self, pos):
        """Chamado quando o botao do mouse e solto. So os minigames que
        precisam saber onde o arrasto terminou reimplementam isso."""
        pass

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
        font = pygame.font.SysFont("verdana", 13)
        hint = font.render("ESPACO para travar o marcador", True, TEXT_DARK)
        surface.blit(hint, (self.rect.left, self.rect.bottom + 16))

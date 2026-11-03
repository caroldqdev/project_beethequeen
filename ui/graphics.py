# -*- coding: utf-8 -*-
"""Funcoes de desenho de graficos simples em pygame: o radar de 5 eixos
da Harmonia da Colmeia (draw_radar) e uma barra de progresso generica
(draw_bar), usada tambem para Mel, Operarias, Relacao e Afinidade."""
import math
import pygame
from data.axes import HARMONIA_AXES, HARMONIA_LABELS

BG = (255, 255, 255)
GRID = (200, 210, 200)
FILL = (255, 209, 102, 120)
LINE = (214, 158, 46)


def draw_radar(surface, center, radius, values, font, max_value=100):
    """values: dict eixo -> valor 0..max_value"""
    cx, cy = center
    n = len(HARMONIA_AXES)
    angle_step = 2 * math.pi / n

    for ring in (0.25, 0.5, 0.75, 1.0):
        points = []
        for i in range(n):
            ang = -math.pi / 2 + i * angle_step
            x = cx + math.cos(ang) * radius * ring
            y = cy + math.sin(ang) * radius * ring
            points.append((x, y))
        pygame.draw.polygon(surface, GRID, points, 1)

    for i, axis in enumerate(HARMONIA_AXES):
        ang = -math.pi / 2 + i * angle_step
        x = cx + math.cos(ang) * radius
        y = cy + math.sin(ang) * radius
        pygame.draw.line(surface, GRID, (cx, cy), (x, y), 1)
        lx = cx + math.cos(ang) * (radius + 34)
        ly = cy + math.sin(ang) * (radius + 16)
        label = font.render(HARMONIA_LABELS[axis], True, (70, 70, 70))
        rect = label.get_rect(center=(lx, ly))
        surface.blit(label, rect)

    poly_points = []
    for i, axis in enumerate(HARMONIA_AXES):
        val = max(0, min(max_value, values.get(axis, 0)))
        ang = -math.pi / 2 + i * angle_step
        r = radius * (val / max_value)
        x = cx + math.cos(ang) * r
        y = cy + math.sin(ang) * r
        poly_points.append((x, y))

    shape_surf = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    pygame.draw.polygon(shape_surf, FILL, poly_points)
    surface.blit(shape_surf, (0, 0))
    pygame.draw.polygon(surface, LINE, poly_points, 3)
    for p in poly_points:
        pygame.draw.circle(surface, LINE, (int(p[0]), int(p[1])), 4)


def draw_bar(surface, pos, size, value, max_value, color, bg_color=(230, 230, 230)):
    x, y = pos
    w, h = size
    pygame.draw.rect(surface, bg_color, (x, y, w, h), border_radius=6)
    ratio = max(0.0, min(1.0, value / max_value))
    if ratio > 0:
        pygame.draw.rect(surface, color, (x, y, int(w * ratio), h), border_radius=6)
    pygame.draw.rect(surface, (150, 150, 150), (x, y, w, h), 1, border_radius=6)
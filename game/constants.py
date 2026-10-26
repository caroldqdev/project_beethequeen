# -*- coding: utf-8 -*-
"""Constantes globais: tamanho de tela, cores, nomes dos estados do jogo."""
import os

WIDTH, HEIGHT = 1000, 650
FPS = 60
ASSETS = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")

WHITE = (255, 255, 255)
DARK = (40, 40, 40)
GOLD = (214, 158, 46)
RELACAO_COLOR = (196, 108, 196)

# --- estados (telas) do jogo -------------------------------------------
STATE_INTRO = "intro"
STATE_COUNCIL_INTRO = "council_intro"
STATE_QUEEN_INTRO = "queen_intro"
STATE_SEASON = "season"
STATE_CONTEXT = "context"
STATE_CHOICE = "choice"
STATE_PUZZLE_BRIEFING = "puzzle_briefing"
STATE_PUZZLE = "puzzle"
STATE_PUZZLE_RESULT = "puzzle_result"
STATE_RESULT = "result"
STATE_SUMMARY = "summary"

BRIEFING_TIME = 5.0  # segundos de preparo antes de cada minigame comecar

SEASON_DIFFICULTY = {"Primavera": 1, "Verao": 2, "Outono": 3, "Inverno": 4}
COUNCIL_ORDER = ["Flora", "Melina", "Nectar", "Aurora"]

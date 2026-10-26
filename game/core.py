# -*- coding: utf-8 -*-
"""
Classe Game final: junta as 3 partes do jogo, cada uma vinda de um arquivo:

    GameLogic   (game/logic.py)    -> regras: numeros, custos, estado
    GameScreens (game/screens.py)  -> tudo que e desenhado na tela
    GameInput   (game/input.py)    -> teclado/mouse + loop principal

Isso e chamado de "mixin": a classe Game abaixo nao tem metodos proprios
(so o __init__), ela so "herda" os metodos de cada uma das 3 partes. Se
voce quer mudar uma REGRA do jogo, mexe em logic.py. Se quer mudar como
algo APARECE na tela, mexe em screens.py. Se quer mudar o que uma TECLA
faz, mexe em input.py.
"""
import os
import pygame

from data import EVENTS, COUNCILORS, HARMONIA_AXES
from .constants import WIDTH, HEIGHT, ASSETS, STATE_INTRO, BRIEFING_TIME
from .utils import load_bee_frames, load_emoji_images
from .logic import GameLogic
from .screens import GameScreens
from .input import GameInput


class Game(GameLogic, GameScreens, GameInput):
    # dados do jogo ficam disponiveis como atributo de classe, assim
    # game.logic pode fazer self.EVENTS sem precisar importar de novo
    EVENTS = EVENTS

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Bee the Queen")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

        self.font_title = pygame.font.SysFont("georgia", 30, bold=True)
        self.font_h2 = pygame.font.SysFont("georgia", 22, bold=True)
        self.font_body = pygame.font.SysFont("verdana", 16)
        self.font_body_bold = pygame.font.SysFont("verdana", 16, bold=True)
        self.font_small = pygame.font.SysFont("verdana", 13)
        self.font_btn = pygame.font.SysFont("verdana", 15, bold=True)

        self.background = pygame.transform.scale(
            pygame.image.load(os.path.join(ASSETS, "bg_scene.png")).convert(), (WIDTH, HEIGHT))
        self.bee_frames = load_bee_frames()
        self.bee_frame_idx = 0
        self.bee_timer = 0.0
        self.emoji_images = load_emoji_images(COUNCILORS, size=48)

        # --- estado do jogo ---
        self.harmonia = {axis: 50 for axis in HARMONIA_AXES}
        self.mel = 100
        self.operarias = 100
        self.relacao = 60  # 3o recurso: moral/confianca da colmeia (Guia 2, sec.1)
        self.affinity = {name: 40 for name in COUNCILORS}
        self.event_index = 0
        self.current_season = None
        self.history = []
        self.next_cooperacao_multiplier = 1.0  # penalidade de falha da Aurora

        self.council_intro_idx = 0

        self.state = STATE_INTRO
        self.chosen_option = None
        self.puzzle = None
        self.result_lines = []
        self.option_rects = []
        self.fail_penalty_text = None
        self.briefing_timer = BRIEFING_TIME
        self.pending_puzzle_name = None
        self.pending_difficulty = 1

# -*- coding: utf-8 -*-
"""
Entrada do jogador (teclado/mouse) e o loop principal (`run`). Decide, para
cada tecla/clique, o que fazer dependendo do estado atual -- delega a
mudanca de estado/numeros para os metodos de game/logic.py.

Este modulo define GameInput, "misturado" (mixin) na classe Game final,
em game/core.py.
"""
import sys
import pygame

from .constants import (FPS, STATE_INTRO, STATE_COUNCIL_INTRO, STATE_QUEEN_INTRO,
                         STATE_SEASON, STATE_CONTEXT, STATE_CHOICE,
                         STATE_PUZZLE_BRIEFING, STATE_PUZZLE,
                         STATE_PUZZLE_RESULT, STATE_RESULT, COUNCIL_ORDER)


class GameInput:
    def handle_event(self, event, mouse_pos):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if self.state == STATE_INTRO and event.key == pygame.K_RETURN:
                self.state = STATE_COUNCIL_INTRO
                self.council_intro_idx = 0
            elif self.state == STATE_COUNCIL_INTRO and event.key == pygame.K_RETURN:
                if self.council_intro_idx < len(COUNCIL_ORDER) - 1:
                    self.council_intro_idx += 1
                else:
                    self.state = STATE_QUEEN_INTRO
            elif self.state == STATE_QUEEN_INTRO and event.key == pygame.K_RETURN:
                self.start_event()
            elif self.state == STATE_SEASON and event.key == pygame.K_RETURN:
                self.state = STATE_CONTEXT
            elif self.state == STATE_CONTEXT and event.key == pygame.K_RETURN:
                self.go_to_choice()
            elif self.state == STATE_PUZZLE_BRIEFING and event.key == pygame.K_RETURN:
                self.start_puzzle()
            elif self.state == STATE_PUZZLE:
                if self.puzzle is not None and not self.puzzle.done:
                    self.puzzle.handle_key(event.key)
                elif event.key == pygame.K_RETURN and self.puzzle is not None and self.puzzle.done:
                    self.resolve_choice(self.puzzle.effect_multiplier())
            elif self.state == STATE_PUZZLE_RESULT and event.key == pygame.K_RETURN:
                self.state = STATE_RESULT
            elif self.state == STATE_RESULT and event.key == pygame.K_RETURN:
                self.next_event()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.state == STATE_CHOICE:
                for rect, opt in self.option_rects:
                    if rect.collidepoint(mouse_pos):
                        self.choose_option(opt)
                        break
            elif self.state == STATE_PUZZLE and self.puzzle is not None and not self.puzzle.done:
                self.puzzle.handle_click(mouse_pos)

    def run(self):
        while True:
            dt = self.clock.tick(FPS) / 1000.0
            self.bee_timer += dt
            if self.bee_timer >= 0.15:
                self.bee_timer = 0.0
                self.bee_frame_idx = (self.bee_frame_idx + 1) % len(self.bee_frames)

            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                self.handle_event(event, mouse_pos)

            if self.state == STATE_PUZZLE_BRIEFING:
                self.briefing_timer -= dt
                if self.briefing_timer <= 0:
                    self.start_puzzle()

            if self.state == STATE_PUZZLE and self.puzzle is not None:
                self.puzzle.update(dt)

            self.render(mouse_pos)

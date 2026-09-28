# -*- coding: utf-8 -*-
"""
Tudo o que aparece na tela. Cada tela do jogo tem uma funcao render_*
correspondente. NADA aqui muda regra de jogo (Mel, Harmonia etc.) -- para
isso, veja game/logic.py.

Este modulo define GameScreens, "misturado" (mixin) na classe Game final,
em game/core.py.

Onde editar o QUE aparece escrito:
  - Textos dos eventos (contexto, falas, consequencia)  -> data/events/*.py
  - Falas/titulo/motto das conselheiras                  -> data/councilors.py
  - Texto da tela "A Nova Rainha"                        -> aqui, render_queen_intro()
  - Texto da tela de abertura                            -> aqui, render_intro()
  - Instrucao de cada minigame (tela de preparo)         -> puzzles/__init__.py

Onde editar COMO aparece (posicao, cor, tamanho):
  - Tudo neste arquivo mesmo, um metodo por tela.
"""
import math
import pygame

from data import COUNCILORS, PROFILE_TEXTS, ECOLOGY_MESSAGE
from puzzles import get_instructions
from ui.harmonia import draw_radar, draw_bar
from .constants import (WIDTH, HEIGHT, WHITE, DARK, GOLD, RELACAO_COLOR,
                         STATE_INTRO, STATE_COUNCIL_INTRO, STATE_QUEEN_INTRO,
                         STATE_SEASON, STATE_CONTEXT, STATE_CHOICE,
                         STATE_PUZZLE_BRIEFING, STATE_PUZZLE,
                         STATE_PUZZLE_RESULT, STATE_RESULT, STATE_SUMMARY,
                         COUNCIL_ORDER)
from .utils import wrap_text, draw_panel


class GameScreens:
    # ----------------------------------------------------------------- draw
    def draw_bee(self, pos):
        self.screen.blit(self.bee_frames[self.bee_frame_idx], pos)

    def draw_hud(self):
        # --- painel esquerdo: Mel / Operarias / Relacao ---
        left_panel = pygame.Rect(16, 16, 310, 168)
        draw_panel(self.screen, left_panel)
        pad_x = left_panel.left + 14
        bar_w = left_panel.width - 28
        row_h = 34
        y = left_panel.top + 12

        self.screen.blit(self.font_small.render(f"Mel: {self.mel}", True, DARK), (pad_x, y))
        draw_bar(self.screen, (pad_x, y + 18), (bar_w, 12), self.mel, 150, GOLD)
        y += row_h

        self.screen.blit(self.font_small.render(f"Operarias: {self.operarias}", True, DARK), (pad_x, y))
        draw_bar(self.screen, (pad_x, y + 18), (bar_w, 12), self.operarias, 150, (120, 170, 90))
        y += row_h

        self.screen.blit(self.font_small.render(
            f"Relacao com a Colmeia: {self.relacao}", True, DARK), (pad_x, y))
        draw_bar(self.screen, (pad_x, y + 18), (bar_w, 12), self.relacao, 100, RELACAO_COLOR)
        y += row_h

        if self.production_penalty_active():
            warn = self.font_small.render("Relacao baixa: producao com penalidade!", True, (180, 60, 60))
            self.screen.blit(warn, (pad_x, y))

        # --- painel direito: Afinidade das conselheiras ---
        right_panel = pygame.Rect(WIDTH - 326, 16, 310, 168)
        draw_panel(self.screen, right_panel)
        rpad_x = right_panel.left + 14
        title = self.font_small.render("Afinidade das Conselheiras", True, DARK)
        self.screen.blit(title, (rpad_x, right_panel.top + 12))
        row_y = right_panel.top + 38
        row_gap = 30
        label_w = 62
        bar_w2 = right_panel.width - 28 - label_w
        for name, data in COUNCILORS.items():
            label = self.font_small.render(name, True, DARK)
            self.screen.blit(label, (rpad_x, row_y + 2))
            draw_bar(self.screen, (rpad_x + label_w, row_y), (bar_w2, 14),
                     self.affinity[name], 100, data["color"])
            row_y += row_gap

    def draw_wrapped(self, text, rect, font, color=DARK, line_gap=6):
        lines = []
        for para in text.split("\n"):
            wrapped = wrap_text(para, font, rect.width)
            if wrapped:
                lines.extend(wrapped)
            else:
                lines.append("")  # paragrafo vazio vira uma linha em branco de verdade
        y = rect.top
        for line in lines:
            surf = font.render(line, True, color)
            self.screen.blit(surf, (rect.left, y))
            y += font.get_height() + line_gap
        return y

    def draw_wrapped_centered(self, text, rect, font, color=DARK, line_gap=6):
        """Como draw_wrapped, mas cada linha fica centralizada na horizontal
        e o bloco inteiro fica centralizado na vertical dentro de `rect`."""
        lines = []
        for para in text.split("\n"):
            wrapped = wrap_text(para, font, rect.width)
            if wrapped:
                lines.extend(wrapped)
            else:
                lines.append("")  # paragrafo vazio vira uma linha em branco de verdade
        line_h = font.get_height() + line_gap
        total_h = len(lines) * line_h - line_gap
        y = rect.top + (rect.height - total_h) // 2
        for line in lines:
            surf = font.render(line, True, color)
            self.screen.blit(surf, surf.get_rect(center=(rect.centerx, y + font.get_height() // 2)))
            y += line_h
        return y

    # ---------------------------------------------------------------- frames
    def render(self, mouse_pos):
        self.screen.blit(self.background, (0, 0))
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((255, 255, 255, 40))
        self.screen.blit(overlay, (0, 0))

        if self.state == STATE_INTRO:
            self.render_intro()
        elif self.state == STATE_COUNCIL_INTRO:
            self.render_council_intro()
        elif self.state == STATE_QUEEN_INTRO:
            self.render_queen_intro()
        elif self.state == STATE_SEASON:
            self.render_season()
        elif self.state == STATE_CONTEXT:
            self.render_context()
        elif self.state == STATE_CHOICE:
            self.render_choice(mouse_pos)
        elif self.state == STATE_PUZZLE_BRIEFING:
            self.render_puzzle_briefing()
        elif self.state == STATE_PUZZLE:
            self.render_puzzle()
        elif self.state == STATE_PUZZLE_RESULT:
            self.render_puzzle_result()
        elif self.state == STATE_RESULT:
            self.render_result()
        elif self.state == STATE_SUMMARY:
            self.render_summary()

        pygame.display.flip()

    # ---- tela de abertura ---------------------------------------------
    def render_intro(self):
        draw_panel(self.screen, pygame.Rect(80, 90, WIDTH - 160, HEIGHT - 180))
        title = self.font_title.render("BEE THE QUEEN", True, DARK)
        self.screen.blit(title, title.get_rect(center=(WIDTH // 2, 140)))
        sub = self.font_h2.render("Ano 1", True, GOLD)
        self.screen.blit(sub, sub.get_rect(center=(WIDTH // 2, 178)))

        y = 220
        y = self.draw_wrapped_centered(
            "A Rainha Anciã se aposenta e escolhe você como sucessora.\n"
            "Você governa apoiada por quatro conselheiras:",
            pygame.Rect(120, y, WIDTH - 240, 60), self.font_body)

        y = self.draw_wrapped_centered(
            "Flora, Melina, Nectar e Aurora",
            pygame.Rect(120, y, WIDTH - 240, 30), self.font_body_bold)

        y += 10  # respiro extra antes do resto do texto
        self.draw_wrapped_centered(
            "Cada escolha altera o painel de Harmonia da Colmeia, a Relação com a Colmeia, "
            "consome recursos e muda a afinidade das conselheiras. "
            "Não existe final único! existe o reino que você constrói."
            "\n\nPressione ENTER para conhecer o Conselho.",
            pygame.Rect(120, y, WIDTH - 240, 160), self.font_body)

        self.draw_bee((WIDTH // 2 - 48, HEIGHT - 150))

    # ---- telas das conselheiras + nova rainha --------------------------
    def render_council_intro(self):
        name = COUNCIL_ORDER[self.council_intro_idx]
        data = COUNCILORS[name]
        draw_panel(self.screen, pygame.Rect(80, 90, WIDTH - 160, HEIGHT - 180))
        header = self.font_title.render(name, True, data["color"])
        header_rect = header.get_rect(center=(WIDTH // 2, 150))
        emoji_img = self.emoji_images.get(name)
        if emoji_img is not None:
            # centraliza o par (emoji + nome) juntos
            gap = 10
            total_w = emoji_img.get_width() + gap + header_rect.width
            start_x = WIDTH // 2 - total_w // 2
            emoji_rect = emoji_img.get_rect(midleft=(start_x, header_rect.centery))
            self.screen.blit(emoji_img, emoji_rect)
            header_rect.left = emoji_rect.right + gap
        self.screen.blit(header, header_rect)
        title = self.font_h2.render(data["title"], True, DARK)
        self.screen.blit(title, title.get_rect(center=(WIDTH // 2, 188)))
        motto = self.font_body.render(f'"{data["motto"]}"', True, GOLD)
        self.screen.blit(motto, motto.get_rect(center=(WIDTH // 2, 224)))
        self.draw_wrapped(data["intro"], pygame.Rect(160, 270, WIDTH - 320, 140), self.font_body)
        hint = self.font_small.render("Pressione ENTER para a proxima conselheira", True, DARK)
        self.screen.blit(hint, hint.get_rect(center=(WIDTH // 2, 470)))
        self.draw_bee((WIDTH // 2 - 48, HEIGHT - 110))

    def render_queen_intro(self):
        draw_panel(self.screen, pygame.Rect(80, 90, WIDTH - 160, HEIGHT - 180))
        header = self.font_title.render("A Nova Rainha", True, DARK)
        self.screen.blit(header, header.get_rect(center=(WIDTH // 2, 160)))
        closing = ("Você é a nova Rainha. A cada estação, o Conselho vai propor 4 caminhos. "
                   "Não existe caminho perfeito. Existe o caminho que você escolhe sustentar.")
        self.draw_wrapped(closing, pygame.Rect(160, 240, WIDTH - 320, 160), self.font_body,
                           color=(70, 70, 70))
        hint = self.font_small.render("Pressione ENTER para comecar o reinado", True, GOLD)
        self.screen.blit(hint, hint.get_rect(center=(WIDTH // 2, 440)))
        self.draw_bee((WIDTH // 2 - 48, HEIGHT - 150))

    # ---- estacao / contexto / escolha -----------------------------------
    def render_season(self):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((20, 20, 30, 140))
        self.screen.blit(overlay, (0, 0))
        label = self.font_title.render(self.current_season.upper(), True, WHITE)
        self.screen.blit(label, label.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20)))
        hint = self.font_body.render("Pressione ENTER para continuar", True, WHITE)
        self.screen.blit(hint, hint.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 30)))

    def render_context(self):
        ev = self.current_event()
        self.draw_hud()
        panel = pygame.Rect(90, 160, WIDTH - 180, 340)
        draw_panel(self.screen, panel)
        header = self.font_h2.render(f"{ev['season']} - Evento {ev['id']}: {ev['title']}", True, DARK)
        self.screen.blit(header, (panel.left + 24, panel.top + 20))
        self.draw_wrapped(ev["context"], pygame.Rect(panel.left + 24, panel.top + 70,
                                                       panel.width - 48, 200), self.font_body)
        hint = self.font_small.render("Pressione ENTER para reunir o Conselho", True, GOLD)
        self.screen.blit(hint, (panel.left + 24, panel.bottom - 40))
        self.draw_bee((panel.right - 110, panel.bottom - 100))

    def render_choice(self, mouse_pos):
        ev = self.current_event()
        self.draw_hud()
        header = self.font_h2.render(f"O Conselho se reune: {ev['title']}", True, DARK)
        self.screen.blit(header, header.get_rect(center=(WIDTH // 2, 165)))

        self.option_rects = []
        card_w, card_h = 470, 160
        gap_x, gap_y = 20, 16
        cols = 2
        start_x = WIDTH // 2 - (cols * card_w + gap_x) // 2
        start_y = 195
        for i, opt in enumerate(ev["options"]):
            col = i % cols
            row = i // cols
            rect = pygame.Rect(start_x + col * (card_w + gap_x),
                                start_y + row * (card_h + gap_y), card_w, card_h)
            hover = rect.collidepoint(mouse_pos)
            data = COUNCILORS[opt["councilor"]]
            color = (255, 240, 210) if hover else (255, 250, 235)
            pygame.draw.rect(self.screen, color, rect, border_radius=12)
            pygame.draw.rect(self.screen, data["color"], rect, 3, border_radius=12)
            name = self.font_btn.render(f"{opt['councilor']}", True, data["color"])
            self.screen.blit(name, (rect.left + 14, rect.top + 10))
            cost = opt.get("cost", {})
            cost_txt = []
            if cost.get("mel"):
                cost_txt.append(f"Mel {cost['mel']}" if cost['mel'] != 'all' else "Mel: tudo")
            if cost.get("operarias"):
                cost_txt.append(f"Operarias {cost['operarias']:+d}")
            if cost.get("relacao"):
                cost_txt.append(f"Relacao {cost['relacao']:+d}")
            cost_str = "  ".join(cost_txt) if cost_txt else "Sem custo direto"
            cost_surf = self.font_small.render(cost_str, True, (110, 90, 40))
            self.screen.blit(cost_surf, (rect.left + 14, rect.top + 34))
            self.draw_wrapped(opt["action"], pygame.Rect(rect.left + 14, rect.top + 54,
                                                           rect.width - 28, 100),
                               self.font_small, color=DARK, line_gap=3)
            self.option_rects.append((rect, opt))

    # ---- minigame: preparo / execucao / resultado -----------------------
    def render_puzzle_briefing(self):
        draw_panel(self.screen, pygame.Rect(90, 120, WIDTH - 180, 360))
        opt = self.chosen_option
        header = self.font_h2.render(f"Preparando: {self.pending_puzzle_name}", True, DARK)
        self.screen.blit(header, header.get_rect(center=(WIDTH // 2, 155)))
        self.draw_wrapped(f"{opt['councilor']} propos: {opt['action']}",
                           pygame.Rect(140, 190, WIDTH - 280, 50), self.font_small,
                           color=(90, 90, 90))
        instructions = get_instructions(self.pending_puzzle_name)
        self.draw_wrapped(instructions, pygame.Rect(140, 260, WIDTH - 280, 120), self.font_body)
        seconds_left = max(1, math.ceil(self.briefing_timer))
        countdown = self.font_title.render(str(seconds_left), True, GOLD)
        self.screen.blit(countdown, countdown.get_rect(center=(WIDTH // 2, 420)))
        hint = self.font_small.render("Pressione ENTER para comecar agora", True, DARK)
        self.screen.blit(hint, hint.get_rect(center=(WIDTH // 2, 460)))
        self.draw_bee((WIDTH - 150, 150))

    def render_puzzle(self):
        opt = self.chosen_option
        draw_panel(self.screen, pygame.Rect(60, 110, WIDTH - 120, 420))
        header = self.font_h2.render(f"Execucao: {self.puzzle.name if self.puzzle else 'Acao direta'}",
                                      True, DARK)
        self.screen.blit(header, header.get_rect(center=(WIDTH // 2, 140)))
        self.draw_wrapped(f"{opt['councilor']} propos: {opt['action']}",
                           pygame.Rect(110, 165, WIDTH - 220, 50), self.font_small)
        if self.puzzle is not None:
            self.puzzle.draw(self.screen)
        if self.puzzle is not None and self.puzzle.done:
            hint = self.font_small.render("Pressione ENTER para ver o resultado", True, DARK)
            self.screen.blit(hint, hint.get_rect(center=(WIDTH // 2, 470)))
        self.draw_bee((WIDTH - 150, 140))

    def render_puzzle_result(self):
        opt = self.chosen_option
        panel = pygame.Rect(120, 140, WIDTH - 240, 340)
        draw_panel(self.screen, panel)
        result = self.puzzle.result if self.puzzle else "sucesso"
        result_txt = {
            "sucesso": "Execucao bem-sucedida!",
            "parcial": "Execucao parcial.",
            "falha": "A execucao falhou.",
        }[result]
        result_detail = {
            "sucesso": "O efeito da escolha foi aplicado por completo (100%).",
            "parcial": "Apenas metade do efeito da escolha foi aplicado (50%).",
            "falha": "So 25% do efeito foi aplicado, e ainda veio uma penalidade extra.",
        }[result]
        result_color = {"sucesso": (90, 160, 90), "parcial": (200, 150, 60),
                        "falha": (190, 80, 80)}[result]
        header = self.font_title.render(result_txt, True, result_color)
        self.screen.blit(header, header.get_rect(center=(WIDTH // 2, panel.top + 46)))
        detail = self.font_body.render(result_detail, True, DARK)
        self.screen.blit(detail, detail.get_rect(center=(WIDTH // 2, panel.top + 84)))

        y = panel.top + 120
        eff_str = "   ".join(self.result_lines) if self.result_lines else "(efeito condicional)"
        y = self.draw_wrapped(f"Efeitos nesta rodada: {eff_str}",
                               pygame.Rect(panel.left + 30, y, panel.width - 60, 50),
                               self.font_small, color=GOLD)
        y += 10
        if self.fail_penalty_text:
            y = self.draw_wrapped(f"Penalidade extra de {opt['councilor']}: {self.fail_penalty_text}",
                                   pygame.Rect(panel.left + 30, y, panel.width - 60, 50),
                                   self.font_small, color=(170, 60, 60))

        hint = self.font_small.render("Pressione ENTER para ver a consequencia", True, DARK)
        self.screen.blit(hint, (panel.left + 30, panel.bottom - 30))
        self.draw_bee((panel.right - 110, panel.top + 10))

    # ---- consequencia -----------------------------------------------------
    def render_result(self):
        ev = self.current_event()
        opt = self.chosen_option
        self.draw_hud()
        panel = pygame.Rect(90, 150, WIDTH - 180, 380)
        draw_panel(self.screen, panel)
        header = self.font_h2.render(f"Consequencia: {ev['title']}", True, DARK)
        self.screen.blit(header, (panel.left + 24, panel.top + 20))

        y = panel.top + 60
        came_from_puzzle = bool(opt.get("puzzle"))
        if not came_from_puzzle:
            # Escolhas sem minigame (acao direta) ainda nao mostraram os
            # efeitos em nenhuma outra tela -- mostra aqui.
            eff_str = "   ".join(self.result_lines) if self.result_lines else "(efeito condicional)"
            eff_surf = self.font_body.render(f"Efeitos: {eff_str}", True, GOLD)
            self.screen.blit(eff_surf, (panel.left + 24, y))
            y += 40

        extra = opt.get("extra")
        if extra:
            y = self.draw_wrapped(extra, pygame.Rect(panel.left + 24, y, panel.width - 48, 40),
                                   self.font_small, color=(90, 70, 30))
            y += 6

        self.draw_wrapped(ev["consequence"], pygame.Rect(panel.left + 24, y, panel.width - 48, 160),
                           self.font_body)

        warn = self.imbalance_warning()
        if warn:
            self.draw_wrapped(warn, pygame.Rect(panel.left + 24, panel.bottom - 80,
                                                 panel.width - 48, 60), self.font_small,
                               color=(180, 90, 40))

        hint = self.font_small.render("Pressione ENTER para continuar", True, DARK)
        self.screen.blit(hint, (panel.left + 24, panel.bottom - 24))
        self.draw_bee((panel.right - 110, panel.top + 10))

    # ---- tela final ---------------------------------------------------
    def render_summary(self):
        panel = pygame.Rect(50, 30, WIDTH - 100, HEIGHT - 60)
        draw_panel(self.screen, panel)
        title = self.font_title.render("O Legado da Colmeia", True, DARK)
        self.screen.blit(title, title.get_rect(center=(WIDTH // 2, panel.top + 32)))

        draw_radar(self.screen, (panel.left + 170, panel.top + 190), 105, self.harmonia,
                   self.font_small)

        x = panel.left + 350
        y = panel.top + 66
        res_title = self.font_h2.render("Recursos finais", True, DARK)
        self.screen.blit(res_title, (x, y))
        y += 26
        self.screen.blit(self.font_small.render(f"Mel: {self.mel}", True, DARK), (x, y))
        y += 20
        self.screen.blit(self.font_small.render(f"Operarias: {self.operarias}", True, DARK), (x, y))
        y += 20
        self.screen.blit(self.font_small.render(f"Relacao com a Colmeia: {self.relacao}", True, DARK), (x, y))
        y += 30

        aff_title = self.font_h2.render("Afinidade final", True, DARK)
        self.screen.blit(aff_title, (x, y))
        y += 24
        for name, data in COUNCILORS.items():
            val = self.affinity[name]
            status = ("aliada proxima" if val >= 70 else
                      "afastada" if val <= 20 else "neutra")
            line = f"{name}: {val} ({status})"
            self.screen.blit(self.font_small.render(line, True, data["color"]), (x, y))
            y += 18

        profile_name = self.dominant_councilor()
        profile_text = PROFILE_TEXTS[profile_name]
        y += 8
        p_title = self.font_h2.render(f"Perfil: {profile_name}", True, GOLD)
        self.screen.blit(p_title, (x, y))
        y += 24
        y = self.draw_wrapped(profile_text, pygame.Rect(x, y, panel.width - (x - panel.left) - 24, 110),
                               self.font_small)

        eco_rect = pygame.Rect(panel.left + 24, panel.bottom - 150, panel.width - 48, 130)
        pygame.draw.rect(self.screen, (250, 245, 230), eco_rect, border_radius=10)
        pygame.draw.rect(self.screen, GOLD, eco_rect, 2, border_radius=10)
        self.draw_wrapped(ECOLOGY_MESSAGE, pygame.Rect(eco_rect.left + 14, eco_rect.top + 10,
                                                        eco_rect.width - 28, eco_rect.height - 20),
                           self.font_small, color=(80, 60, 20), line_gap=3)

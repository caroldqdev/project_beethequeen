# -*- coding: utf-8 -*-
"""
Bee the Queen — Protótipo MVP (Ano 1: Primavera -> Verão -> Outono -> Inverno)

Fluxo por evento (conforme secao 1 do Roteiro Narrativo):
  1) Contexto narrado
  2) O Conselho se reune -> 4 propostas (uma por conselheira)
  3) O jogador escolhe
  4) Um puzzle representa a execucao da escolha
  5) O mundo reage de forma permanente (texto de consequencia)

Como rodar:
    pip install pygame
    python main.py

Setas/mouse para escolher opcoes, ESPACO para travar o puzzle,
ENTER/clique para avancar as telas de texto.
"""
import os
import sys
import textwrap
import pygame

from events_data import EVENTS, COUNCILORS, HARMONIA_AXES
from harmonia import draw_radar, draw_bar
from puzzle import PuzzleState

WIDTH, HEIGHT = 1000, 650
FPS = 60
ASSETS = os.path.join(os.path.dirname(__file__), "assets")

WHITE = (255, 255, 255)
DARK = (40, 40, 40)
PANEL_BG = (255, 255, 255, 235)
GOLD = (214, 158, 46)

STATE_INTRO = "intro"
STATE_SEASON = "season"
STATE_CONTEXT = "context"
STATE_CHOICE = "choice"
STATE_PUZZLE = "puzzle"
STATE_RESULT = "result"
STATE_SUMMARY = "summary"


def load_bee_frames():
    frames = []
    for i in range(9):
        img = pygame.image.load(os.path.join(ASSETS, f"bee_frame_{i}.png")).convert_alpha()
        frames.append(pygame.transform.scale(img, (96, 96)))
    return frames


def wrap_text(text, font, max_width):
    words = text.split(" ")
    lines, current = [], ""
    for w in words:
        trial = (current + " " + w).strip()
        if font.size(trial)[0] <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = w
    if current:
        lines.append(current)
    return lines


def draw_panel(surface, rect, radius=16, alpha=235):
    panel = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    pygame.draw.rect(panel, (255, 255, 255, alpha), panel.get_rect(), border_radius=radius)
    pygame.draw.rect(panel, (120, 120, 120, 255), panel.get_rect(), 2, border_radius=radius)
    surface.blit(panel, rect.topleft)


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Bee the Queen — Prototipo MVP")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

        self.font_title = pygame.font.SysFont("georgia", 30, bold=True)
        self.font_h2 = pygame.font.SysFont("georgia", 22, bold=True)
        self.font_body = pygame.font.SysFont("verdana", 16)
        self.font_small = pygame.font.SysFont("verdana", 13)
        self.font_btn = pygame.font.SysFont("verdana", 15, bold=True)

        self.background = pygame.transform.scale(
            pygame.image.load(os.path.join(ASSETS, "bg_scene.png")).convert(), (WIDTH, HEIGHT))
        self.bee_frames = load_bee_frames()
        self.bee_frame_idx = 0
        self.bee_timer = 0.0

        # --- estado do jogo ---
        self.harmonia = {axis: 50 for axis in HARMONIA_AXES}
        self.mel = 100
        self.operarias = 100
        self.affinity = {name: 40 for name in COUNCILORS}
        self.event_index = 0
        self.current_season = None
        self.history = []  # (evento, conselheira escolhida, resultado_puzzle)

        self.state = STATE_INTRO
        self.chosen_option = None
        self.puzzle = None
        self.result_lines = []
        self.option_rects = []

    # ---------------------------------------------------------------- utils
    def current_event(self):
        return EVENTS[self.event_index]

    def apply_choice(self, option, multiplier=1.0):
        """Aplica custo, efeitos de Harmonia e afinidade de uma escolha."""
        cost = option.get("cost", {})
        mel_cost = cost.get("mel", 0)
        if mel_cost == "all":
            self.mel = 0
        elif isinstance(mel_cost, (int, float)):
            self.mel = max(0, self.mel + mel_cost)
        oper_cost = cost.get("operarias", 0)
        if isinstance(oper_cost, (int, float)):
            self.operarias = max(0, self.operarias + oper_cost)

        applied = {}
        if option.get("mirror_axis"):
            # Evento-espelho: efeito depende do estado acumulado
            axis = option["mirror_axis"]
            if axis == "mel_reserve":
                base = 20 if self.mel >= 40 else -20
                self.harmonia["populacao"] = max(0, min(100, self.harmonia["populacao"] + int(base * multiplier)))
                applied["populacao"] = int(base * multiplier)
            else:
                current = self.harmonia.get(axis, 50)
                base = 15 if current >= 60 else (-15 if current < 40 else 3)
                self.harmonia[axis] = max(0, min(100, self.harmonia[axis] + int(base * multiplier)))
                applied[axis] = int(base * multiplier)
        else:
            for axis, delta in option.get("effects", {}).items():
                change = int(round(delta * multiplier))
                self.harmonia[axis] = max(0, min(100, self.harmonia[axis] + change))
                applied[axis] = change

        aff = option.get("affinity", {})
        chosen = option["councilor"]
        self.affinity[chosen] = max(0, min(100, self.affinity[chosen] + aff.get("self", 0)))
        for name in COUNCILORS:
            if name != chosen:
                self.affinity[name] = max(0, min(100, self.affinity[name] + aff.get("others", 0)))
        return applied

    def imbalance_warning(self):
        vals = self.harmonia.values()
        if max(vals) - min(vals) >= 45:
            return ("O painel de Harmonia esta muito desequilibrado -- em sprints futuros "
                    "isso desencadeia eventos de correcao automatica (ex.: pragas por "
                    "excesso de Producao sem Biodiversidade).")
        return None

    # --------------------------------------------------------------- estados
    def start_event(self):
        ev = self.current_event()
        if ev["season"] != self.current_season:
            self.current_season = ev["season"]
            self.state = STATE_SEASON
        else:
            self.state = STATE_CONTEXT

    def go_to_choice(self):
        self.state = STATE_CHOICE

    def choose_option(self, option):
        self.chosen_option = option
        puzzle_name = option.get("puzzle")
        if puzzle_name:
            rect = pygame.Rect(0, 0, 560, 40)
            rect.center = (WIDTH // 2, 430)
            self.puzzle = PuzzleState(rect)
            self.state = STATE_PUZZLE
        else:
            self.resolve_choice(multiplier=1.0)

    def resolve_choice(self, multiplier):
        applied = self.apply_choice(self.chosen_option, multiplier)
        ev = self.current_event()
        self.history.append((ev["title"], self.chosen_option["councilor"], multiplier))
        lines = []
        for axis, change in applied.items():
            sign = "+" if change >= 0 else ""
            lines.append(f"{axis.capitalize()}: {sign}{change}")
        self.result_lines = lines
        self.state = STATE_RESULT

    def next_event(self):
        self.event_index += 1
        if self.event_index >= len(EVENTS):
            self.state = STATE_SUMMARY
        else:
            self.start_event()

    # ----------------------------------------------------------------- draw
    def draw_bee(self, pos):
        self.screen.blit(self.bee_frames[self.bee_frame_idx], pos)

    def draw_hud(self):
        draw_panel(self.screen, pygame.Rect(16, 16, 300, 96))
        mel_label = self.font_small.render(f"Mel: {self.mel}", True, DARK)
        oper_label = self.font_small.render(f"Operarias: {self.operarias}", True, DARK)
        self.screen.blit(mel_label, (30, 26))
        draw_bar(self.screen, (30, 44), (270, 14), self.mel, 150, GOLD)
        self.screen.blit(oper_label, (30, 66))
        draw_bar(self.screen, (30, 84), (270, 14), self.operarias, 150, (120, 170, 90))

        draw_panel(self.screen, pygame.Rect(WIDTH - 316, 16, 300, 130))
        title = self.font_small.render("Afinidade das Conselheiras", True, DARK)
        self.screen.blit(title, (WIDTH - 300, 24))
        for i, (name, data) in enumerate(COUNCILORS.items()):
            y = 46 + i * 22
            label = self.font_small.render(name, True, DARK)
            self.screen.blit(label, (WIDTH - 300, y))
            draw_bar(self.screen, (WIDTH - 210, y + 2), (190, 12),
                     self.affinity[name], 100, data["color"])

    def draw_wrapped(self, text, rect, font, color=DARK, line_gap=6):
        lines = []
        for para in text.split("\n"):
            lines.extend(wrap_text(para, font, rect.width))
        y = rect.top
        for line in lines:
            surf = font.render(line, True, color)
            self.screen.blit(surf, (rect.left, y))
            y += font.get_height() + line_gap
        return y

    def draw_button(self, rect, text, hover=False):
        color = (255, 230, 150) if hover else (255, 245, 220)
        pygame.draw.rect(self.screen, color, rect, border_radius=10)
        pygame.draw.rect(self.screen, GOLD, rect, 2, border_radius=10)
        lines = wrap_text(text, self.font_btn, rect.width - 20)
        total_h = len(lines) * (self.font_btn.get_height() + 2)
        y = rect.centery - total_h // 2
        for line in lines:
            surf = self.font_btn.render(line, True, DARK)
            r = surf.get_rect(center=(rect.centerx, y + surf.get_height() // 2))
            self.screen.blit(surf, r)
            y += surf.get_height() + 2

    # ---------------------------------------------------------------- frames
    def render(self, mouse_pos):
        self.screen.blit(self.background, (0, 0))
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((255, 255, 255, 40))
        self.screen.blit(overlay, (0, 0))

        if self.state == STATE_INTRO:
            self.render_intro()
        elif self.state == STATE_SEASON:
            self.render_season()
        elif self.state == STATE_CONTEXT:
            self.render_context()
        elif self.state == STATE_CHOICE:
            self.render_choice(mouse_pos)
        elif self.state == STATE_PUZZLE:
            self.render_puzzle()
        elif self.state == STATE_RESULT:
            self.render_result()
        elif self.state == STATE_SUMMARY:
            self.render_summary()

        pygame.display.flip()

    def render_intro(self):
        draw_panel(self.screen, pygame.Rect(80, 90, WIDTH - 160, HEIGHT - 180))
        title = self.font_title.render("BEE THE QUEEN", True, DARK)
        self.screen.blit(title, title.get_rect(center=(WIDTH // 2, 140)))
        sub = self.font_h2.render("Prototipo MVP - Ano 1", True, GOLD)
        self.screen.blit(sub, sub.get_rect(center=(WIDTH // 2, 178)))
        body = ("A Rainha Ancia se aposenta e escolhe voce como sucessora.\n"
                "Voce governa por 4 estacoes, apoiada por quatro conselheiras:\n"
                "Flora, Melina, Nectar e Aurora. Cada escolha altera o painel de\n"
                "Harmonia da Colmeia, consome recursos e muda a afinidade das\n"
                "conselheiras. Nao existe final unico -- existe o reino que voce\n"
                "construir.\n\nPressione ENTER para comecar.")
        self.draw_wrapped(body, pygame.Rect(120, 220, WIDTH - 240, 300), self.font_body)
        self.draw_bee((WIDTH // 2 - 48, HEIGHT - 150))

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
        self.screen.blit(header, header.get_rect(center=(WIDTH // 2, 150)))

        self.option_rects = []
        n = len(ev["options"])
        card_w, card_h = 470, 150
        gap_x, gap_y = 20, 16
        cols = 2
        start_x = WIDTH // 2 - (cols * card_w + gap_x) // 2
        start_y = 180
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
            cost_str = "  ".join(cost_txt) if cost_txt else "Sem custo direto"
            cost_surf = self.font_small.render(cost_str, True, (110, 90, 40))
            self.screen.blit(cost_surf, (rect.left + 14, rect.top + 34))
            self.draw_wrapped(opt["action"], pygame.Rect(rect.left + 14, rect.top + 54,
                                                           rect.width - 28, 90),
                               self.font_small, color=DARK, line_gap=3)
            self.option_rects.append((rect, opt))

    def render_puzzle(self):
        ev = self.current_event()
        opt = self.chosen_option
        draw_panel(self.screen, pygame.Rect(70, 130, WIDTH - 140, 380))
        header = self.font_h2.render(f"Execucao: {opt.get('puzzle') or 'Acao direta'}", True, DARK)
        self.screen.blit(header, header.get_rect(center=(WIDTH // 2, 170)))
        sub = self.font_small.render(
            f"{opt['councilor']} propos: {opt['action']}", True, (90, 90, 90))
        self.draw_wrapped(sub.get_rect() and opt['action'], pygame.Rect(120, 200, WIDTH - 240, 60),
                           self.font_small)
        instructions = self.font_body.render(
            "Pressione ESPACO para travar o marcador na zona verde (sucesso) ou amarela (parcial).",
            True, DARK)
        self.screen.blit(instructions, instructions.get_rect(center=(WIDTH // 2, 300)))
        self.puzzle.draw(self.screen)
        if self.puzzle.done:
            result_txt = {
                "sucesso": "Execucao bem-sucedida! Efeito completo.",
                "parcial": "Execucao parcial. Metade do efeito.",
                "falha": "A execucao falhou. Apenas 25% do efeito, custo pago integralmente.",
            }[self.puzzle.result]
            r = self.font_h2.render(result_txt, True, GOLD)
            self.screen.blit(r, r.get_rect(center=(WIDTH // 2, 470)))
            hint = self.font_small.render("Pressione ENTER para continuar", True, DARK)
            self.screen.blit(hint, hint.get_rect(center=(WIDTH // 2, 500)))
        self.draw_bee((WIDTH - 160, 150))

    def render_result(self):
        ev = self.current_event()
        opt = self.chosen_option
        self.draw_hud()
        panel = pygame.Rect(90, 150, WIDTH - 180, 360)
        draw_panel(self.screen, panel)
        header = self.font_h2.render(f"Consequencia: {ev['title']}", True, DARK)
        self.screen.blit(header, (panel.left + 24, panel.top + 20))

        eff_str = "   ".join(self.result_lines) if self.result_lines else "(efeito condicional)"
        eff_surf = self.font_body.render(f"Efeitos na Harmonia: {eff_str}", True, GOLD)
        self.screen.blit(eff_surf, (panel.left + 24, panel.top + 60))

        extra = opt.get("extra")
        y = panel.top + 90
        if extra:
            y = self.draw_wrapped(extra, pygame.Rect(panel.left + 24, y, panel.width - 48, 40),
                                   self.font_small, color=(90, 70, 30))
            y += 10

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

    def render_summary(self):
        panel = pygame.Rect(60, 40, WIDTH - 120, HEIGHT - 80)
        draw_panel(self.screen, panel)
        title = self.font_title.render("O Legado da Colmeia", True, DARK)
        self.screen.blit(title, title.get_rect(center=(WIDTH // 2, panel.top + 40)))

        draw_radar(self.screen, (panel.left + 200, panel.top + 230), 130, self.harmonia,
                   self.font_small)

        x = panel.left + 420
        y = panel.top + 90
        res_title = self.font_h2.render("Recursos finais", True, DARK)
        self.screen.blit(res_title, (x, y))
        y += 32
        self.screen.blit(self.font_body.render(f"Mel: {self.mel}", True, DARK), (x, y))
        y += 26
        self.screen.blit(self.font_body.render(f"Operarias: {self.operarias}", True, DARK), (x, y))
        y += 40

        aff_title = self.font_h2.render("Afinidade final", True, DARK)
        self.screen.blit(aff_title, (x, y))
        y += 32
        for name, data in COUNCILORS.items():
            val = self.affinity[name]
            status = ("aliada proxima" if val >= 70 else
                      "afastada" if val <= 20 else "neutra")
            line = f"{name}: {val} ({status})"
            self.screen.blit(self.font_body.render(line, True, data["color"]), (x, y))
            y += 26

        dominant = max(self.harmonia, key=self.harmonia.get)
        weakest = min(self.harmonia, key=self.harmonia.get)
        legacy = (f"Sua colmeia se destacou em {dominant} e ficou mais fragil em {weakest}. "
                  f"Nao existe final unico -- este e o reino que voce construiu.")
        self.draw_wrapped(legacy, pygame.Rect(panel.left + 40, panel.bottom - 90,
                                               panel.width - 80, 60), self.font_body)
        self.draw_bee((panel.right - 130, panel.bottom - 130))

    # ----------------------------------------------------------------- input
    def handle_event(self, event, mouse_pos):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if self.state == STATE_INTRO and event.key == pygame.K_RETURN:
                self.start_event()
            elif self.state == STATE_SEASON and event.key == pygame.K_RETURN:
                self.state = STATE_CONTEXT
            elif self.state == STATE_CONTEXT and event.key == pygame.K_RETURN:
                self.go_to_choice()
            elif self.state == STATE_PUZZLE:
                if event.key == pygame.K_SPACE:
                    self.puzzle.lock()
                elif event.key == pygame.K_RETURN and self.puzzle.done:
                    self.resolve_choice(self.puzzle.effect_multiplier())
            elif self.state == STATE_RESULT and event.key == pygame.K_RETURN:
                self.next_event()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.state == STATE_CHOICE:
                for rect, opt in self.option_rects:
                    if rect.collidepoint(mouse_pos):
                        self.choose_option(opt)
                        break

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

            if self.state == STATE_PUZZLE and self.puzzle is not None:
                self.puzzle.update(dt)

            self.render(mouse_pos)


if __name__ == "__main__":
    Game().run()

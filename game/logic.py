# -*- coding: utf-8 -*-
"""
Regras do jogo: tudo que muda numeros (Mel, Operarias, Relacao, Harmonia,
Afinidade) e decide para qual tela ir em seguida. NADA aqui desenha na tela
-- para isso, veja game/screens.py.

Este modulo define GameLogic, que e "misturado" (mixin) na classe Game
final, em game/core.py. Ele espera encontrar em `self` os atributos criados
la (self.mel, self.harmonia, self.state, etc.).
"""
import pygame

from data import COUNCILORS, FAIL_PENALTY
from puzzles import make_puzzle
from .constants import (STATE_SEASON, STATE_CONTEXT, STATE_CHOICE,
                         STATE_PUZZLE_BRIEFING, STATE_PUZZLE,
                         STATE_PUZZLE_RESULT, STATE_RESULT, STATE_SUMMARY,
                         BRIEFING_TIME, SEASON_DIFFICULTY, WIDTH)


class GameLogic:
    # ---------------------------------------------------------------- utils
    def current_event(self):
        return self.EVENTS[self.event_index]

    def production_penalty_active(self):
        return self.relacao < 25

    def apply_choice(self, option, multiplier=1.0):
        """Aplica custo, efeitos de Harmonia, Relacao e afinidade de uma escolha."""
        cost = option.get("cost", {})
        mel_cost = cost.get("mel", 0)
        if mel_cost == "all":
            self.mel = 0
        elif isinstance(mel_cost, (int, float)):
            self.mel = max(0, self.mel + int(round(mel_cost * multiplier if mel_cost < 0 else mel_cost)))
        oper_cost = cost.get("operarias", 0)
        if isinstance(oper_cost, (int, float)):
            self.operarias = max(0, self.operarias + int(round(oper_cost * multiplier if oper_cost < 0 else oper_cost)))
        relacao_cost = cost.get("relacao", 0)
        if isinstance(relacao_cost, (int, float)):
            self.relacao = max(0, min(100, self.relacao + int(round(relacao_cost))))

        applied = {}
        if option.get("mirror_axis"):
            axis = option["mirror_axis"]
            if axis == "mel_reserve":
                base = 20 if self.mel >= 40 else -20
                self.harmonia["populacao"] = max(0, min(100, self.harmonia["populacao"] + int(base * multiplier)))
                applied["populacao"] = int(base * multiplier)
            elif axis == "relacao":
                base = 20 if self.relacao >= 60 else -20
                self.harmonia["populacao"] = max(0, min(100, self.harmonia["populacao"] + int(base * multiplier)))
                applied["populacao (via relacao)"] = int(base * multiplier)
            else:
                current = self.harmonia.get(axis, 50)
                base = 15 if current >= 60 else (-15 if current < 40 else 3)
                self.harmonia[axis] = max(0, min(100, self.harmonia[axis] + int(base * multiplier)))
                applied[axis] = int(base * multiplier)
        else:
            for axis, delta in option.get("effects", {}).items():
                change = int(round(delta * multiplier))
                # Relacao baixa penaliza producao positiva (Guia 2, sec.1)
                if axis == "producao" and change > 0 and self.production_penalty_active():
                    change = int(round(change * 0.85))
                # Penalidade da Aurora: proximo ganho de cooperacao vale metade
                if axis == "cooperacao" and change > 0 and self.next_cooperacao_multiplier < 1.0:
                    change = int(round(change * self.next_cooperacao_multiplier))
                    self.next_cooperacao_multiplier = 1.0
                self.harmonia[axis] = max(0, min(100, self.harmonia[axis] + change))
                applied[axis] = change

        aff = option.get("affinity", {})
        chosen = option["councilor"]
        self.affinity[chosen] = max(0, min(100, self.affinity[chosen] + aff.get("self", 0)))
        for name in COUNCILORS:
            if name != chosen:
                self.affinity[name] = max(0, min(100, self.affinity[name] + aff.get("others", 0)))
        return applied

    def apply_fail_penalty(self, councilor):
        """Penalidade extra ao falhar no minigame (Guia 2, sec.3)."""
        pen = FAIL_PENALTY.get(councilor)
        if not pen:
            return None
        if "operarias" in pen:
            self.operarias = max(0, self.operarias + pen["operarias"])
        if "mel" in pen:
            self.mel = max(0, self.mel + pen["mel"])
        if "relacao" in pen:
            self.relacao = max(0, min(100, self.relacao + pen["relacao"]))
        if "weaken_next_cooperacao" in pen:
            self.next_cooperacao_multiplier = pen["weaken_next_cooperacao"]
        return pen.get("text")

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
        self.fail_penalty_text = None
        puzzle_name = option.get("puzzle")
        if puzzle_name:
            self.pending_puzzle_name = puzzle_name
            self.pending_difficulty = SEASON_DIFFICULTY.get(self.current_event()["season"], 1)
            self.puzzle = None
            self.briefing_timer = BRIEFING_TIME
            self.state = STATE_PUZZLE_BRIEFING
        else:
            self.resolve_choice(multiplier=1.0)

    def start_puzzle(self):
        rect = pygame.Rect(0, 0, 620, 260)
        rect.center = (WIDTH // 2, 360)
        self.puzzle = make_puzzle(self.pending_puzzle_name, rect,
                                   difficulty=self.pending_difficulty, relacao=self.relacao)
        self.state = STATE_PUZZLE

    def resolve_choice(self, multiplier):
        # Bonus de dialogo se relacao alta (Guia 2, sec.1): +10% no efeito
        if self.relacao > 80 and multiplier >= 1.0:
            multiplier *= 1.1
        if multiplier < 1.0:
            councilor = self.chosen_option["councilor"]
            self.fail_penalty_text = self.apply_fail_penalty(councilor)
        applied = self.apply_choice(self.chosen_option, multiplier)
        ev = self.current_event()
        self.history.append((ev["title"], self.chosen_option["councilor"], multiplier))
        lines = []
        for axis, change in applied.items():
            sign = "+" if change >= 0 else ""
            lines.append(f"{str(axis).capitalize()}: {sign}{change}")
        self.result_lines = lines
        if self.chosen_option.get("puzzle"):
            self.state = STATE_PUZZLE_RESULT
        else:
            self.state = STATE_RESULT

    def next_event(self):
        self.event_index += 1
        if self.event_index >= len(self.EVENTS):
            self.state = STATE_SUMMARY
        else:
            self.start_event()

    def dominant_councilor(self):
        max_val = max(self.affinity.values())
        top = [n for n, v in self.affinity.items() if v == max_val]
        if len(top) > 1 or (max(self.affinity.values()) - min(self.affinity.values())) < 15:
            return "Equilibrado"
        return top[0]

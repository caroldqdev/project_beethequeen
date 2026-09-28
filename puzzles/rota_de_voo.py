# -*- coding: utf-8 -*-
"""Rota de Voo (Nectar, Evento 1 — O Novo Jardim).

Estilo "Zip": arraste de flor em flor, preenchendo TODAS as celulas do
campo sem repetir nenhuma, passando pelos pontos numerados em ordem
crescente. Algumas celulas sao barreiras (intransponiveis).

Como jogar:
  - Clique na flor numero 1 para comecar.
  - Arraste (mantendo o botao pressionado) para celulas vizinhas
    (cima/baixo/esquerda/direita) ainda nao visitadas.
  - Os pontos numerados so podem ser visitados na ordem certa.
  - Complete cobrindo TODAS as celulas e terminando no ultimo numero.
  - Tecla R reinicia a tentativa (o tempo total continua contando).

Regras de resultado (tempo total ate completar):
  - < 2 minutos            -> sucesso (sucesso total)
  - 2 a 5 minutos          -> parcial (sucesso)
  - > 5 minutos ou nao completou -> falha
"""
import random
import pygame

from .base import BasePuzzle, TARGET_BAD, TEXT_DARK

DIRS = [(1, 0), (-1, 0), (0, 1), (0, -1)]

CELL_EMPTY = (235, 235, 225)
CELL_VISITED = (240, 200, 60)
CELL_BARRIER = (90, 90, 90)
CELL_HEAD = (214, 158, 46)
CHECKPOINT_DONE = (120, 190, 110)
CHECKPOINT_NEXT = (230, 150, 60)
CHECKPOINT_FUTURE = (140, 150, 200)


def _neighbors(cell, cell_set, visited):
    x, y = cell
    return [(x + dx, y + dy) for dx, dy in DIRS
            if (x + dx, y + dy) in cell_set and (x + dx, y + dy) not in visited]


def _degree(cell, cell_set, visited):
    return len(_neighbors(cell, cell_set, visited))


def _dfs_hamiltonian(path, visited, cell_set, total):
    if len(path) == total:
        return True
    neighbors = _neighbors(path[-1], cell_set, visited)
    # heuristica de Warnsdorff: tenta primeiro quem tem menos opcoes futuras
    neighbors.sort(key=lambda n: _degree(n, cell_set, visited))
    for n in neighbors:
        visited.add(n)
        path.append(n)
        if _dfs_hamiltonian(path, visited, cell_set, total):
            return True
        path.pop()
        visited.remove(n)
    return False


def _serpentine_path(cols, rows):
    """Caminho garantido (cobre a grade inteira, sem barreiras) -- usado
    como reserva caso a geracao aleatoria com barreiras falhe."""
    path = []
    for y in range(rows):
        xs = range(cols) if y % 2 == 0 else range(cols - 1, -1, -1)
        for x in xs:
            path.append((x, y))
    return path


def _generate_path_and_barriers(cols, rows, n_barriers, max_tries=60):
    all_cells = [(x, y) for y in range(rows) for x in range(cols)]
    for _ in range(max_tries):
        barriers = set(random.sample(all_cells, n_barriers)) if n_barriers else set()
        cell_set = set(c for c in all_cells if c not in barriers)
        start = random.choice(list(cell_set))
        visited = {start}
        path = [start]
        if _dfs_hamiltonian(path, visited, cell_set, len(cell_set)):
            return path, barriers
    # reserva: sem barreiras, caminho em zigue-zague garantido
    return _serpentine_path(cols, rows), set()


class RotaDeVoo(BasePuzzle):
    name = "Rota de Voo"

    def __init__(self, rect, difficulty=1, relacao=100):
        self.rect = rect
        self.difficulty = difficulty
        self.done = False
        self.result = None

        d = max(1, min(5, difficulty))
        self.cols = 4 + d // 2       # 4..6
        self.rows = 3 + d // 3       # 3..4
        n_barriers = max(0, d - 2)   # 0..3

        self.path_solution, self.barriers = _generate_path_and_barriers(
            self.cols, self.rows, n_barriers)
        self.total_cells = len(self.path_solution)

        # escolhe de 4 a 6 pontos numerados, sempre incluindo inicio e fim
        n_checkpoints = min(6, max(4, self.total_cells // 4))
        n_checkpoints = min(n_checkpoints, self.total_cells)
        idxs = sorted(set(round(i * (self.total_cells - 1) / (n_checkpoints - 1))
                           for i in range(n_checkpoints)))
        self.checkpoint_cell_of_number = {}
        self.checkpoint_number_of_cell = {}
        for num, idx in enumerate(idxs, start=1):
            cell = self.path_solution[idx]
            self.checkpoint_cell_of_number[num] = cell
            self.checkpoint_number_of_cell[cell] = num
        self.total_checkpoints = len(idxs)
        self.final_cell = self.path_solution[-1]

        cell_w = rect.width / self.cols
        cell_h = rect.height / self.rows
        self.cell_size = (cell_w, cell_h)

        self.player_path = []
        self.visited = set()
        self.next_checkpoint = 1
        self.dragging = False
        self.elapsed = 0.0
        self.max_time = 300.0  # 5 minutos

    # ------------------------------------------------------------ helpers
    def _cell_at(self, pos):
        gx = int((pos[0] - self.rect.left) // self.cell_size[0])
        gy = int((pos[1] - self.rect.top) // self.cell_size[1])
        if 0 <= gx < self.cols and 0 <= gy < self.rows:
            return gx, gy
        return None

    def _cell_center(self, cell):
        gx, gy = cell
        cw, ch = self.cell_size
        return (self.rect.left + gx * cw + cw / 2, self.rect.top + gy * ch + ch / 2)

    def _reset_attempt(self):
        self.player_path = []
        self.visited = set()
        self.next_checkpoint = 1
        self.dragging = False

    # ------------------------------------------------------------- update
    def update(self, dt):
        if self.done:
            return
        self.elapsed += dt
        if self.elapsed >= self.max_time:
            self.result = "falha"
            self.done = True

    def handle_key(self, key):
        if key == pygame.K_r and not self.done:
            self._reset_attempt()

    def handle_click(self, pos):
        if self.done:
            return
        cell = self._cell_at(pos)
        if cell is None or cell in self.barriers:
            return
        if not self.player_path:
            if cell == self.checkpoint_cell_of_number[1]:
                self.player_path = [cell]
                self.visited = {cell}
                self.next_checkpoint = 2
                self.dragging = True
        elif cell == self.player_path[-1]:
            self.dragging = True  # retomar o arrasto de onde parou

    def handle_drag(self, pos, pressed):
        if self.done or not pressed or not self.dragging or not self.player_path:
            return
        cell = self._cell_at(pos)
        if cell is None or cell in self.barriers or cell in self.visited:
            return
        last = self.player_path[-1]
        if abs(cell[0] - last[0]) + abs(cell[1] - last[1]) != 1:
            return  # nao e vizinho ortogonal
        checkpoint_num = self.checkpoint_number_of_cell.get(cell)
        if checkpoint_num is not None and checkpoint_num != self.next_checkpoint:
            return  # ponto fora de ordem -- bloqueado
        self.player_path.append(cell)
        self.visited.add(cell)
        if checkpoint_num is not None:
            self.next_checkpoint += 1
        if len(self.player_path) == self.total_cells and cell == self.final_cell:
            self._finish_success()

    def handle_release(self, pos):
        self.dragging = False

    def _finish_success(self):
        self.done = True
        if self.elapsed < 120:
            self.result = "sucesso"
        elif self.elapsed <= 300:
            self.result = "parcial"
        else:
            self.result = "falha"

    # --------------------------------------------------------------- draw
    def draw(self, surface):
        pygame.draw.rect(surface, (150, 150, 150), self.rect, 2, border_radius=8)
        cw, ch = self.cell_size
        for gy in range(self.rows):
            for gx in range(self.cols):
                cell = (gx, gy)
                x = self.rect.left + gx * cw
                y = self.rect.top + gy * ch
                cell_rect = pygame.Rect(x + 1, y + 1, cw - 2, ch - 2)
                if cell in self.barriers:
                    pygame.draw.rect(surface, CELL_BARRIER, cell_rect, border_radius=4)
                    continue
                color = CELL_VISITED if cell in self.visited else CELL_EMPTY
                pygame.draw.rect(surface, color, cell_rect, border_radius=4)

        # trilha (linha conectando o caminho ja percorrido)
        if len(self.player_path) > 1:
            points = [self._cell_center(c) for c in self.player_path]
            pygame.draw.lines(surface, (180, 140, 40), False, points, 4)

        font_num = pygame.font.SysFont("verdana", 14, bold=True)
        for num, cell in self.checkpoint_cell_of_number.items():
            cx, cy = self._cell_center(cell)
            if num < self.next_checkpoint:
                color = CHECKPOINT_DONE
            elif num == self.next_checkpoint:
                color = CHECKPOINT_NEXT
            else:
                color = CHECKPOINT_FUTURE
            pygame.draw.circle(surface, color, (int(cx), int(cy)), 13)
            label = font_num.render(str(num), True, (255, 255, 255))
            surface.blit(label, label.get_rect(center=(cx, cy)))

        if self.player_path:
            hx, hy = self._cell_center(self.player_path[-1])
            pygame.draw.circle(surface, CELL_HEAD, (int(hx), int(hy)), 7)

        font = pygame.font.SysFont("verdana", 13)
        pct = len(self.player_path) / max(1, self.total_cells) * 100
        txt = font.render(
            f"Arraste da flor 1 ate a {self.total_checkpoints}, cobrindo tudo  "
            f"({pct:.0f}% do campo)  Tempo: {self.elapsed:.0f}s  [R] reiniciar tentativa",
            True, TEXT_DARK)
        surface.blit(txt, (self.rect.left, self.rect.bottom + 16))

# -*- coding: utf-8 -*-
"""Sob as Folhas (Flora, Evento 1 — O Novo Jardim).

O chão está coberto por várias camadas de folhas, empilhadas umas sobre as
outras. Embaixo das de cima se escondem 6 bichos, e embaixo de cada bicho
também há folhas. O objetivo é LIMPAR O CHÃO, tirando TODAS as folhas, o mais
rápido possível, sem clicar nos bichos.

Como funciona um clique: vale o que estiver por CIMA no ponto clicado.
  - uma folha        -> ela sai
  - um bicho         -> o bicho é atingido (cada bicho conta uma vez)
  - nada             -> não acontece nada
As folhas que ficam embaixo de um bicho só saem se você clicar na parte delas
que está FORA da área do bicho. O jogo garante, ao montar cada rodada, que isso
é sempre possível.

Regras de resultado:
  - Tirou todas as folhas, 0 bichos atingidos        -> sucesso
  - Tirou todas as folhas, 1 a 3 bichos atingidos    -> parcial
  - Tirou todas as folhas, 4+ bichos atingidos       -> falha
  - O tempo acabou com folhas sobrando               -> falha

OS DESENHOS vêm da pasta assets/ do projeto, feitos no Aseprite:
    Folha.ase, Borboleta.ase, Joaninha.ase, Vespa.ase, Pernilongo.ase, Minhoca.ase
Se algum não estiver lá, o jogo avisa no terminal e usa um desenho provisório.
"""
import math
import os
import random

import pygame

from . import aseprite
from .base import BasePuzzle, difficulty_scale, TEXT_DARK

# ============================================================
# AJUSTES -- mexa aqui para balancear e para trocar o visual
# ============================================================
# --- os desenhos ---
PASTA_DOS_DESENHOS = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "assets")
ARQUIVO_DA_FOLHA = "Folha.ase"
# (nome do arquivo sem .ase, quantos) -- ficam em lugares sorteados
BICHOS = [("Borboleta", 1), ("Joaninha", 2), ("Vespa", 1), ("Pernilongo", 1), ("Minhoca", 1)]
TAMANHO_DA_FOLHA = 72            # largura aproximada de cada folha na tela, em pixels
TAMANHO_DOS_BICHOS = {"Borboleta": 52, "Joaninha": 36, "Vespa": 48, "Pernilongo": 44, "Minhoca": 56}
TAMANHO_PADRAO_DE_BICHO = 44     # para um bicho que não esteja na lista acima
GIRAR_BICHOS = False             # True = cada bicho aparece virado de um jeito (se o desenho é visto de cima)

# --- a dificuldade (o primeiro valor é o do mais fácil, o segundo o do mais difícil) ---
CAMADAS_DE_CIMA = 2              # camadas de folhas ACIMA dos bichos (mais 1 embaixo deles)
FOLHAS_POR_CAMADA = (20, 32)     # quantas folhas em cada camada
FOLHAS_EMBAIXO_DE_CADA_BICHO = 2
TEMPO_EM_SEGUNDOS = (30.0, 23.0)

# --- a regra dos bichos ---
FOLGA_DO_BICHO = 2               # pixels além do desenho que também contam como "clicou no bicho"
COBERTURA_MINIMA = 0.90          # quanto de cada bicho as folhas de cima escondem no começo
SOBRA_MINIMA_DA_FOLHA = 0.15     # quanto de uma folha de baixo tem que ficar clicável (fora do bicho)

# --- o visual ---
SOMBRA_DAS_FOLHAS = 70           # 0 a 255; 0 = sem sombra
ESCURECER_CAMADAS_DE_BAIXO = 0.38  # quanto as camadas de baixo ficam mais escuras (0 = nada)
COR_DO_CHAO = (92, 64, 44)
COR_DA_BORDA = (60, 42, 30)

TOTAL_INSECTS = sum(quantidade for _, quantidade in BICHOS)
_AVISADOS = set()


# ============================================================
# os desenhos: do Aseprite, ou provisórios
# ============================================================
def _desenho(nome):
    """A animação de `nome` (sem a extensão): o .ase da pasta de desenhos, ou um provisório."""
    caminho = os.path.join(PASTA_DOS_DESENHOS, nome + ".ase")
    try:
        return aseprite.carregar(caminho)
    except ValueError as erro:
        if caminho not in _AVISADOS:
            _AVISADOS.add(caminho)
            print(f"AVISO: Sob as Folhas: {erro}; usando um desenho provisório de {nome}.")
        return _provisorio(nome)


def _provisorio(nome):
    """Um desenho simples (pixel art) pra o jogo funcionar mesmo sem os arquivos."""
    def folha():
        s = pygame.Surface((16, 16), pygame.SRCALPHA)
        pygame.draw.ellipse(s, (60, 110, 45), (1, 3, 14, 10))
        pygame.draw.ellipse(s, (96, 160, 62), (2, 4, 12, 7))
        pygame.draw.line(s, (60, 110, 45), (2, 12), (14, 5), 1)
        pygame.draw.line(s, (130, 190, 90), (4, 10), (12, 6), 1)
        return [s]

    def borboleta():
        quadros = []
        for aberta in (True, False):
            s = pygame.Surface((16, 14), pygame.SRCALPHA)
            largura = 6 if aberta else 3
            for lado in (-1, 1):
                x = 8 + lado * largura // 2
                pygame.draw.ellipse(s, (230, 120, 40), (x - largura // 2 - 1, 2, largura + 1, 6))
                pygame.draw.ellipse(s, (245, 190, 70), (x - largura // 2 - 1, 7, largura, 5))
            pygame.draw.rect(s, (50, 35, 30), (7, 3, 2, 9))
            quadros.append(s)
        return quadros

    def joaninha():
        s = pygame.Surface((12, 12), pygame.SRCALPHA)
        pygame.draw.ellipse(s, (200, 40, 40), (1, 2, 10, 9))
        pygame.draw.circle(s, (30, 30, 30), (6, 2), 2)
        pygame.draw.line(s, (30, 30, 30), (6, 3), (6, 10), 1)
        for p in ((3, 5), (8, 5), (4, 8), (8, 8)):
            s.set_at(p, (30, 30, 30))
        return [s]

    def vespa():
        quadros = []
        for abertas in (True, False):
            s = pygame.Surface((16, 12), pygame.SRCALPHA)
            if abertas:
                pygame.draw.ellipse(s, (200, 220, 240, 170), (3, 0, 6, 5))
                pygame.draw.ellipse(s, (200, 220, 240, 170), (8, 1, 6, 4))
            pygame.draw.ellipse(s, (235, 190, 30), (1, 4, 14, 6))
            for x in (5, 9):
                pygame.draw.rect(s, (40, 30, 20), (x, 4, 2, 6))
            pygame.draw.circle(s, (40, 30, 20), (13, 7), 2)
            quadros.append(s)
        return quadros

    def pernilongo():
        quadros = []
        for t in (0, 1):
            s = pygame.Surface((16, 14), pygame.SRCALPHA)
            pygame.draw.line(s, (60, 60, 60), (3, 7), (12, 7), 2)
            pygame.draw.line(s, (60, 60, 60), (12, 7), (15, 9), 1)
            for x in (5, 7, 9):
                pygame.draw.line(s, (80, 80, 80), (x, 8), (x - 2 + 4 * t, 13), 1)
            pygame.draw.ellipse(s, (210, 225, 240, 190), (4, 1 + t, 7, 4))
            quadros.append(s)
        return quadros

    def minhoca():
        s = pygame.Surface((20, 8), pygame.SRCALPHA)
        for i in range(9):
            y = 4 + int(2 * math.sin(i * 0.9))
            pygame.draw.rect(s, (226, 142, 140) if i % 2 == 0 else (206, 112, 112), (1 + i * 2, y - 1, 3, 3))
        return [s]

    fabricas = {"Folha": folha, "Borboleta": borboleta, "Joaninha": joaninha, "Vespa": vespa,
                "Pernilongo": pernilongo, "Minhoca": minhoca}
    quadros = fabricas.get(nome, joaninha)()
    return aseprite.Animacao(quadros, [250] * len(quadros), quadros[0].get_size())


def _ampliar_para(animacao, alvo):
    """Faz o desenho ter cerca de `alvo` pixels no lado maior: ampliando por um número
    inteiro (pixel art, sem borrar) ou, se for grande demais, reduzindo."""
    razao = alvo / max(animacao.tamanho)
    if razao >= 1:
        return animacao.ampliada(round(razao))
    quadros = [pygame.transform.smoothscale(q, (max(1, round(q.get_width() * razao)), max(1, round(q.get_height() * razao))))
               for q in animacao.quadros]
    return aseprite.Animacao(quadros, list(animacao.duracoes), quadros[0].get_size())


def _mascara(imagem, limite=1):
    return pygame.mask.from_surface(imagem, limite)


def _sombra(mascara, alfa):
    if alfa <= 0:
        return None
    return mascara.to_surface(setcolor=(15, 10, 5, alfa), unsetcolor=(0, 0, 0, 0))


def _escurecida(imagem, fator):
    cinza = int(255 * fator)
    nova = imagem.copy()
    nova.fill((cinza, cinza, cinza, 255), special_flags=pygame.BLEND_RGBA_MULT)
    return nova


class _Folha:
    __slots__ = ("camada", "imagem", "sombra", "mascara", "rect")

    def __init__(self, camada, virada, centro):
        self.camada = camada
        self.imagem, self.sombra, self.mascara = virada
        self.rect = self.imagem.get_rect(center=(int(centro[0]), int(centro[1])))

    def cobre(self, pos):
        x, y = pos[0] - self.rect.x, pos[1] - self.rect.y
        return 0 <= x < self.rect.width and 0 <= y < self.rect.height and bool(self.mascara.get_at((x, y)))


class _Bicho:
    def __init__(self, nome, animacao, centro, fase):
        self.nome = nome
        self.animacao = animacao
        self.fase = fase
        self.atingido = False
        self.tremor = 0.0
        self.rect = animacao.quadros[0].get_rect(center=(int(centro[0]), int(centro[1])))
        self.mascara_visivel = _mascara(animacao.quadros[0])
        # a "área do bicho": o desenho de todos os quadros, um pouco engordado
        n = FOLGA_DO_BICHO
        area = pygame.mask.Mask((self.rect.width + 2 * n, self.rect.height + 2 * n))
        for quadro in animacao.quadros:
            m = _mascara(quadro)
            for dx in range(-n, n + 1):
                for dy in range(-n, n + 1):
                    if dx * dx + dy * dy <= n * n + 1:
                        area.draw(m, (n + dx, n + dy))
        self.mascara_da_area = area
        self.canto_da_area = (self.rect.x - n, self.rect.y - n)
        self._vermelhos = {}

    def na_area(self, pos):
        x, y = pos[0] - self.canto_da_area[0], pos[1] - self.canto_da_area[1]
        w, h = self.mascara_da_area.get_size()
        return 0 <= x < w and 0 <= y < h and bool(self.mascara_da_area.get_at((x, y)))

    def quadro(self, segundos):
        return self.animacao.quadro_em(segundos + self.fase)

    def quadro_vermelho(self, segundos):
        quadro = self.quadro(segundos)
        if id(quadro) not in self._vermelhos:
            vermelho = quadro.copy()
            vermelho.fill((255, 90, 80, 255), special_flags=pygame.BLEND_RGBA_MULT)
            self._vermelhos[id(quadro)] = vermelho
        return self._vermelhos[id(quadro)]


class SobAsFolhas(BasePuzzle):
    name = "Sob as Folhas"
    # texto da tela de preparo (os segundos antes de jogar)
    instrucao = (
        "Limpe o chão! Clique nas folhas o mais rápido que puder, de cima pra baixo. "
        "Embaixo delas se escondem 6 bichos (borboleta, 2 joaninhas, vespa, pernilongo e "
        "minhoca): não clique neles! Até as folhas debaixo dos bichos precisam sair: "
        "clique nelas, só que fora do bicho."
    )

    def __init__(self, rect, difficulty=1, relacao=100):
        self.rect = rect
        self.difficulty = difficulty
        self.relacao = relacao
        self.done = False
        self.result = None
        self.tempo = 0.0
        self.efeitos = []

        self._preparar_desenhos()
        self.bichos = self._posicionar_bichos()
        self.folhas = self._montar_folhas()
        self.leaves_left = len(self.folhas)
        self.insects_hit = 0
        self.time_left = difficulty_scale(difficulty, relacao, *TEMPO_EM_SEGUNDOS)
        self.total_time = self.time_left

        self._chao = self._pintar_o_chao()
        self._fonte = pygame.font.SysFont("verdana", 13)

    # ------------------------------------------------------------ preparo
    def _preparar_desenhos(self):
        """As 8 viradas de folha (espelhada ou não, girada de 90 em 90), em cada camada."""
        nome_da_folha = os.path.splitext(ARQUIVO_DA_FOLHA)[0]
        folha = _ampliar_para(_desenho(nome_da_folha).recortada(), TAMANHO_DA_FOLHA)
        base = folha.quadros[0]
        if _mascara(base, 128).count() < 20:
            # um desenho vazio (ex.: a camada ficou escondida no Aseprite) deixaria as folhas
            # impossíveis de clicar: nesse caso, usa o provisório
            if ARQUIVO_DA_FOLHA not in _AVISADOS:
                _AVISADOS.add(ARQUIVO_DA_FOLHA)
                print(f"AVISO: Sob as Folhas: {ARQUIVO_DA_FOLHA} parece vazio (tudo transparente); "
                      f"usando um desenho provisório de folha.")
            folha = _ampliar_para(_provisorio(nome_da_folha).recortada(), TAMANHO_DA_FOLHA)
            base = folha.quadros[0]
        viradas = []
        for espelhar in (False, True):
            for graus in (0, 90, 180, 270):
                v = pygame.transform.flip(base, True, False) if espelhar else base
                viradas.append(pygame.transform.rotate(v, graus) if graus else v)
        self.tamanho_da_folha = max(base.get_size())
        n = CAMADAS_DE_CIMA
        self._viradas = []
        for camada in range(n + 1):                      # 0 = a de baixo, n = a de cima
            fator = 1.0 - ESCURECER_CAMADAS_DE_BAIXO * (1 - camada / n) if n else 1.0
            lista = []
            for v in viradas:
                imagem = _escurecida(v, fator) if fator < 0.999 else v
                mascara = _mascara(v, 128)
                lista.append((imagem, _sombra(mascara, SOMBRA_DAS_FOLHAS), mascara))
            self._viradas.append(lista)

    def _posicionar_bichos(self):
        bichos = []
        centros = []
        for nome, quantidade in BICHOS:
            for _ in range(quantidade):
                animacao = _ampliar_para(_desenho(nome).recortada(), TAMANHO_DOS_BICHOS.get(nome, TAMANHO_PADRAO_DE_BICHO))
                if GIRAR_BICHOS:
                    giro = random.choice((0, 90, 180, 270))
                    animacao = aseprite.Animacao([pygame.transform.rotate(q, giro) for q in animacao.quadros],
                                                 list(animacao.duracoes), animacao.tamanho)
                if random.random() < 0.5:                # virado pro outro lado
                    animacao = aseprite.Animacao([pygame.transform.flip(q, True, False) for q in animacao.quadros],
                                                 list(animacao.duracoes), animacao.tamanho)
                w, h = animacao.quadros[0].get_size()
                raio = max(w, h) / 2
                margem = 8
                centro = None
                for _ in range(400):
                    c = (random.uniform(self.rect.left + w / 2 + margem, self.rect.right - w / 2 - margem),
                         random.uniform(self.rect.top + h / 2 + margem, self.rect.bottom - h / 2 - margem))
                    if all(math.hypot(c[0] - o[0], c[1] - o[1]) >= (raio + o[2]) * 0.9 + 16 for o in centros):
                        centro = c
                        break
                if centro is None:                       # sem lugar sobrando: espalha em fileira
                    i = len(centros)
                    centro = (self.rect.left + (i + 0.5) * self.rect.width / TOTAL_INSECTS, self.rect.centery)
                centros.append((centro[0], centro[1], raio))
                bichos.append(_Bicho(nome, animacao, centro, random.uniform(0, 3)))
        return bichos

    def _montar_folhas(self):
        S = self.tamanho_da_folha
        n_cima = CAMADAS_DE_CIMA
        por_camada = int(round(difficulty_scale(self.difficulty, self.relacao, *FOLHAS_POR_CAMADA)))
        pontos = {camada: self._grade(por_camada, camada) for camada in range(n_cima + 1)}
        # folhas embaixo de cada bicho (camada 0)
        for bicho in self.bichos:
            for _ in range(FOLHAS_EMBAIXO_DE_CADA_BICHO):
                cx, cy = bicho.rect.center
                pontos[0].append((cx + random.uniform(-0.28, 0.28) * S, cy + random.uniform(-0.28, 0.28) * S))

        folhas = []
        for camada in range(n_cima + 1):
            for p in pontos[camada]:
                folhas.append(_Folha(camada, random.choice(self._viradas[camada]), p))

        # folhas por cima dos bichos, até escondê-los quase por completo
        if n_cima:
            for bicho in self.bichos:
                for _ in range(6):
                    if self._cobertura(bicho, folhas) >= COBERTURA_MINIMA:
                        break
                    camada = random.randint(1, n_cima)
                    cx, cy = bicho.rect.center
                    p = (cx + random.uniform(-0.22, 0.22) * S, cy + random.uniform(-0.22, 0.22) * S)
                    folhas.append(_Folha(camada, random.choice(self._viradas[camada]), p))

        self._garantir_que_da_pra_limpar(folhas)
        # a ordem de desenho: camada de baixo primeiro; dentro da camada, a ordem sorteada
        random.shuffle(folhas)
        folhas.sort(key=lambda f: f.camada)
        return folhas

    def _grade(self, quantidade, camada):
        """`quantidade` pontos bem espalhados pela área (grade com sorteio)."""
        rect = self.rect
        colunas = max(3, round(math.sqrt(quantidade * rect.width / rect.height)))
        linhas = max(2, math.ceil(quantidade / colunas))
        dx, dy = rect.width / colunas, rect.height / linhas
        deslocamento = 0.5 * (camada % 2)
        pontos = []
        for l in range(linhas):
            for c in range(colunas):
                x = rect.left + ((c + 0.5 + deslocamento) % colunas) * dx + random.uniform(-0.38, 0.38) * dx
                y = rect.top + (l + 0.5) * dy + random.uniform(-0.38, 0.38) * dy
                pontos.append((x, y))
        random.shuffle(pontos)
        return pontos[:quantidade]

    def _cobertura(self, bicho, folhas):
        """De 0 a 1: quanto do desenho do bicho está coberto pelas folhas de cima."""
        total = bicho.mascara_visivel.count()
        if not total:
            return 1.0
        coberto = pygame.mask.Mask(bicho.rect.size)
        for f in folhas:
            if f.camada >= 1 and f.rect.colliderect(bicho.rect):
                coberto.draw(f.mascara, (f.rect.x - bicho.rect.x, f.rect.y - bicho.rect.y))
        return coberto.overlap_area(bicho.mascara_visivel, (0, 0)) / total

    def _garantir_que_da_pra_limpar(self, folhas):
        """Toda folha precisa ter um pedacinho que dê pra clicar sem tocar em bicho. As
        de baixo, que estão sob um bicho, são as que podem falhar: se uma não tiver,
        ela é afastada do bicho; se mesmo assim não der, é tirada."""
        for folha in list(folhas):
            if folha.camada != 0:
                continue
            minimo = max(150, SOBRA_MINIMA_DA_FOLHA * folha.mascara.count())
            for _ in range(10):
                if self._area_livre(folha) >= minimo:
                    break
                perto = min((b for b in self.bichos if b.rect.colliderect(folha.rect)),
                            key=lambda b: math.hypot(b.rect.centerx - folha.rect.centerx,
                                                     b.rect.centery - folha.rect.centery),
                            default=None)
                if perto is None:
                    break
                vx, vy = folha.rect.centerx - perto.rect.centerx, folha.rect.centery - perto.rect.centery
                norma = math.hypot(vx, vy) or 1.0
                folha.rect.centerx += int(round(vx / norma * 0.12 * self.tamanho_da_folha)) or 1
                folha.rect.centery += int(round(vy / norma * 0.12 * self.tamanho_da_folha))
            if self._area_livre(folha) < minimo:
                folhas.remove(folha)

    def _area_livre(self, folha):
        """Quantos pixels da folha dá pra clicar sem acertar a área de nenhum bicho."""
        livre = folha.mascara.copy()
        for bicho in self.bichos:
            if bicho.rect.inflate(2 * FOLGA_DO_BICHO + 2, 2 * FOLGA_DO_BICHO + 2).colliderect(folha.rect):
                livre.erase(bicho.mascara_da_area, (bicho.canto_da_area[0] - folha.rect.x,
                                                    bicho.canto_da_area[1] - folha.rect.y))
        return livre.count()

    def _pintar_o_chao(self):
        """A terra que aparece quando as folhas saem: cor de fundo + pontinhos e pedrinhas."""
        w, h = self.rect.size
        chao = pygame.Surface((w, h), pygame.SRCALPHA)
        chao.fill(COR_DO_CHAO)
        bloco = 4
        for y in range(0, h, bloco):
            for x in range(0, w, bloco):
                if random.random() < 0.22:
                    variacao = random.choice((-14, -8, 8, 12))
                    cor = tuple(max(0, min(255, c + variacao)) for c in COR_DO_CHAO)
                    pygame.draw.rect(chao, cor, (x, y, bloco, bloco))
        for _ in range(w * h // 2600):
            x, y = random.randrange(w - 6), random.randrange(h - 5)
            pygame.draw.rect(chao, (120, 98, 76), (x, y, 5, 3))
            pygame.draw.rect(chao, (150, 126, 100), (x, y, 3, 1))
        # cantos arredondados
        mascara = pygame.Surface((w, h), pygame.SRCALPHA)
        pygame.draw.rect(mascara, (255, 255, 255, 255), mascara.get_rect(), border_radius=8)
        chao.blit(mascara, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
        return chao

    # ------------------------------------------------------------ jogo
    def update(self, dt):
        self.tempo += dt
        for efeito in self.efeitos:
            efeito["t"] += dt
        self.efeitos = [e for e in self.efeitos if e["t"] < e["dur"]]
        for bicho in self.bichos:
            if bicho.tremor > 0:
                bicho.tremor = max(0.0, bicho.tremor - dt)
        if self.done:
            return
        self.time_left -= dt
        if self.time_left <= 0:
            self._finish()

    def handle_key(self, key):
        pass

    def _o_que_esta_em_cima(self, pos):
        """O que está por cima no ponto: ("folha", f), ("bicho", b) ou None.
        Da frente pra trás: as folhas das camadas de cima, os bichos, as folhas de baixo."""
        for f in reversed(self.folhas):
            if f.camada >= 1 and f.cobre(pos):
                return "folha", f
        for b in self.bichos:
            if b.na_area(pos):
                return "bicho", b
        for f in reversed(self.folhas):
            if f.camada == 0 and f.cobre(pos):
                return "folha", f
        return None

    def handle_click(self, pos):
        if self.done:
            return
        alvo = self._o_que_esta_em_cima(pos)
        self.efeitos.append({"tipo": "toque", "pos": pos, "t": 0.0, "dur": 0.16})
        if alvo is None:
            return
        tipo, coisa = alvo
        if tipo == "folha":
            self.folhas.remove(coisa)
            self.leaves_left -= 1
            vx = coisa.rect.centerx - pos[0]
            vy = coisa.rect.centery - pos[1]
            norma = math.hypot(vx, vy) or 1.0
            self.efeitos.append({"tipo": "folha", "folha": coisa, "t": 0.0, "dur": 0.3,
                                 "vel": (vx / norma * 150 + random.uniform(-40, 40), vy / norma * 150 - 90)})
            if self.leaves_left <= 0:
                self._finish()
        elif not coisa.atingido:
            coisa.atingido = True
            coisa.tremor = 0.5
            self.insects_hit += 1
            self.efeitos.append({"tipo": "pancada", "pos": coisa.rect.center, "t": 0.0, "dur": 0.45})

    def _finish(self):
        self.done = True
        if self.leaves_left > 0:
            self.result = "falha"                 # o tempo acabou com folhas sobrando
        elif self.insects_hit == 0:
            self.result = "sucesso"
        elif self.insects_hit <= 3:
            self.result = "parcial"
        else:
            self.result = "falha"

    # ------------------------------------------------------------ desenho
    def draw(self, surface):
        clip_anterior = surface.get_clip()
        surface.blit(self._chao, self.rect.topleft)
        surface.set_clip(self.rect)

        for f in self.folhas:
            if f.camada == 0:
                self._desenhar_folha(surface, f)
        for b in self.bichos:
            self._desenhar_bicho(surface, b)
        for f in self.folhas:
            if f.camada >= 1:
                self._desenhar_folha(surface, f)
        self._desenhar_efeitos(surface)
        surface.set_clip(clip_anterior)

        pygame.draw.rect(surface, COR_DA_BORDA, self.rect, 3, border_radius=8)
        self._desenhar_painel(surface)

    @staticmethod
    def _desenhar_folha(surface, f):
        if f.sombra is not None:
            surface.blit(f.sombra, (f.rect.x + 3, f.rect.y + 4))
        surface.blit(f.imagem, f.rect)

    def _desenhar_bicho(self, surface, b):
        x, y = b.rect.topleft
        if b.tremor > 0:
            x += round(math.sin(self.tempo * 70) * 3 * (b.tremor / 0.5))
        imagem = b.quadro_vermelho(self.tempo) if b.atingido else b.quadro(self.tempo)
        surface.blit(imagem, (x, y))

    def _desenhar_efeitos(self, surface):
        for e in self.efeitos:
            progresso = e["t"] / e["dur"]
            if e["tipo"] == "folha":                  # a folha voa e some
                f = e["folha"]
                vx, vy = e["vel"]
                imagem = f.imagem.copy()
                imagem.set_alpha(int(255 * (1 - progresso)))
                surface.blit(imagem, (f.rect.x + vx * e["t"], f.rect.y + vy * e["t"] + 260 * e["t"] * e["t"]))
            elif e["tipo"] == "toque":                # um anelzinho onde clicou
                raio = 6 + int(14 * progresso)
                anel = pygame.Surface((raio * 2 + 4, raio * 2 + 4), pygame.SRCALPHA)
                pygame.draw.circle(anel, (255, 255, 255, int(150 * (1 - progresso))), (raio + 2, raio + 2), raio, 2)
                surface.blit(anel, (e["pos"][0] - raio - 2, e["pos"][1] - raio - 2))
            elif e["tipo"] == "pancada":              # clicou num bicho: anel vermelho
                raio = 14 + int(30 * progresso)
                anel = pygame.Surface((raio * 2 + 6, raio * 2 + 6), pygame.SRCALPHA)
                pygame.draw.circle(anel, (230, 60, 50, int(220 * (1 - progresso))), (raio + 3, raio + 3), raio, 4)
                surface.blit(anel, (e["pos"][0] - raio - 3, e["pos"][1] - raio - 3))

    def _desenhar_painel(self, surface):
        """Folhas que faltam, a barra do tempo e os bichos atingidos."""
        y = self.rect.bottom + 12
        esquerda = self._fonte.render(f"Folhas: {self.leaves_left}", True, TEXT_DARK)
        surface.blit(esquerda, (self.rect.left, y))

        largura = int(self.rect.width * 0.42)
        barra = pygame.Rect(0, y + 2, largura, 12)
        barra.centerx = self.rect.centerx
        fracao = max(0.0, min(1.0, self.time_left / self.total_time))
        cor = (110, 180, 90) if fracao > 0.5 else ((226, 170, 60) if fracao > 0.25 else (210, 80, 70))
        pygame.draw.rect(surface, (225, 220, 205), barra, border_radius=6)
        if fracao > 0:
            pygame.draw.rect(surface, cor, (barra.x, barra.y, int(barra.width * fracao), barra.height), border_radius=6)
        pygame.draw.rect(surface, (140, 130, 115), barra, 1, border_radius=6)
        tempo = self._fonte.render(f"{max(0, self.time_left):.1f}s", True, TEXT_DARK)
        surface.blit(tempo, (barra.right + 8, y))

        cor_do_texto = (190, 60, 50) if self.insects_hit else TEXT_DARK
        direita = self._fonte.render(f"Bichos atingidos: {self.insects_hit}/{len(self.bichos)}", True, cor_do_texto)
        surface.blit(direita, (self.rect.right - direita.get_width(), y))

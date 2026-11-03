# -*- coding: utf-8 -*-
"""
LEITOR DE ARQUIVOS DO ASEPRITE (.ase / .aseprite).

O pygame não lê .ase direto. Este arquivo lê o desenho do jeito que ele sai do
Aseprite, então você pode editar o desenho lá, salvar, e o jogo usa a versão
nova na próxima vez que abrir (sem exportar PNG).

    from minigames.jogos import aseprite
    animacao = aseprite.carregar("assets/Folha.ase")
    animacao.quadros      # lista de imagens do pygame (uma por quadro)
    animacao.duracoes     # quanto cada quadro dura, em milissegundos
    animacao.tamanho      # (largura, altura)

O que ele entende: cores RGBA, tons de cinza e paleta (indexado); várias camadas
(as camadas escondidas não aparecem); opacidade da camada e do "cel"; cels
ligados entre quadros; a duração de cada quadro.
O que ele ignora: modos de mesclagem (tudo é tratado como "normal") e camadas
de tilemap.

Se o arquivo não existir ou estiver estragado, levanta ValueError com uma
mensagem dizendo o que houve.
"""
import os
import struct
import zlib

import pygame

_CACHE = {}

_FLAG_CAMADA_VISIVEL = 1
_FLAG_CAMADA_FUNDO = 8
_FLAG_OPACIDADE_VALIDA = 2


class Animacao:
    """Os quadros de um desenho do Aseprite (um só, ou uma animação)."""

    def __init__(self, quadros, duracoes, tamanho):
        self.quadros = quadros
        self.duracoes = duracoes
        self.tamanho = tamanho

    @property
    def duracao_total(self):
        return sum(self.duracoes) or 1

    def quadro_em(self, segundos):
        """O quadro que aparece no instante `segundos` (a animação repete sozinha)."""
        if len(self.quadros) == 1:
            return self.quadros[0]
        t = int(segundos * 1000) % self.duracao_total
        for quadro, duracao in zip(self.quadros, self.duracoes):
            if t < duracao:
                return quadro
            t -= duracao
        return self.quadros[-1]

    def recortada(self):
        """Uma cópia sem as bordas transparentes (o recorte é o mesmo em todos os
        quadros, pra a animação não pular)."""
        caixa = None
        for quadro in self.quadros:
            r = quadro.get_bounding_rect()
            if r.width and r.height:
                caixa = r if caixa is None else caixa.union(r)
        if caixa is None:
            return self
        novos = [q.subsurface(caixa).copy() for q in self.quadros]
        return Animacao(novos, list(self.duracoes), caixa.size)

    def ampliada(self, fator):
        """Uma cópia ampliada por um número inteiro, sem borrar (pixel art)."""
        fator = max(1, int(fator))
        if fator == 1:
            return self
        novos = [pygame.transform.scale(q, (q.get_width() * fator, q.get_height() * fator)) for q in self.quadros]
        return Animacao(novos, list(self.duracoes), (self.tamanho[0] * fator, self.tamanho[1] * fator))


def carregar(caminho):
    """Lê um .ase e devolve uma Animacao. (Guarda o resultado: ler de novo o
    mesmo arquivo não custa nada, a menos que ele tenha mudado.)"""
    if not os.path.isfile(caminho):
        raise ValueError(f"não achei o arquivo {caminho}")
    chave = (os.path.abspath(caminho), os.path.getmtime(caminho))
    if chave not in _CACHE:
        with open(caminho, "rb") as f:
            dados = f.read()
        try:
            _CACHE[chave] = _ler(dados)
        except (struct.error, zlib.error, IndexError) as erro:
            raise ValueError(f"o arquivo {caminho} não parece um .ase válido ({erro})") from None
    return _CACHE[chave]


# ============================================================ por dentro
def _texto(dados, pos):
    n = struct.unpack_from("<H", dados, pos)[0]
    return dados[pos + 2:pos + 2 + n].decode("utf-8", "replace"), pos + 2 + n


def _ler(b):
    if len(b) < 128:
        raise ValueError("arquivo pequeno demais para ser um .ase")
    _, magico, n_quadros, largura, altura, profundidade, flags = struct.unpack_from("<IHHHHHI", b, 0)
    if magico != 0xA5E0:
        raise ValueError("não começa como um .ase (cabeçalho inesperado)")
    if profundidade not in (8, 16, 32):
        raise ValueError(f"profundidade de cor {profundidade} não suportada")
    indice_transparente = b[28]
    opacidade_da_camada_vale = bool(flags & _FLAG_OPACIDADE_VALIDA)

    paleta = [(0, 0, 0, 255)] * 256
    camadas = []                      # cada uma: dict(flags, tipo, nivel, opacidade, visivel)
    quadros_de_cels = []              # por quadro: {indice_da_camada: dict(x, y, opacidade, z, tipo, ...)}
    duracoes = []

    pos = 128
    for _ in range(n_quadros):
        tam, _, n_antigo, duracao = struct.unpack_from("<IHHH", b, pos)
        n_novo = struct.unpack_from("<I", b, pos + 12)[0]
        n_chunks = n_novo or n_antigo
        cels = {}
        off = pos + 16
        for _ in range(n_chunks):
            tc, tipo = struct.unpack_from("<IH", b, off)
            corpo = b[off + 6:off + tc]

            if tipo == 0x2004:                                   # camada
                cflags, ctipo, nivel, _, _, _, opacidade = struct.unpack_from("<HHHHHHB", corpo, 0)
                camadas.append({"flags": cflags, "tipo": ctipo, "nivel": nivel,
                                "opacidade": opacidade if opacidade_da_camada_vale else 255})
            elif tipo == 0x2005:                                 # cel
                indice, x, y, opacidade, ctipo, z = struct.unpack_from("<HhhBHh", corpo, 0)
                cel = {"x": x, "y": y, "opacidade": opacidade, "z": z, "tipo": ctipo}
                if ctipo in (0, 2):
                    w, h = struct.unpack_from("<HH", corpo, 16)
                    bruto = corpo[20:]
                    cel["w"], cel["h"] = w, h
                    cel["bytes"] = zlib.decompress(bruto) if ctipo == 2 else bruto
                    cels[indice] = cel
                elif ctipo == 1:                                 # ligado a outro quadro: usa o mesmo desenho
                    outro = struct.unpack_from("<H", corpo, 16)[0]
                    original = quadros_de_cels[outro].get(indice)
                    if original is not None:
                        cels[indice] = original
                # (ctipo 3 = tilemap: ignorado)
            elif tipo == 0x2019:                                 # paleta
                tamanho_novo, primeiro, ultimo = struct.unpack_from("<III", corpo, 0)
                p = 20
                for i in range(primeiro, ultimo + 1):
                    eflags, r, g, bl, a = struct.unpack_from("<HBBBB", corpo, p)
                    p += 6
                    if eflags & 1:
                        _, p = _texto(corpo, p)
                    if i < 256:
                        paleta[i] = (r, g, bl, a)
            elif tipo in (0x0004, 0x0011):                       # paletas antigas
                n_pacotes = struct.unpack_from("<H", corpo, 0)[0]
                p, i = 2, 0
                for _ in range(n_pacotes):
                    pular, quantas = corpo[p], corpo[p + 1] or 256
                    p += 2
                    i += pular
                    for _ in range(quantas):
                        r, g, bl = corpo[p], corpo[p + 1], corpo[p + 2]
                        p += 3
                        if tipo == 0x0011:                       # valores de 0 a 63
                            r, g, bl = r * 255 // 63, g * 255 // 63, bl * 255 // 63
                        if i < 256:
                            paleta[i] = (r, g, bl, 255)
                        i += 1
            off += tc
        quadros_de_cels.append(cels)
        duracoes.append(duracao or 100)
        pos += tam

    visiveis = _camadas_visiveis(camadas)
    quadros = []
    for cels in quadros_de_cels:
        quadro = pygame.Surface((largura, altura), pygame.SRCALPHA)
        quadro.fill((0, 0, 0, 0))
        ordem = sorted(cels.items(), key=lambda item: (item[0] + item[1]["z"], item[1]["z"]))
        for indice, cel in ordem:
            if indice >= len(camadas) or not visiveis[indice] or camadas[indice]["tipo"] != 0:
                continue
            imagem = _imagem_do_cel(cel, profundidade, paleta, indice_transparente,
                                    camadas[indice]["flags"] & _FLAG_CAMADA_FUNDO)
            opacidade = camadas[indice]["opacidade"] * cel["opacidade"] // 255
            if opacidade < 255:
                imagem = imagem.copy()
                imagem.fill((255, 255, 255, opacidade), special_flags=pygame.BLEND_RGBA_MULT)
            quadro.blit(imagem, (cel["x"], cel["y"]))
        if pygame.display.get_surface() is not None:
            quadro = quadro.convert_alpha()
        quadros.append(quadro)
    return Animacao(quadros, duracoes, (largura, altura))


def _camadas_visiveis(camadas):
    """Uma camada só aparece se ela E todos os grupos em que ela está estiverem visíveis."""
    visiveis = []
    pilha = []                         # (nivel, visivel) dos grupos abertos
    for camada in camadas:
        while pilha and pilha[-1][0] >= camada["nivel"]:
            pilha.pop()
        proprio = bool(camada["flags"] & _FLAG_CAMADA_VISIVEL)
        todos = proprio and all(v for _, v in pilha)
        visiveis.append(todos)
        if camada["tipo"] == 1:        # grupo
            pilha.append((camada["nivel"], proprio and all(v for _, v in pilha)))
    return visiveis


def _imagem_do_cel(cel, profundidade, paleta, indice_transparente, e_fundo):
    w, h, dados = cel["w"], cel["h"], cel["bytes"]
    if profundidade == 32:
        rgba = dados[:w * h * 4]
    elif profundidade == 16:                                     # cinza + transparência
        rgba = b"".join(bytes((dados[i], dados[i], dados[i], dados[i + 1])) for i in range(0, w * h * 2, 2))
    else:                                                        # indexado
        tabela = []
        for i, (r, g, bl, a) in enumerate(paleta):
            if i == indice_transparente and not e_fundo:
                a = 0
            tabela.append(bytes((r, g, bl, a)))
        rgba = b"".join(tabela[i] for i in dados[:w * h])
    return pygame.image.frombuffer(rgba, (w, h), "RGBA").copy()

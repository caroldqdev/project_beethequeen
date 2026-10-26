# -*- coding: utf-8 -*-
"""
OS COMPONENTES: as peças que as telas reutilizam -- painel, texto, barra,
radar e o HUD (os painéis de moedas e afinidade, no alto).

Cada tela monta o que precisa com estas peças; mudou o jeito de uma peça
aqui, muda em todas as telas.
"""
import math
import pygame

import config
import regras
from dados.conselheiras import CONSELHEIRAS
from dados.eixos import EIXOS, ROTULOS
from telas import estilos, layout, textos


# ------------------------------------------------------------ colar na tela
_TINTA = {}      # (texto, fonte, cor) -> onde fica a "tinta" de cada linha (não muda; guardado)


def colar(v, superficie, retangulo, chave=None):
    """Cola um texto (ou imagem) na tela, em `retangulo`. Dentro de um card de
    escrita, primeiro só MEDE (onde cai a tinta) e depois cola já deslocado."""
    if v.medindo:
        tinta = _TINTA.get(chave) if chave is not None else None
        if tinta is None:
            tinta = superficie.get_bounding_rect()
            if chave is not None:
                _TINTA[chave] = tinta
        if tinta.width and tinta.height:
            caixa = tinta.move(retangulo.x, retangulo.y)
            v.tinta = caixa if v.tinta is None else v.tinta.union(caixa)
        return
    v.tela.blit(superficie, (retangulo.x, retangulo.y + v.deslocamento_y))


# ------------------------------------------------------------------ painel
def painel(tela, retangulo, raio=16, alfa=235):
    """O card branco translúcido de quase toda tela."""
    superficie = pygame.Surface((retangulo.width, retangulo.height), pygame.SRCALPHA)
    pygame.draw.rect(superficie, (255, 255, 255, alfa), superficie.get_rect(), border_radius=raio)
    pygame.draw.rect(superficie, (120, 120, 120, 255), superficie.get_rect(), 2, border_radius=raio)
    tela.blit(superficie, retangulo.topleft)


# ------------------------------------------------------------------- texto
def quebrar_texto(conteudo, fonte, largura):
    """Quebra um texto em linhas que cabem na largura."""
    palavras = conteudo.split(" ")
    linhas, atual = [], ""
    for palavra in palavras:
        tentativa = (atual + " " + palavra).strip()
        if fonte.size(tentativa)[0] <= largura:
            atual = tentativa
        else:
            if atual:
                linhas.append(atual)
            atual = palavra
    if atual:
        linhas.append(atual)
    return linhas


def _linhas(conteudo, fonte, largura):
    linhas = []
    for paragrafo in conteudo.split("\n"):
        quebradas = quebrar_texto(paragrafo, fonte, largura)
        if quebradas:
            linhas.extend(quebradas)
        else:
            linhas.append("")      # parágrafo vazio vira uma linha em branco de verdade
    return linhas


def texto(v, conteudo, retangulo, fonte="corpo", cor=layout.ESCURO, espaco=6, alinhamento="esquerda"):
    """Escreve um texto quebrado em linhas a partir do topo do retângulo, alinhado
    à "esquerda" ou ao "centro" (cada linha centralizada no retângulo).
    Devolve o y logo abaixo da última linha."""
    f = v.fontes[fonte]
    y = retangulo.top
    for linha in _linhas(conteudo, f, retangulo.width):
        superficie = f.render(linha, True, cor)
        if alinhamento == "centro":
            destino = superficie.get_rect(midtop=(retangulo.centerx, y))
        else:
            destino = superficie.get_rect(topleft=(retangulo.left, y))
        colar(v, superficie, destino, (linha, fonte, cor))
        y += f.get_height() + espaco
    return y


def escrever(v, conteudo, fonte, cor, centro=None, canto=None, topo_centro=None):
    """Escreve uma linha de texto: centralizada em `centro`, com o canto de cima
    à esquerda em `canto`, ou com o meio do TOPO em `topo_centro`. Devolve o
    retângulo que ela ocupou."""
    superficie = v.fontes[fonte].render(conteudo, True, cor)
    if centro is not None:
        retangulo = superficie.get_rect(center=centro)
    elif topo_centro is not None:
        retangulo = superficie.get_rect(midtop=topo_centro)
    else:
        retangulo = superficie.get_rect(topleft=canto)
    colar(v, superficie, retangulo, (conteudo, fonte, cor))
    return retangulo


# ------------------------------------------------------- os cards de escrita
# Estas peças leem o "CSS" (telas/estilos.py): cada texto tem um card e um nome.
def _estilo(card, elemento):
    return estilos.ESTILOS[card][elemento]


def _deslocamento(v, estilo):
    """O deslocamento do texto (na hora de medir o bloco ele não conta)."""
    return (0, 0) if v.medindo else (estilo["deslocamento_x"], estilo["deslocamento_y"])


def _cor(estilo, automatica):
    """A cor do estilo; "conselheira" e "resultado" usam a cor que a tela passou."""
    return automatica if estilo["cor"] in ("conselheira", "resultado") else estilo["cor"]


def linha(v, conteudo, card, elemento, caixa, y, ancora_y="centro", cor_automatica=None):
    """Uma linha de texto, no estilo de ESTILOS[card][elemento].

    `caixa` é o retângulo onde ela se alinha (o card); `y` é a posição na vertical:
    o MEIO da linha (ancora_y="centro") ou o TOPO dela (ancora_y="topo")."""
    est = _estilo(card, elemento)
    margem = estilos.ESTILOS[card]["_card"]["margem_lateral"]
    cor = _cor(est, cor_automatica)
    superficie = v.fontes[est["fonte"]].render(conteudo, True, cor)
    r = superficie.get_rect()
    if est["alinhamento"] == "esquerda":
        r.left = caixa.left + margem
    elif est["alinhamento"] == "direita":
        r.right = caixa.right - margem
    else:
        r.centerx = caixa.centerx
    if ancora_y == "topo":
        r.top = y
    else:
        r.centery = y
    dx, dy = _deslocamento(v, est)
    r.x += dx
    r.y += dy
    colar(v, superficie, r, (conteudo, est["fonte"], cor))
    return r


def linha_com_emoji(v, nome, dados, emoji, card, elemento, caixa, y):
    """O nome da conselheira com o emoji dela ao lado (o par se alinha junto)."""
    est = _estilo(card, elemento)
    margem = estilos.ESTILOS[card]["_card"]["margem_lateral"]
    cor = _cor(est, dados["cor"])
    cabecalho = v.fontes[est["fonte"]].render(nome, True, cor)
    retangulo = cabecalho.get_rect()
    retangulo.centery = y
    espaco = layout.CONSELHEIRA_EMOJI_ESPACO
    largura_total = retangulo.width + (emoji.get_width() + espaco if emoji is not None else 0)
    if est["alinhamento"] == "esquerda":
        inicio_x = caixa.left + margem
    elif est["alinhamento"] == "direita":
        inicio_x = caixa.right - margem - largura_total
    else:
        inicio_x = caixa.centerx - largura_total // 2
    dx, dy = _deslocamento(v, est)
    if emoji is not None:
        retangulo_do_emoji = emoji.get_rect(midleft=(inicio_x + dx, retangulo.centery + dy))
        colar(v, emoji, retangulo_do_emoji, ("emoji", nome))
        retangulo.left = retangulo_do_emoji.right + espaco
    else:
        retangulo.left = inicio_x + dx
    retangulo.y += dy
    colar(v, cabecalho, retangulo, (nome, est["fonte"], cor))
    return retangulo


def paragrafo(v, conteudo, card, elemento, caixa):
    """Um texto que quebra em várias linhas, no estilo de ESTILOS[card][elemento].

    `caixa` é onde ele cabe (a posição e o tamanho estão em telas/layout.py).
    Devolve o y logo abaixo da última linha (sem contar o deslocamento, que só
    move esse texto e não empurra os outros)."""
    est = _estilo(card, elemento)
    esquerda, direita = est["margem_esquerda"], est["margem_direita"]
    area = pygame.Rect(caixa.left + esquerda, caixa.top, caixa.width - esquerda - direita, caixa.height)
    fonte = v.fontes[est["fonte"]]
    cor = est["cor"]
    linhas = _linhas(conteudo, fonte, area.width)
    passo = fonte.get_height() + est["espaco_entre_linhas"]
    y = area.top
    if est["alinhamento_vertical"] == "centro":
        y += (area.height - (len(linhas) * passo - est["espaco_entre_linhas"])) // 2
    dx, dy = _deslocamento(v, est)
    for texto_da_linha in linhas:
        superficie = fonte.render(texto_da_linha, True, cor)
        if est["alinhamento"] == "centro":
            r = superficie.get_rect(midtop=(area.centerx, y))
        elif est["alinhamento"] == "direita":
            r = superficie.get_rect(topright=(area.right, y))
        else:
            r = superficie.get_rect(topleft=(area.left, y))
        r.x += dx
        r.y += dy
        colar(v, superficie, r, (texto_da_linha, est["fonte"], cor))
        y += passo
    return y


def dica_aparece(v, j):
    """A dica "Pressione ENTER..." já pode aparecer? (Na hora de medir o bloco
    ela conta como visível, pra o texto não pular quando ela aparecer.)"""
    return v.medindo or j.dica_visivel


def card_de_texto(v, card, caixa, desenhar):
    """Desenha os textos de um card, na parte "_card" do CSS (telas/estilos.py):

    centralizar_bloco   o bloco todo fica no meio do card na vertical (os textos
                        se movem juntos, a distância entre eles não muda)
    padding_topo        depois disso, anda todos os textos pra baixo (+) ou pra cima (-)

    `desenhar()` desenha os textos com linha()/paragrafo(). A abelhinha e o
    painel ficam de fora: desenhe-os fora daqui."""
    est = estilos.ESTILOS[card]["_card"]
    automatico = 0
    try:
        if est["centralizar_bloco"]:
            # 1) mede: "desenha" sem colar nada e vê onde a tinta cairia
            v.medindo, v.tinta, v.deslocamento_y = True, None, 0
            desenhar()
            if v.tinta is not None:
                automatico = caixa.centery - v.tinta.centery
        # 2) desenha de verdade, já deslocado
        v.medindo = False
        v.deslocamento_y = automatico + est["padding_topo"]
        desenhar()
    finally:
        v.medindo, v.tinta, v.deslocamento_y = False, None, 0


# ------------------------------------------------------------ barra e radar
def barra(tela, posicao, tamanho, valor, maximo, cor, fundo=(230, 230, 230)):
    x, y = posicao
    largura, altura = tamanho
    pygame.draw.rect(tela, fundo, (x, y, largura, altura), border_radius=6)
    proporcao = max(0.0, min(1.0, valor / maximo))
    if proporcao > 0:
        pygame.draw.rect(tela, cor, (x, y, int(largura * proporcao), altura), border_radius=6)
    pygame.draw.rect(tela, (150, 150, 150), (x, y, largura, altura), 1, border_radius=6)


def radar(tela, centro, raio, valores, fonte, maximo=100):
    """O gráfico de teia da Harmonia (5 eixos). `valores` é {eixo: 0..maximo}."""
    cx, cy = centro
    n = len(EIXOS)
    passo = 2 * math.pi / n
    for anel in (0.25, 0.5, 0.75, 1.0):
        pontos = []
        for i in range(n):
            ang = -math.pi / 2 + i * passo
            pontos.append((cx + math.cos(ang) * raio * anel, cy + math.sin(ang) * raio * anel))
        pygame.draw.polygon(tela, (200, 210, 200), pontos, 1)
    for i, eixo in enumerate(EIXOS):
        ang = -math.pi / 2 + i * passo
        pygame.draw.line(tela, (200, 210, 200), (cx, cy),
                         (cx + math.cos(ang) * raio, cy + math.sin(ang) * raio), 1)
        rotulo = fonte.render(ROTULOS[eixo], True, (70, 70, 70))
        tela.blit(rotulo, rotulo.get_rect(center=(cx + math.cos(ang) * (raio + 34),
                                                  cy + math.sin(ang) * (raio + 16))))
    pontos = []
    for i, eixo in enumerate(EIXOS):
        valor = max(0, min(maximo, valores.get(eixo, 0)))
        ang = -math.pi / 2 + i * passo
        r = raio * (valor / maximo)
        pontos.append((cx + math.cos(ang) * r, cy + math.sin(ang) * r))
    forma = pygame.Surface(tela.get_size(), pygame.SRCALPHA)
    pygame.draw.polygon(forma, (255, 209, 102, 120), pontos)
    tela.blit(forma, (0, 0))
    pygame.draw.polygon(tela, layout.DOURADO, pontos, 3)
    for ponto in pontos:
        pygame.draw.circle(tela, layout.DOURADO, (int(ponto[0]), int(ponto[1])), 4)


# --------------------------------------------------------- listas de efeito/custo
def linhas_de_efeitos(resolucao):
    """['Biodiversidade: +8', 'Produção: +3'] -- o que mudou na Harmonia."""
    return [f"{nome}: {'+' if valor >= 0 else ''}{valor}" for nome, valor in resolucao.efeitos]


def linhas_de_custos(resolucao):
    """['Mel: -4', 'Operárias: +25'] -- o que mudou nas moedas."""
    return [f"{textos.NOMES_DAS_MOEDAS[moeda]}: {valor:+d}" for moeda, valor in resolucao.custos.items()]


# --------------------------------------------------------------------- o HUD
def hud(v, estado):
    """Os dois painéis do alto: moedas (esquerda) e afinidade (direita)."""
    # --- moedas ---
    esquerdo = layout.retangulo(layout.HUD_ESQUERDO)
    painel(v.tela, esquerdo)
    x = esquerdo.left + layout.HUD_MARGEM
    largura_da_barra = esquerdo.width - 2 * layout.HUD_MARGEM
    y = esquerdo.top + layout.HUD_TOPO_INTERNO
    barra_altura = layout.HUD_BARRA_ALTURA
    moedas = [
        (textos.HUD_MEL.format(valor=estado.mel), estado.mel, layout.HUD_MEL_MAXIMO, layout.DOURADO),
        (textos.HUD_OPERARIAS.format(valor=estado.operarias), estado.operarias, layout.HUD_MEL_MAXIMO, layout.COR_OPERARIAS),
        (textos.HUD_RELACAO.format(valor=estado.relacao), estado.relacao, layout.HUD_RELACAO_MAXIMO, layout.COR_RELACAO),
    ]
    for legenda, valor, maximo, cor in moedas:
        escrever(v, legenda, "pequena", layout.ESCURO, canto=(x, y))
        barra(v.tela, (x, y + layout.HUD_BARRA_DESLOC), (largura_da_barra, barra_altura), valor, maximo, cor)
        y += layout.HUD_ALTURA_DA_LINHA
    if regras.producao_penalizada(estado):
        escrever(v, textos.HUD_AVISO_DE_PRODUCAO, "pequena", layout.COR_AVISO, canto=(x, y))

    # --- afinidade ---
    direito = layout.retangulo(layout.HUD_DIREITO)
    painel(v.tela, direito)
    x = direito.left + layout.HUD_MARGEM
    escrever(v, textos.HUD_AFINIDADE, "pequena", layout.ESCURO, canto=(x, direito.top + layout.HUD_TOPO_INTERNO))
    y = direito.top + layout.HUD_AFINIDADE_TOPO
    largura_da_barra = direito.width - 2 * layout.HUD_MARGEM - layout.HUD_AFINIDADE_NOME
    for nome, dados in CONSELHEIRAS.items():
        escrever(v, nome, "pequena", layout.ESCURO, canto=(x, y + 2))
        barra(v.tela, (x + layout.HUD_AFINIDADE_NOME, y), (largura_da_barra, layout.HUD_AFINIDADE_BARRA_ALTURA),
              estado.afinidade[nome], 100, dados["cor"])
        y += layout.HUD_AFINIDADE_LINHA


def barra_de_tempo(v, j):
    """A barrinha no pé da tela que mostra quanto falta pra tela passar sozinha
    (só aparece se MOSTRAR_BARRA_DE_TEMPO estiver ligado em config.py)."""
    limite = j.segundos_ate_avancar()
    if not limite:
        return
    restante = max(0.0, 1.0 - j.tempo_da_tela / limite)
    largura, altura = layout.BARRA_DE_TEMPO
    x, y = (config.LARGURA - largura) // 2, config.ALTURA - layout.BARRA_DE_TEMPO_DA_BASE
    pygame.draw.rect(v.tela, (255, 255, 255), (x, y, largura, altura), border_radius=3)
    pygame.draw.rect(v.tela, layout.DOURADO, (x, y, int(largura * restante), altura), border_radius=3)
    pygame.draw.rect(v.tela, (120, 120, 120), (x, y, largura, altura), 1, border_radius=3)

# -*- coding: utf-8 -*-
"""
O LAYOUT: onde cada coisa fica na tela, com um NOME para cada medida.

Para mover ou redimensionar algo, mude o número AQUI -- todas as telas usam
estes nomes (assim nada fica desalinhado porque um número foi trocado só num
lugar). Um retângulo é (x, y, largura, altura), em pixels; (0, 0) é o canto
de cima à esquerda.

  1) CORES
  2) O HUD            os painéis de moedas e afinidade, no alto
  3) APRESENTAÇÃO     abertura, conselheiras, Nova Rainha, estação
  4) EVENTO           o texto do evento e os 4 cards de escolha
  5) MINIGAME         preparo, jogo e resultado
  6) CONSEQUÊNCIA E FINAL
"""
import pygame
from config import LARGURA, ALTURA

# ============================================================
# 1) CORES
# ============================================================
BRANCO = (255, 255, 255)
ESCURO = (40, 40, 40)
DOURADO = (214, 158, 46)
COR_RELACAO = (196, 108, 196)
COR_OPERARIAS = (120, 170, 90)
CINZA = (90, 90, 90)
CINZA_ESCURO = (70, 70, 70)
COR_AVISO = (180, 60, 60)
COR_CUSTO_NO_CARD = (110, 90, 40)
COR_CARD = (255, 250, 235)
COR_CARD_COM_MOUSE = (255, 240, 210)
COR_NOTA_DA_PONTE = (120, 90, 160)
COR_PENALIDADE = (170, 60, 60)
COR_EXTRA = (90, 70, 30)
COR_DESEQUILIBRIO = (180, 90, 40)
COR_CAIXA_ECOLOGIA = (250, 245, 230)
COR_RESULTADO = {"sucesso": (90, 160, 90), "parcial": (200, 150, 60), "falha": (190, 80, 80)}
VEU_BRANCO = (255, 255, 255, 40)
VEU_ESCURO = (20, 20, 30, 140)

# ============================================================
# 2) O HUD (moedas à esquerda, afinidade à direita)
# ============================================================
HUD_ESQUERDO = (16, 16, 310, 168)
HUD_DIREITO = (LARGURA - 326, 16, 310, 168)
HUD_MARGEM = 14
HUD_TOPO_INTERNO = 12
HUD_BARRA_DESLOC = 18
HUD_ALTURA_DA_LINHA = 34
HUD_BARRA_ALTURA = 12
HUD_AFINIDADE_TOPO = 38
HUD_AFINIDADE_LINHA = 30
HUD_AFINIDADE_NOME = 62
HUD_AFINIDADE_BARRA_ALTURA = 14
HUD_MEL_MAXIMO = 150
HUD_RELACAO_MAXIMO = 100

# ============================================================
# 3) APRESENTAÇÃO
# ============================================================
PAINEL_APRESENTACAO = (80, 90, LARGURA - 160, ALTURA - 180)
ABELHA_NA_ABERTURA = (LARGURA // 2 - 48, ALTURA - 150)
ABELHA_NA_CONSELHEIRA = (LARGURA // 2 - 48, ALTURA - 150)

# a abertura (cada bloco de texto é um retângulo; o seguinte começa onde o anterior termina)
ABERTURA_TITULO_Y = 140
ABERTURA_SUBTITULO_Y = 178
ABERTURA_TEXTO_Y = 220
ABERTURA_TEXTO_MARGEM = 120
ABERTURA_TEXTO_1_ALTURA = 60
ABERTURA_CONSELHEIRAS_ALTURA = 30
ABERTURA_ESPACO_ANTES_DO_ULTIMO = 10
ABERTURA_TEXTO_2_ALTURA = 160

# a tela de cada conselheira
CONSELHEIRA_NOME_Y = 150
CONSELHEIRA_EMOJI_ESPACO = 10
CONSELHEIRA_TITULO_Y = 188
CONSELHEIRA_LEMA_Y = 224
CONSELHEIRA_TEXTO = (160, 270, LARGURA - 320, 140)
CONSELHEIRA_DICA_Y = 470

# a Nova Rainha
NOVA_RAINHA_TITULO_Y = 160
NOVA_RAINHA_TEXTO = (160, 240, LARGURA - 320, 160)
NOVA_RAINHA_DICA_Y = 440

# o cartão da estação
ESTACAO_NOME_Y = ALTURA // 2 - 20
ESTACAO_DICA_Y = ALTURA // 2 + 30

# ============================================================
# 4) EVENTO
# ============================================================
PAINEL_CONTEXTO = (90, 200, LARGURA - 180, 320)
CONTEXTO_MARGEM = 24
CONTEXTO_TITULO_DO_TOPO = 20
CONTEXTO_ABELHA_DA_DIREITA = 110
CONTEXTO_TEXTO_TOPO = 70
CONTEXTO_TEXTO_ALTURA = 200
CONTEXTO_DICA_DA_BASE = 40
CONTEXTO_ABELHA_DA_BASE = 100

# a escolha: o título e os 4 cards
ESCOLHA_TITULO_Y = 205
CARD_LARGURA = 474
CARD_ALTURA = 160
CARD_ESPACO_X = 20
CARD_ESPACO_Y = 16
CARD_COLUNAS = 2
CARD_TOPO = 230
CARD_MARGEM = 14
CARD_NOME_TOPO = 10
CARD_CUSTO_TOPO = 34
CARD_ACAO_TOPO = 54
CARD_ACAO_ALTURA = 100
CARD_RAIO = 12

# ============================================================
# 5) MINIGAME
# ============================================================
PAINEL_PREPARO = (90, 120, LARGURA - 180, 360)
PREPARO_TITULO_Y = 155
PREPARO_PROPOSTA = (140, 190, LARGURA - 280, 50)
PREPARO_INSTRUCAO = (140, 260, LARGURA - 280, 120)
PREPARO_CONTAGEM_Y = 420
PREPARO_DICA_Y = 460
ABELHA_NO_PREPARO = (LARGURA - 150, 150)

PAINEL_MINIGAME = (60, 110, LARGURA - 120, 420)
MINIGAME_TITULO_Y = 140
MINIGAME_PROPOSTA = (110, 165, LARGURA - 220, 50)
MINIGAME_DICA_Y = 470
ABELHA_NO_MINIGAME = (LARGURA - 150, 140)
MINIGAME_AREA = (620, 260)
MINIGAME_CENTRO = (LARGURA // 2, 360)

PAINEL_RESULTADO_DO_MINIGAME = (120, 140, LARGURA - 240, 340)
RESULTADO_TITULO_DO_TOPO = 46
RESULTADO_DETALHE_DO_TOPO = 84
RESULTADO_TEXTOS_DO_TOPO = 120
RESULTADO_MARGEM = 30
RESULTADO_LINHA_ALTURA = 50
RESULTADO_DICA_DA_BASE = 30
ABELHA_DO_PAINEL = (-110, 10)

# ============================================================
# 6) CONSEQUÊNCIA E TELA FINAL
# ============================================================
PAINEL_CONSEQUENCIA = (90, 200, LARGURA - 180, 380)
CONSEQUENCIA_MARGEM = 24
CONSEQUENCIA_TITULO_DO_TOPO = 20
CONSEQUENCIA_ABELHA_DA_DIREITA = 110
CONSEQUENCIA_TEXTO_DO_TOPO = 60
CONSEQUENCIA_RESERVA_DA_ABELHA = 110
CONSEQUENCIA_MARGEM_CENTRALIZADA = 118
CONSEQUENCIA_EXTRA_ALTURA = 40
CONSEQUENCIA_TEXTO_ALTURA = 160
CONSEQUENCIA_AVISO_DA_BASE = 80
CONSEQUENCIA_AVISO_ALTURA = 60
CONSEQUENCIA_DICA_DA_BASE = 24

PAINEL_FINAL = (50, 30, LARGURA - 100, ALTURA - 60)
FINAL_TITULO_DO_TOPO = 32
FINAL_RADAR_CENTRO = (170, 190)
FINAL_RADAR_RAIO = 105
FINAL_COLUNA_X = 350
FINAL_COLUNA_TOPO = 66
CAIXA_ECOLOGIA_MARGEM = 24
CAIXA_ECOLOGIA_DA_BASE = 150
CAIXA_ECOLOGIA_ALTURA = 130
FINAL_PERFIL_TEXTO_ALTURA = 110
COR_TEXTO_ECOLOGIA = (80, 60, 20)
BARRA_DE_TEMPO = (360, 6)
BARRA_DE_TEMPO_DA_BASE = 12


# ============================================================
# funções que calculam retângulos a partir dos números acima
# (quem desenha e quem trata o clique usam as mesmas, então nunca discordam)
# ============================================================
def retangulo(medidas):
    return pygame.Rect(*medidas)


def retangulos_dos_cards(quantidade):
    """Os retângulos dos cards da tela de escolha, na ordem das opções."""
    inicio_x = LARGURA // 2 - (CARD_COLUNAS * CARD_LARGURA + CARD_ESPACO_X) // 2
    retangulos = []
    for i in range(quantidade):
        coluna, linha = i % CARD_COLUNAS, i // CARD_COLUNAS
        retangulos.append(pygame.Rect(
            inicio_x + coluna * (CARD_LARGURA + CARD_ESPACO_X),
            CARD_TOPO + linha * (CARD_ALTURA + CARD_ESPACO_Y),
            CARD_LARGURA, CARD_ALTURA))
    return retangulos


def area_do_minigame():
    """O retângulo onde o minigame é desenhado."""
    area = pygame.Rect(0, 0, *MINIGAME_AREA)
    area.center = MINIGAME_CENTRO
    return area

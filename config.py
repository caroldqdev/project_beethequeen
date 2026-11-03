# -*- coding: utf-8 -*-
"""
CONFIG: todos os números e ajustes do jogo, num lugar só.

  1) JANELA E TEMPO       tamanho da janela, velocidade
  2) EQUILÍBRIO           os números que balanceiam o jogo
  3) RITMO DAS TELAS      quanto cada tela dura, quando a dica do ENTER aparece
  4) FONTES               família e tamanho das letras
  5) NOMES DAS TELAS e VOCABULÁRIO   (estes não se mexe)

O PREÇO de cada opção fica em eventos/; o desconto de um evento pro outro,
em resultados/; a penalidade de cada conselheira, em dados/conselheiras.py.
"""

# ============================================================
# 1) JANELA E TEMPO
# ============================================================
TITULO_DA_JANELA = "Bee the Queen"
LARGURA, ALTURA = 1000, 650
FPS = 60

# ============================================================
# 2) EQUILÍBRIO
# ============================================================
# --- como o jogo começa ---
MEL_INICIAL = 100
OPERARIAS_INICIAIS = 100
RELACAO_INICIAL = 60            # moral/confiança da colmeia
HARMONIA_INICIAL = 50           # cada um dos 5 eixos
AFINIDADE_INICIAL = 40          # de cada conselheira
ESCALA_MAXIMA = 100             # Relação, Harmonia e Afinidade vão de 0 a isto

# --- o que a Relação com a colmeia faz ---
RELACAO_BAIXA = 25              # abaixo disso a colmeia está desmotivada:
PRODUCAO_COM_RELACAO_BAIXA = 0.85    # ...só 85% de todo ganho de Produção
RELACAO_ALTA = 80               # acima disso, escolhas bem-sucedidas rendem mais:
BONUS_RELACAO_ALTA = 1.1        # ...10% a mais no efeito

# --- avisos e perfil final ---
DESEQUILIBRIO_HARMONIA = 45     # diferença entre o maior e o menor eixo que dispara o aviso
MARGEM_PERFIL_EQUILIBRADO = 15  # afinidades mais próximas que isso -> perfil "Equilibrado"

# --- na tela final: afinidade igual ou acima disto = "aliada próxima"; igual ou abaixo = "afastada" ---
AFINIDADE_ALIADA = 70
AFINIDADE_AFASTADA = 20

# --- como o resultado do minigame vira "super_sucesso / sucesso / falha" ---
# (o multiplicador do minigame é 1.0, 0.5 ou 0.25; o +10% da Relação alta
#  também cai em "super_sucesso")
LIMITE_SUPER_SUCESSO = 0.9
LIMITE_SUCESSO = 0.4

# --- dificuldade do minigame por estação (1 a 5) ---
# (um evento pode forçar a sua em minigames/eNN_*.py, com DIFICULDADE = n)
DIFICULDADE_POR_ESTACAO = {"Primavera": 1, "Verao": 2, "Outono": 3, "Inverno": 4}

# --- evento-espelho (o último): o efeito depende do que foi acumulado ---
ESPELHO_MEL_MINIMO = 40                  # Melina: mel guardado >= isso
ESPELHO_RELACAO_MINIMA = 60              # Aurora: Relação >= isso
ESPELHO_EFEITO_RESERVA_OU_RELACAO = 20   # +20 (ou -20) de População
ESPELHO_EIXO_ALTO = 60                   # Flora/Nectar: eixo >= isso
ESPELHO_EIXO_BAIXO = 40                  # eixo < isso
ESPELHO_EFEITO_EIXO = 15                 # +15 se alto, -15 se baixo
ESPELHO_EFEITO_EIXO_NEUTRO = 3           # no meio

# ============================================================
# 3) RITMO DAS TELAS
# ============================================================
TEMPO_DE_PREPARO_DO_MINIGAME = 5.0   # segundos de contagem antes de cada minigame

# {tela: segundos}. Passado esse tempo, a tela avança sozinha, como numa
# animação; apertar ENTER avança na hora. Tela que NÃO está aqui só avança
# com ENTER. (os nomes das telas estão na seção 5)
AVANCO_AUTOMATICO = {
    "abertura": 15,       # a abertura ("Bee the Queen")
    "conselheira": 10,    # cada uma das 4 conselheiras
    "nova_rainha": 10,    # "A Nova Rainha"
    "estacao": 3,         # o cartão "PRIMAVERA", "VERÃO"...
    # "contexto": 20,     # (tire o # para o texto do evento também passar sozinho;
    #                     #  fica de fora por ser texto pra ler com calma)
}

# O texto "Pressione ENTER para..." só aparece depois de tantos segundos na
# tela (0 = aparece logo).
ATRASO_DA_DICA = 5

# Barrinha no pé da tela mostrando quanto falta pra tela passar sozinha.
MOSTRAR_BARRA_DE_TEMPO = False

# ============================================================
# 4) FONTES  --  "nome": (família, tamanho, negrito)
# ============================================================
FONTES = {
    "titulo":        ("georgia", 30, True),    # títulos grandes
    "subtitulo":     ("georgia", 22, True),    # subtítulos
    "corpo":         ("verdana", 16, False),   # texto corrido
    "corpo_negrito": ("verdana", 16, True),    # texto corrido em negrito
    "pequena":       ("verdana", 13, False),   # textos pequenos e dicas
    "botao":         ("verdana", 15, True),    # nome nos cards
}
CENTRALIZAR_TEXTO_DOS_CARDS = True
ABELHA_SEGUNDOS_POR_QUADRO = 0.15   # velocidade do bater de asas
EMOJI_TAMANHO = 48                  # emoji de cada conselheira

# ============================================================
# 5) NOMES DAS TELAS e VOCABULÁRIO  (não mexa)
# ============================================================
ABERTURA = "abertura"
CONSELHEIRA = "conselheira"
NOVA_RAINHA = "nova_rainha"
ESTACAO = "estacao"
CONTEXTO = "contexto"
ESCOLHA = "escolha"
PREPARO = "preparo"
MINIGAME = "minigame"
RESULTADO_DO_MINIGAME = "resultado_do_minigame"
CONSEQUENCIA = "consequencia"
FINAL = "final"

# telas que o ENTER (e o relógio) sabem avançar
TELAS_QUE_AVANCAM = (ABERTURA, CONSELHEIRA, NOVA_RAINHA, ESTACAO, CONTEXTO)

# os três nomes de resultado usados nas pontes (resultados/eNN_*.py)
NOMES_DE_RESULTADO = ("super_sucesso", "sucesso", "falha")
# as três moedas
MOEDAS = ("mel", "operarias", "relacao")


def verificar():
    """Confere os ajustes acima ao abrir o jogo (erro de digitação para tudo,
    com uma mensagem dizendo o que está errado)."""
    for tela, segundos in AVANCO_AUTOMATICO.items():
        if tela not in TELAS_QUE_AVANCAM:
            raise ValueError(f"config.py: AVANCO_AUTOMATICO: a tela {tela!r} não pode passar "
                             f"sozinha. As válidas são: {', '.join(TELAS_QUE_AVANCAM)}.")
        if not isinstance(segundos, (int, float)) or segundos <= 0:
            raise ValueError(f"config.py: AVANCO_AUTOMATICO: o tempo de {tela!r} precisa ser um "
                             f"número maior que zero (veio {segundos!r}).")
    if not isinstance(ATRASO_DA_DICA, (int, float)) or ATRASO_DA_DICA < 0:
        raise ValueError(f"config.py: ATRASO_DA_DICA precisa ser um número (0 ou mais), "
                         f"veio {ATRASO_DA_DICA!r}.")
    for estacao, dificuldade in DIFICULDADE_POR_ESTACAO.items():
        if dificuldade not in (1, 2, 3, 4, 5):
            raise ValueError(f"config.py: DIFICULDADE_POR_ESTACAO: a de {estacao!r} precisa "
                             f"ser de 1 a 5 (veio {dificuldade!r}).")

# -*- coding: utf-8 -*-
"""
O "CSS" DOS TEXTOS: aqui você manda em como cada texto aparece, um por um.

Cada tela é um "card" com nome, e cada texto do card tem um nome também:

    ESTILOS["contexto"]["texto"]   ->   o card "contexto", o texto "texto"

AS PROPRIEDADES (o que dá pra mudar em cada texto)

    alinhamento           "esquerda", "centro" ou "direita"        (text-align)
    alinhamento_vertical  "topo" ou "centro"  -- só nos PARÁGRAFOS: o texto
                          começa no alto da sua caixa, ou fica no meio dela
    deslocamento_x        anda o texto pra direita (+) ou esquerda (-), em pixels
    deslocamento_y        anda o texto pra BAIXO (+) ou pra cima (-), em pixels
                          (como "padding-top"; mexe só nesse texto, não empurra os outros)
    fonte                 uma das de config.py: titulo, subtitulo, corpo,
                          corpo_negrito, pequena, botao
    cor                   (vermelho, verde, azul), de 0 a 255. Em 3 textos a cor é
                          automática: "conselheira" (a cor de cada conselheira) e
                          "resultado" (verde, laranja ou vermelho, conforme o resultado)
    espaco_entre_linhas   só nos parágrafos: pixels entre uma linha e outra
    margem_esquerda       só nos parágrafos: estreita a caixa pela esquerda
    margem_direita        idem, pela direita

E cada card tem a sua parte "_card" (o card inteiro):

    centralizar_bloco     True = o bloco de textos do card fica no MEIO do card na
                          vertical (sem mudar a distância entre os textos)
    padding_topo          anda TODOS os textos do card pra baixo (+) ou pra cima (-)
    margem_lateral        a distância da borda do card, quando o alinhamento é
                          "esquerda" ou "direita"

Ordem em que as coisas acontecem: primeiro o jogo coloca cada texto no seu lugar
(as posições estão em telas/layout.py), depois centraliza o bloco (se
centralizar_bloco), depois soma o padding_topo e o deslocamento de cada texto.

OS CARDS, OS TEXTOS E ONDE MUDAR O QUE ESTÁ ESCRITO
(textos.py = telas/textos.py)

  card                    texto        o que é                          onde está escrito
  ----------------------  -----------  -------------------------------  -------------------------------
  abertura                titulo       BEE THE QUEEN                    textos.py  TITULO_DO_JOGO
                          subtitulo    Ano 1                            textos.py  SUBTITULO_DO_JOGO
                          texto_1      "A Rainha Anciã se aposenta..."  textos.py  ABERTURA_1
                          nomes        "Flora, Melina, Nectar..."       textos.py  ABERTURA_CONSELHEIRAS
                          texto_2      "Cada escolha altera..." + dica  textos.py  ABERTURA_2, DICA_ABERTURA
  conselheira             nome         emoji + nome                     dados/conselheiras.py (a chave do nome)
                          titulo       "Guardiã da ..."                 dados/conselheiras.py  titulo
                          lema         a frase entre aspas              dados/conselheiras.py  lema
                          texto        a apresentação                   dados/conselheiras.py  apresentacao
                          dica         "Pressione ENTER..."             textos.py  DICA_CONSELHEIRA
  nova_rainha             titulo       A Nova Rainha                    textos.py  NOVA_RAINHA_TITULO
                          texto        o texto do meio                  textos.py  NOVA_RAINHA_TEXTO
                          dica         "Pressione ENTER..."             textos.py  DICA_NOVA_RAINHA
  estacao                 nome         PRIMAVERA, VERÃO...              eventos/eNN_*.py "estacao"; textos.py NOMES_DAS_ESTACOES
                          dica         "Pressione ENTER..."             textos.py  DICA_ESTACAO
  contexto                cabecalho    "Primavera - Evento 1: ..."      textos.py  CABECALHO_DO_EVENTO; eventos/eNN_*.py
                          texto        o texto do evento                eventos/eNN_*.py "contexto" (ou a ponte,
                                                                        em resultados/eNN_*.py "proximo"/"frases")
                          dica         "Pressione ENTER..."             textos.py  DICA_CONTEXTO
  escolha                 titulo       "O Conselho se reúne: ..."       textos.py  CABECALHO_DA_ESCOLHA
  (os 4 cards)            card_nome    o nome da conselheira            (a chave em eventos/eNN_*.py)
                          card_custo   "Mel -15  Relação +3"            eventos/eNN_*.py "custo"; textos.py CARD_*
                          card_acao    o que ela propõe                 eventos/eNN_*.py "acao"
  preparo                 titulo       "Preparando: <jogo>"             textos.py  PREPARO_TITULO
                          proposta     "<ela> propôs: ..."              textos.py  PROPOSTA; eventos/eNN_*.py "acao"
                          instrucao    como se joga                     minigames/jogos/<jogo>.py  instrucao
                          contagem     o número da contagem             (calculado pelo jogo)
                          dica         "Pressione ENTER..."             textos.py  DICA_PREPARO
  minigame                titulo       "Execução: <jogo>"               textos.py  MINIGAME_TITULO
                          proposta     "<ela> propôs: ..."              textos.py  PROPOSTA
                          dica         "Pressione ENTER..."             textos.py  DICA_MINIGAME
  resultado_do_minigame   titulo       "Execução bem-sucedida!"...      textos.py  RESULTADO_TITULO
                          detalhe      "O efeito ... (100%)"            textos.py  RESULTADO_DETALHE
                          efeitos      "Efeitos nesta rodada: ..."      textos.py  RESULTADO_EFEITOS
                          custo        "Custo desta escolha: ..."       textos.py  RESULTADO_CUSTO
                          nota         a frase do desconto              resultados/eNN_*.py "proximo"/"notas"
                          penalidade   "Penalidade extra de ..."        dados/conselheiras.py  penalidade_falha/texto
                          dica         "Pressione ENTER..."             textos.py  DICA_RESULTADO_DO_MINIGAME
  consequencia            titulo       "Consequência: ..."              textos.py  CONSEQUENCIA_TITULO
                          efeitos      "Efeitos: ..." (ação direta)     textos.py  CONSEQUENCIA_EFEITOS
                          extra        o texto extra da opção           resultados/eNN_*.py "efeitos"/"extra"
                          texto        a consequência                   resultados/eNN_*.py "consequencia"
                          aviso        o aviso de desequilíbrio         textos.py  AVISO_DE_DESEQUILIBRIO
                          dica         "Pressione ENTER..."             textos.py  DICA_CONSEQUENCIA

(O HUD de cima e a tela final não estão aqui: são painéis com barras e gráfico.)
"""
import config
from telas import layout as L

# ============================================================
# A LISTA DE NOMES (não mexa): o tipo de cada texto
#   "linha"     = uma linha só (título, dica, nome...)
#   "paragrafo" = texto que quebra em várias linhas
# ============================================================
ELEMENTOS = {
    "abertura": {"titulo": "linha", "subtitulo": "linha", "texto_1": "paragrafo",
                 "nomes": "paragrafo", "texto_2": "paragrafo"},
    "conselheira": {"nome": "linha", "titulo": "linha", "lema": "linha", "texto": "paragrafo", "dica": "linha"},
    "nova_rainha": {"titulo": "linha", "texto": "paragrafo", "dica": "linha"},
    "estacao": {"nome": "linha", "dica": "linha"},
    "contexto": {"cabecalho": "linha", "texto": "paragrafo", "dica": "linha"},
    "escolha": {"titulo": "linha", "card_nome": "linha", "card_custo": "linha", "card_acao": "paragrafo"},
    "preparo": {"titulo": "linha", "proposta": "paragrafo", "instrucao": "paragrafo",
                "contagem": "linha", "dica": "linha"},
    "minigame": {"titulo": "linha", "proposta": "paragrafo", "dica": "linha"},
    "resultado_do_minigame": {"titulo": "linha", "detalhe": "linha", "efeitos": "paragrafo", "custo": "paragrafo",
                              "nota": "paragrafo", "penalidade": "paragrafo", "dica": "linha"},
    "consequencia": {"titulo": "linha", "efeitos": "linha", "extra": "paragrafo", "texto": "paragrafo",
                     "aviso": "paragrafo", "dica": "linha"},
}

# ============================================================
# O CSS
# ============================================================
ESTILOS = {

    # ---------------------------------------------------------------- abertura
    "abertura": {
        "_card": {"centralizar_bloco": True, "padding_topo": 0, "margem_lateral": 120},
        "titulo":    {"alinhamento": "centro", "deslocamento_x": 0, "deslocamento_y": 0, "fonte": "titulo", "cor": L.ESCURO},
        "subtitulo": {"alinhamento": "centro", "deslocamento_x": 0, "deslocamento_y": 0, "fonte": "subtitulo", "cor": L.DOURADO},
        "texto_1":   {"alinhamento": "centro", "alinhamento_vertical": "centro", "deslocamento_x": 0, "deslocamento_y": 0,
                      "fonte": "corpo", "cor": L.ESCURO, "espaco_entre_linhas": 6, "margem_esquerda": 0, "margem_direita": 0},
        "nomes":     {"alinhamento": "centro", "alinhamento_vertical": "centro", "deslocamento_x": 0, "deslocamento_y": 0,
                      "fonte": "corpo_negrito", "cor": L.ESCURO, "espaco_entre_linhas": 6, "margem_esquerda": 0, "margem_direita": 0},
        "texto_2":   {"alinhamento": "centro", "alinhamento_vertical": "centro", "deslocamento_x": 0, "deslocamento_y": 0,
                      "fonte": "corpo", "cor": L.ESCURO, "espaco_entre_linhas": 6, "margem_esquerda": 0, "margem_direita": 0},
    },

    # ------------------------------------------------------------ conselheira
    "conselheira": {
        "_card": {"centralizar_bloco": True, "padding_topo": 54, "margem_lateral": 160},
        "nome":   {"alinhamento": "centro", "deslocamento_x": 0, "deslocamento_y": 0, "fonte": "titulo", "cor": "conselheira"},
        "titulo": {"alinhamento": "centro", "deslocamento_x": 0, "deslocamento_y": 0, "fonte": "subtitulo", "cor": L.ESCURO},
        "lema":   {"alinhamento": "centro", "deslocamento_x": 0, "deslocamento_y": 0, "fonte": "corpo", "cor": L.DOURADO},
        "texto":  {"alinhamento": "centro", "alinhamento_vertical": "topo", "deslocamento_x": 0, "deslocamento_y": 0,
                   "fonte": "corpo", "cor": L.ESCURO, "espaco_entre_linhas": 6, "margem_esquerda": 0, "margem_direita": 0},
        "dica":   {"alinhamento": "centro", "deslocamento_x": 0, "deslocamento_y": -80, "fonte": "pequena", "cor": L.ESCURO},
    },

    # ------------------------------------------------------------- nova rainha
    "nova_rainha": {
        "_card": {"centralizar_bloco": True, "padding_topo": 0, "margem_lateral": 160},
        "titulo": {"alinhamento": "centro", "deslocamento_x": 0, "deslocamento_y": 0, "fonte": "titulo", "cor": L.ESCURO},
        "texto":  {"alinhamento": "centro", "alinhamento_vertical": "topo", "deslocamento_x": 0, "deslocamento_y": 0,
                   "fonte": "corpo", "cor": L.CINZA_ESCURO, "espaco_entre_linhas": 6, "margem_esquerda": 0, "margem_direita": 0},
        "dica":   {"alinhamento": "centro", "deslocamento_x": 0, "deslocamento_y": 0, "fonte": "pequena", "cor": L.DOURADO},
    },

    # ----------------------------------------------------------------- estação
    "estacao": {
        "_card": {"centralizar_bloco": False, "padding_topo": 0, "margem_lateral": 40},
        "nome": {"alinhamento": "centro", "deslocamento_x": 0, "deslocamento_y": 0, "fonte": "titulo", "cor": L.BRANCO},
        "dica": {"alinhamento": "centro", "deslocamento_x": 0, "deslocamento_y": 0, "fonte": "corpo", "cor": L.BRANCO},
    },

    # ---------------------------------------------------- o texto do evento
    "contexto": {
        "_card": {"centralizar_bloco": False, "padding_topo": 0, "margem_lateral": 24},
        "cabecalho": {"alinhamento": "centro", "deslocamento_x": 0, "deslocamento_y": 0, "fonte": "subtitulo", "cor": L.ESCURO},
        "texto":     {"alinhamento": "centro", "alinhamento_vertical": "centro", "deslocamento_x": 0, "deslocamento_y": 0,
                      "fonte": "corpo", "cor": L.ESCURO, "espaco_entre_linhas": 6, "margem_esquerda": 0, "margem_direita": 0},
        "dica":      {"alinhamento": "centro", "deslocamento_x": 0, "deslocamento_y": 0, "fonte": "pequena", "cor": L.DOURADO},
    },

    # --------------------------------------- a escolha (título + os 4 cards)
    "escolha": {
        # aqui "_card" é cada um dos 4 cards das conselheiras
        "_card": {"centralizar_bloco": False, "padding_topo": 0, "margem_lateral": 14},
        "titulo":     {"alinhamento": "centro", "deslocamento_x": 0, "deslocamento_y": 0, "fonte": "subtitulo", "cor": L.ESCURO},
        "card_nome":  {"alinhamento": "esquerda", "deslocamento_x": 0, "deslocamento_y": 0, "fonte": "botao", "cor": "conselheira"},
        "card_custo": {"alinhamento": "esquerda", "deslocamento_x": 0, "deslocamento_y": 0, "fonte": "pequena", "cor": L.COR_CUSTO_NO_CARD},
        "card_acao":  {"alinhamento": "esquerda", "alinhamento_vertical": "topo", "deslocamento_x": 0, "deslocamento_y": 0,
                       "fonte": "pequena", "cor": L.ESCURO, "espaco_entre_linhas": 3, "margem_esquerda": 0, "margem_direita": 0},
    },

    # ----------------------------------------------------- preparo do minigame
    "preparo": {
        "_card": {"centralizar_bloco": True, "padding_topo": 0, "margem_lateral": 140},
        "titulo":    {"alinhamento": "centro", "deslocamento_x": 0, "deslocamento_y": 0, "fonte": "subtitulo", "cor": L.ESCURO},
        "proposta":  {"alinhamento": "centro", "alinhamento_vertical": "topo", "deslocamento_x": 0, "deslocamento_y": 0,
                      "fonte": "pequena", "cor": L.CINZA, "espaco_entre_linhas": 6, "margem_esquerda": 0, "margem_direita": 0},
        "instrucao": {"alinhamento": "centro", "alinhamento_vertical": "topo", "deslocamento_x": 0, "deslocamento_y": 0,
                      "fonte": "corpo", "cor": L.ESCURO, "espaco_entre_linhas": 6, "margem_esquerda": 0, "margem_direita": 0},
        "contagem":  {"alinhamento": "centro", "deslocamento_x": 0, "deslocamento_y": 0, "fonte": "titulo", "cor": L.DOURADO},
        "dica":      {"alinhamento": "centro", "deslocamento_x": 0, "deslocamento_y": 0, "fonte": "pequena", "cor": L.ESCURO},
    },

    # ------------------------------------------------ o jogo em andamento
    "minigame": {
        "_card": {"centralizar_bloco": False, "padding_topo": 0, "margem_lateral": 110},
        "titulo":   {"alinhamento": "centro", "deslocamento_x": 0, "deslocamento_y": 0, "fonte": "subtitulo", "cor": L.ESCURO},
        "proposta": {"alinhamento": "esquerda", "alinhamento_vertical": "topo", "deslocamento_x": 0, "deslocamento_y": 0,
                     "fonte": "pequena", "cor": L.ESCURO, "espaco_entre_linhas": 6, "margem_esquerda": 0, "margem_direita": 0},
        "dica":     {"alinhamento": "centro", "deslocamento_x": 0, "deslocamento_y": 0, "fonte": "pequena", "cor": L.ESCURO},
    },

    # ------------------------------------------------ resultado do minigame
    "resultado_do_minigame": {
        "_card": {"centralizar_bloco": True, "padding_topo": 0, "margem_lateral": 30},
        "titulo":     {"alinhamento": "centro", "deslocamento_x": 0, "deslocamento_y": 0, "fonte": "titulo", "cor": "resultado"},
        "detalhe":    {"alinhamento": "centro", "deslocamento_x": 0, "deslocamento_y": 0, "fonte": "corpo", "cor": L.ESCURO},
        "efeitos":    {"alinhamento": "centro", "alinhamento_vertical": "topo", "deslocamento_x": 0, "deslocamento_y": 0,
                       "fonte": "pequena", "cor": L.DOURADO, "espaco_entre_linhas": 6, "margem_esquerda": 0, "margem_direita": 0},
        "custo":      {"alinhamento": "centro", "alinhamento_vertical": "topo", "deslocamento_x": 0, "deslocamento_y": 0,
                       "fonte": "pequena", "cor": L.CINZA, "espaco_entre_linhas": 6, "margem_esquerda": 0, "margem_direita": 0},
        "nota":       {"alinhamento": "centro", "alinhamento_vertical": "topo", "deslocamento_x": 0, "deslocamento_y": 0,
                       "fonte": "pequena", "cor": L.COR_NOTA_DA_PONTE, "espaco_entre_linhas": 6, "margem_esquerda": 0, "margem_direita": 0},
        "penalidade": {"alinhamento": "centro", "alinhamento_vertical": "topo", "deslocamento_x": 0, "deslocamento_y": 0,
                       "fonte": "pequena", "cor": L.COR_PENALIDADE, "espaco_entre_linhas": 6, "margem_esquerda": 0, "margem_direita": 0},
        "dica":       {"alinhamento": "centro", "deslocamento_x": 0, "deslocamento_y": 0, "fonte": "pequena", "cor": L.ESCURO},
    },

    # ------------------------------------------------------------ consequência
    "consequencia": {
        "_card": {"centralizar_bloco": True, "padding_topo": 0, "margem_lateral": 24},
        "titulo":  {"alinhamento": "centro", "deslocamento_x": 0, "deslocamento_y": 0, "fonte": "subtitulo", "cor": L.ESCURO},
        "efeitos": {"alinhamento": "centro", "deslocamento_x": 0, "deslocamento_y": 0, "fonte": "corpo", "cor": L.DOURADO},
        "extra":   {"alinhamento": "centro", "alinhamento_vertical": "topo", "deslocamento_x": 0, "deslocamento_y": 0,
                    "fonte": "pequena", "cor": L.COR_EXTRA, "espaco_entre_linhas": 6, "margem_esquerda": 94, "margem_direita": 94},
        "texto":   {"alinhamento": "centro", "alinhamento_vertical": "topo", "deslocamento_x": 0, "deslocamento_y": 0,
                    "fonte": "corpo", "cor": L.ESCURO, "espaco_entre_linhas": 6, "margem_esquerda": 94, "margem_direita": 94},
        "aviso":   {"alinhamento": "centro", "alinhamento_vertical": "topo", "deslocamento_x": 0, "deslocamento_y": 0,
                    "fonte": "pequena", "cor": L.COR_DESEQUILIBRIO, "espaco_entre_linhas": 6, "margem_esquerda": 0, "margem_direita": 0},
        "dica":    {"alinhamento": "centro", "deslocamento_x": 0, "deslocamento_y": 0, "fonte": "pequena", "cor": L.ESCURO},
    },
}


# ============================================================
# CONFERÊNCIA (roda ao abrir o jogo): avisa qual texto e qual propriedade
# está errada, em vez de o jogo quebrar no meio de uma tela
# ============================================================
_PROPRIEDADES = {
    "linha": ("alinhamento", "deslocamento_x", "deslocamento_y", "fonte", "cor"),
    "paragrafo": ("alinhamento", "alinhamento_vertical", "deslocamento_x", "deslocamento_y", "fonte", "cor",
                  "espaco_entre_linhas", "margem_esquerda", "margem_direita"),
}
_PROPRIEDADES_DO_CARD = ("centralizar_bloco", "padding_topo", "margem_lateral")
_CORES_AUTOMATICAS = {
    "conselheira": {("conselheira", "nome"), ("escolha", "card_nome")},
    "resultado": {("resultado_do_minigame", "titulo")},
}


def _erro(onde, mensagem):
    raise ValueError(f"telas/estilos.py, {onde}: {mensagem}")


def _numero(onde, nome, valor):
    if isinstance(valor, bool) or not isinstance(valor, (int, float)):
        _erro(onde, f"'{nome}' precisa ser um número (veio {valor!r}).")


def verificar():
    for card in ESTILOS:
        if card not in ELEMENTOS:
            _erro(card, f"não existe um card com esse nome. Os cards são: {', '.join(ELEMENTOS)}.")
    for card, elementos in ELEMENTOS.items():
        if card not in ESTILOS:
            _erro(card, "faltou o card inteiro em ESTILOS.")
        estilo_do_card = ESTILOS[card]
        onde = f'"{card}"/"_card"'
        if "_card" not in estilo_do_card:
            _erro(f'"{card}"', 'faltou a parte "_card".')
        for chave in estilo_do_card["_card"]:
            if chave not in _PROPRIEDADES_DO_CARD:
                _erro(onde, f"propriedade desconhecida: {chave!r}. As válidas são: {', '.join(_PROPRIEDADES_DO_CARD)}.")
        for chave in _PROPRIEDADES_DO_CARD:
            if chave not in estilo_do_card["_card"]:
                _erro(onde, f"faltou a propriedade '{chave}'.")
        if not isinstance(estilo_do_card["_card"]["centralizar_bloco"], bool):
            _erro(onde, "'centralizar_bloco' precisa ser True ou False.")
        _numero(onde, "padding_topo", estilo_do_card["_card"]["padding_topo"])
        _numero(onde, "margem_lateral", estilo_do_card["_card"]["margem_lateral"])

        for chave in estilo_do_card:
            if chave != "_card" and chave not in elementos:
                _erro(f'"{card}"', f"não existe um texto chamado {chave!r}. Os textos são: {', '.join(elementos)}.")
        for elemento, tipo in elementos.items():
            onde = f'"{card}"/"{elemento}"'
            if elemento not in estilo_do_card:
                _erro(f'"{card}"', f"faltou o texto '{elemento}'.")
            estilo = estilo_do_card[elemento]
            validas = _PROPRIEDADES[tipo]
            for chave in estilo:
                if chave not in validas:
                    _erro(onde, f"propriedade desconhecida: {chave!r}. As válidas aqui são: {', '.join(validas)}.")
            for chave in validas:
                if chave not in estilo:
                    _erro(onde, f"faltou a propriedade '{chave}'.")
            if estilo["alinhamento"] not in ("esquerda", "centro", "direita"):
                _erro(onde, f"'alinhamento' precisa ser \"esquerda\", \"centro\" ou \"direita\" (veio {estilo['alinhamento']!r}).")
            if tipo == "paragrafo":
                if estilo["alinhamento_vertical"] not in ("topo", "centro"):
                    _erro(onde, f"'alinhamento_vertical' precisa ser \"topo\" ou \"centro\" (veio {estilo['alinhamento_vertical']!r}).")
                for chave in ("espaco_entre_linhas", "margem_esquerda", "margem_direita"):
                    _numero(onde, chave, estilo[chave])
            _numero(onde, "deslocamento_x", estilo["deslocamento_x"])
            _numero(onde, "deslocamento_y", estilo["deslocamento_y"])
            if estilo["fonte"] not in config.FONTES:
                _erro(onde, f"fonte desconhecida: {estilo['fonte']!r}. As válidas são: {', '.join(config.FONTES)}.")
            cor = estilo["cor"]
            if cor in _CORES_AUTOMATICAS:
                if (card, elemento) not in _CORES_AUTOMATICAS[cor]:
                    onde_vale = ", ".join(f"{c}/{e}" for c, e in sorted(_CORES_AUTOMATICAS[cor]))
                    _erro(onde, f'"{cor}" como cor só vale em: {onde_vale} (aqui use uma cor, ex.: (40, 40, 40)).')
            elif not (isinstance(cor, tuple) and len(cor) == 3 and all(isinstance(c, int) and 0 <= c <= 255 for c in cor)):
                _erro(onde, f"'cor' precisa ser (vermelho, verde, azul) de 0 a 255 (veio {cor!r}).")


verificar()

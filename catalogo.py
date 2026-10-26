# -*- coding: utf-8 -*-
"""
O CATÁLOGO: carrega o jogo.

Cada evento tem TRÊS arquivos com o MESMO nome, um em cada pasta:

    eventos/e01_o_novo_jardim.py      a situação (texto, 4 opções, preço)
    minigames/e01_o_novo_jardim.py    qual jogo cada conselheira joga
    resultados/e01_o_novo_jardim.py   o que acontece (efeitos, consequência,
                                      o que muda no próximo evento)

Para ADICIONAR um evento: crie os 3 arquivos (copie os de outro evento) e
acrescente o nome na lista NOMES_DOS_EVENTOS, na ordem em que ele acontece.

Ao abrir o jogo, verificar() confere se os três arquivos de cada evento
combinam entre si (conselheira sem minigame, eixo escrito errado, campo de
nota que não existe...) e para com uma mensagem dizendo QUAL arquivo e o quê.
"""
import importlib
import string

import config
from dados.conselheiras import CONSELHEIRAS, ORDEM
from dados.eixos import EIXOS

# ============================================================
# A LISTA DO JOGO -- a ordem daqui é a ordem dos eventos
# ============================================================
NOMES_DOS_EVENTOS = [
    "e01_o_novo_jardim",
    "e02_enxame_errante",
    "e03_floracao_de_um_so_tipo",
    "e04_a_seca_chega",
    "e05_a_fazenda_com_pesticidas",
    "e06_incendio_nas_redondezas",
    "e07_colonizar_outro_jardim",
    "e08_excesso_de_producao",
    "e09_o_conselho_divide_opinioes",
    "e10_o_frio_chega",
    "e11_teias_na_entrada",
    "e12_a_grande_nevasca",
]


def _importar(pasta, nome):
    try:
        return importlib.import_module(f"{pasta}.{nome}")
    except ModuleNotFoundError as erro:
        if erro.name == f"{pasta}.{nome}":
            if pasta == "introducao":
                raise ValueError(f"Falta o arquivo introducao/{nome}.py -- a introdução precisa de "
                                 f"abertura.py, conselheiras.py e nova_rainha.py.") from None
            raise ValueError(
                f"Falta o arquivo {pasta}/{nome}.py -- cada evento precisa de um arquivo "
                f"com o MESMO nome nas pastas eventos/, minigames/ e resultados/.") from None
        raise


EVENTOS = []        # os eventos, na ordem do jogo
ARQUIVO_DO = {}     # id do evento -> nome do arquivo (para mensagens de erro)
JOGOS = {}          # id do evento -> {conselheira: classe do minigame, ou None}
DIFICULDADES = {}   # id do evento -> dificuldade forçada, ou None
RESULTADOS = {}     # id do evento -> o RESULTADO dele

for _nome in NOMES_DOS_EVENTOS:
    _evento = _importar("eventos", _nome).EVENTO
    _minigames = _importar("minigames", _nome)
    _resultado = _importar("resultados", _nome).RESULTADO
    EVENTOS.append(_evento)
    ARQUIVO_DO[_evento["id"]] = _nome
    JOGOS[_evento["id"]] = _minigames.JOGOS
    DIFICULDADES[_evento["id"]] = getattr(_minigames, "DIFICULDADE", None)
    RESULTADOS[_evento["id"]] = _resultado

# ============================================================
# A INTRODUÇÃO: os textos da abertura, das conselheiras e da Nova Rainha
# (um arquivo para cada, na pasta introducao/)
# ============================================================
INTRODUCAO = {
    "abertura": _importar("introducao", "abertura").ABERTURA,
    "conselheiras": _importar("introducao", "conselheiras").CONSELHEIRAS,
    "nova_rainha": _importar("introducao", "nova_rainha").NOVA_RAINHA,
}


# id de cada evento -> id do evento seguinte (a "ponte" de um resultado só vale pro seguinte)
PROXIMO_ID = {a["id"]: b["id"] for a, b in zip(EVENTOS, EVENTOS[1:])}


# ============================================================
# CONFERÊNCIA (roda uma vez, ao abrir o jogo)
# ============================================================
def _erro(onde, mensagem):
    raise ValueError(f"{onde}: {mensagem}")


def _verificar_proximo(onde, proximo):
    for chave in proximo.get("frases", {}):
        if not (isinstance(chave, tuple) and len(chave) == 2):
            _erro(onde, f"chave inválida em 'frases': {chave!r}. Use ('Conselheira', 'resultado').")
        conselheira, resultado = chave
        if conselheira not in CONSELHEIRAS:
            _erro(onde, f"conselheira desconhecida em 'frases': {conselheira!r}. "
                        f"As válidas são: {', '.join(CONSELHEIRAS)}.")
        if resultado not in config.NOMES_DE_RESULTADO:
            _erro(onde, f"resultado desconhecido em 'frases': {resultado!r}. "
                        f"Os válidos são: {', '.join(config.NOMES_DE_RESULTADO)}.")
    for resultado in proximo.get("fator_custo", {}):
        if resultado not in config.NOMES_DE_RESULTADO:
            _erro(onde, f"resultado desconhecido em 'fator_custo': {resultado!r}. "
                        f"Os válidos são: {', '.join(config.NOMES_DE_RESULTADO)}.")
    for moeda in proximo.get("moedas_afetadas", []):
        if moeda not in config.MOEDAS:
            _erro(onde, f"moeda desconhecida em 'moedas_afetadas': {moeda!r}. "
                        f"As válidas são: {', '.join(config.MOEDAS)}.")
    campos_validos = {f"{m}_{k}" for m in config.MOEDAS for k in ("normal", "final", "diferenca")}
    for resultado, texto in proximo.get("notas", {}).items():
        if resultado not in config.NOMES_DE_RESULTADO:
            _erro(onde, f"resultado desconhecido em 'notas': {resultado!r}. "
                        f"Os válidos são: {', '.join(config.NOMES_DE_RESULTADO)}.")
        try:
            campos = [c for _, c, _, _ in string.Formatter().parse(texto) if c is not None]
        except ValueError as exc:
            raise ValueError(f"{onde}: frase de 'notas' ({resultado}) com chaves mal formadas "
                             f"({exc}). Cada campo deve estar inteiro, ex.: {{mel_final}}.") from None
        for campo in campos:
            if campo not in campos_validos:
                _erro(onde, f"'notas' ({resultado}) usa {{{campo}}}, que não existe. "
                            f"Os campos válidos são: {', '.join(sorted(campos_validos))}.")


def _verificar_introducao():
    esperados = {
        "abertura": ("titulo", "subtitulo", "texto_1", "nomes", "texto_2"),
        "nova_rainha": ("titulo", "texto"),
    }
    for arquivo, textos_esperados in esperados.items():
        onde = f"introducao/{arquivo}.py"
        conteudo = INTRODUCAO[arquivo]
        for chave in textos_esperados:
            if chave not in conteudo:
                _erro(onde, f"faltou o texto '{chave}'.")
        for chave, valor in conteudo.items():
            if chave not in textos_esperados:
                _erro(onde, f"texto desconhecido: {chave!r}. Os válidos são: {', '.join(textos_esperados)}.")
            if not isinstance(valor, str):
                _erro(onde, f"'{chave}' precisa ser um texto entre aspas (veio {valor!r}).")

    onde = "introducao/conselheiras.py"
    campos = ("titulo", "lema", "apresentacao")
    for nome in ORDEM:
        if nome not in INTRODUCAO["conselheiras"]:
            _erro(onde, f"falta a apresentação de {nome} (ela está em ORDEM, em dados/conselheiras.py).")
    for nome, conteudo in INTRODUCAO["conselheiras"].items():
        if nome not in CONSELHEIRAS:
            _erro(onde, f"conselheira desconhecida: {nome!r}. As válidas são: {', '.join(CONSELHEIRAS)}.")
        for chave in campos:
            if chave not in conteudo:
                _erro(onde, f"faltou o texto '{chave}' de {nome}.")
        for chave, valor in conteudo.items():
            if chave not in campos:
                _erro(onde, f"texto desconhecido em {nome}: {chave!r}. Os válidos são: {', '.join(campos)}.")
            if not isinstance(valor, str):
                _erro(onde, f"'{chave}' de {nome} precisa ser um texto entre aspas (veio {valor!r}).")

    # sobra de versões antigas: esses textos agora ficam em introducao/conselheiras.py
    sobras = [c for c in campos if any(c in dados for dados in CONSELHEIRAS.values())]
    if sobras:
        print(f"AVISO: dados/conselheiras.py ainda tem {', '.join(sobras)} das conselheiras; esses textos agora "
              f"ficam em introducao/conselheiras.py (o jogo ignora os de lá, pode apagar essas linhas).")


def verificar():
    _verificar_introducao()
    ids = [ev["id"] for ev in EVENTOS]
    if len(set(ids)) != len(ids):
        _erro("catalogo.py", f"há ids de evento repetidos: {ids}")

    for ev in EVENTOS:
        if ev["estacao"] not in config.DIFICULDADE_POR_ESTACAO:
            print(f"AVISO: eventos/{ARQUIVO_DO[ev['id']]}.py: a estação {ev['estacao']!r} não está em "
                  f"DIFICULDADE_POR_ESTACAO (config.py); os minigames usarão dificuldade 1.")
    for ev in EVENTOS:
        nome = ARQUIVO_DO[ev["id"]]
        jogos, resultado = JOGOS[ev["id"]], RESULTADOS[ev["id"]]
        dificuldade = DIFICULDADES[ev["id"]]
        if dificuldade is not None and dificuldade not in (1, 2, 3, 4, 5):
            _erro(f"minigames/{nome}.py", f"DIFICULDADE precisa ser de 1 a 5 (veio {dificuldade!r}).")
        if "consequencia" not in resultado or "efeitos" not in resultado:
            _erro(f"resultados/{nome}.py", "precisa ter 'consequencia' e 'efeitos'.")

        conselheiras_do_evento = [o["conselheira"] for o in ev["opcoes"]]
        if len(set(conselheiras_do_evento)) != len(conselheiras_do_evento):
            _erro(f"eventos/{nome}.py", "uma conselheira aparece em duas opções.")

        for opcao in ev["opcoes"]:
            c = opcao["conselheira"]
            if c not in CONSELHEIRAS:
                _erro(f"eventos/{nome}.py", f"conselheira desconhecida: {c!r}. "
                                            f"As válidas são: {', '.join(CONSELHEIRAS)}.")
            for moeda, valor in opcao["custo"].items():
                if moeda not in config.MOEDAS:
                    _erro(f"eventos/{nome}.py", f"moeda desconhecida no custo de {c}: {moeda!r}. "
                                                f"As válidas são: {', '.join(config.MOEDAS)}.")
                if not (isinstance(valor, (int, float)) or valor == "tudo"):
                    _erro(f"eventos/{nome}.py", f"custo de {moeda} de {c} precisa ser número "
                                                f"ou \"tudo\" (veio {valor!r}).")
            if c not in jogos:
                _erro(f"minigames/{nome}.py", f"falta o jogo de {c} em JOGOS "
                                              f"(use None para ação direta, sem minigame).")
            if jogos[c] is not None and not callable(jogos[c]):
                _erro(f"minigames/{nome}.py", f"o jogo de {c} precisa ser uma classe (ou None).")
            if c not in resultado["efeitos"]:
                _erro(f"resultados/{nome}.py", f"faltam os efeitos de {c} em 'efeitos'.")
            efeito = resultado["efeitos"][c]
            for eixo in efeito.get("harmonia", {}):
                if eixo not in EIXOS:
                    _erro(f"resultados/{nome}.py", f"eixo desconhecido nos efeitos de {c}: {eixo!r}. "
                                                   f"Os válidos são: {', '.join(EIXOS)}.")
            espelho = efeito.get("espelho")
            if espelho is not None and espelho not in ("reserva_mel", "relacao") and espelho not in EIXOS:
                _erro(f"resultados/{nome}.py", f"'espelho' de {c} desconhecido: {espelho!r}. "
                                               f"Use reserva_mel, relacao ou um eixo ({', '.join(EIXOS)}).")
            if "harmonia" not in efeito and espelho is None:
                _erro(f"resultados/{nome}.py", f"os efeitos de {c} precisam de 'harmonia' ou 'espelho'.")
            afinidade = efeito.get("afinidade", {})
            if "propria" not in afinidade or "demais" not in afinidade:
                _erro(f"resultados/{nome}.py", f"a 'afinidade' de {c} precisa de 'propria' e 'demais'.")
        for c in jogos:
            if c not in conselheiras_do_evento:
                _erro(f"minigames/{nome}.py", f"{c} está em JOGOS mas não tem opção neste evento.")

        proximo = resultado.get("proximo")
        if proximo:
            _verificar_proximo(f"resultados/{nome}.py", proximo)

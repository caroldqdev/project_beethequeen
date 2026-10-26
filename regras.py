# -*- coding: utf-8 -*-
"""
AS REGRAS do jogo: o que acontece com Mel, Operárias, Relação, Harmonia e
Afinidade quando o jogador escolhe algo.

Este arquivo NÃO desenha nada (isso é telas/) e NÃO decide qual tela vem
depois (isso é o main.py). Ele só calcula: recebe o estado e a escolha e
devolve "o que mudou". Os números que balanceiam o jogo estão em config.py.

De onde vem cada coisa:
  - o PREÇO da opção              eventos/eNN_*.py        ("custo")
  - os EFEITOS (Harmonia, afinidade) resultados/eNN_*.py  ("efeitos")
  - a penalidade de falha         dados/conselheiras.py   ("penalidade_falha")
  - o que o evento ANTERIOR muda  resultados/eNN_*.py     ("proximo")
"""
import string

import catalogo
import config
from dados.conselheiras import CONSELHEIRAS
from dados.eixos import EIXOS, ROTULOS


class Estado:
    """Os números do jogo agora."""

    def __init__(self):
        self.mel = config.MEL_INICIAL
        self.operarias = config.OPERARIAS_INICIAIS
        self.relacao = config.RELACAO_INICIAL
        self.harmonia = {eixo: config.HARMONIA_INICIAL for eixo in EIXOS}
        self.afinidade = {nome: config.AFINIDADE_INICIAL for nome in CONSELHEIRAS}
        # uma linha por escolha já feita: (id do evento, conselheira, multiplicador)
        self.historico = []
        # penalidade da Aurora: multiplica o PRÓXIMO ganho de Cooperação
        self.multiplicador_proxima_cooperacao = 1.0


class Resolucao:
    """O que uma escolha produziu -- as telas de resultado mostram isto."""

    def __init__(self):
        self.multiplicador = 1.0
        self.efeitos = []        # [(nome na tela, mudança)]  ex.: [("Biodiversidade", 8)]
        self.custos = {}         # {moeda: mudança}, só o que mudou  ex.: {"mel": -15}
        self.nota_da_ponte = None    # a frase que explica o desconto, se houver
        self.penalidade = None   # texto da penalidade extra de falha, se houve
        self.extra = None        # texto extra da opção, se houver


# ============================================================
# perguntas simples sobre o estado
# ============================================================
def producao_penalizada(estado):
    """Relação baixa: a colmeia está desmotivada e a Produção rende menos."""
    return estado.relacao < config.RELACAO_BAIXA


def harmonia_desequilibrada(estado):
    valores = estado.harmonia.values()
    return max(valores) - min(valores) >= config.DESEQUILIBRIO_HARMONIA


def perfil_dominante(estado):
    """Perfil final: a conselheira com mais afinidade, ou "Equilibrado"."""
    maior = max(estado.afinidade.values())
    topo = [nome for nome, v in estado.afinidade.items() if v == maior]
    folga = max(estado.afinidade.values()) - min(estado.afinidade.values())
    if len(topo) > 1 or folga < config.MARGEM_PERFIL_EQUILIBRADO:
        return "Equilibrado"
    return topo[0]


def nome_do_resultado(multiplicador):
    """Traduz o multiplicador do minigame em 'super_sucesso', 'sucesso' ou 'falha'."""
    if multiplicador >= config.LIMITE_SUPER_SUCESSO:
        return "super_sucesso"
    if multiplicador >= config.LIMITE_SUCESSO:
        return "sucesso"
    return "falha"


# ============================================================
# A PONTE: o que o evento ANTERIOR muda no evento de agora
# (os dados estão em resultados/eNN_*.py, na chave "proximo")
# ============================================================
def _ponte_para(evento, estado):
    """(ponte, conselheira, resultado) do evento anterior -- ou (None, None, None)
    se não houve evento anterior, ele não tem ponte, ou este não é o seguinte."""
    if not estado.historico:
        return None, None, None
    id_anterior, conselheira, multiplicador = estado.historico[-1]
    if catalogo.PROXIMO_ID.get(id_anterior) != evento["id"]:
        return None, None, None
    ponte = catalogo.RESULTADOS[id_anterior].get("proximo")
    if not ponte:
        return None, None, None
    return ponte, conselheira, nome_do_resultado(multiplicador)


def texto_de_abertura(evento, estado):
    """O texto de abertura do evento: a frase da ponte (conforme o evento
    anterior), ou o texto normal do evento."""
    ponte, conselheira, resultado = _ponte_para(evento, estado)
    if ponte is None:
        return evento["contexto"]
    return ponte.get("frases", {}).get((conselheira, resultado)) or evento["contexto"]


def _ajustar_custo(evento, estado, moeda, valor):
    """Aplica o desconto/encarecimento da ponte a um custo. Ganhos (>= 0) e
    moedas fora de 'moedas_afetadas' passam sem mudar."""
    if valor >= 0:
        return valor
    ponte, _, resultado = _ponte_para(evento, estado)
    if ponte is None or moeda not in ponte.get("moedas_afetadas", []):
        return valor
    return valor * ponte.get("fator_custo", {}).get(resultado, 1.0)


_NOTAS_PADRAO = {
    "mais_barato": ("O resultado do evento anterior foi um SUPER SUCESSO -- "
                    "esta escolha saiu mais barata do que o normal."),
    "mais_caro": ("O resultado do evento anterior foi uma FALHA -- "
                  "esta escolha saiu mais cara do que o normal."),
    "normal": ("O resultado do evento anterior foi um SUCESSO normal -- "
               "esta escolha custou o valor de sempre."),
}


def _nota_da_ponte(evento, estado, detalhe_do_custo):
    """A frase que explica o desconto. `detalhe_do_custo` é {moeda: (normal, final)}.
    Usa as 'notas' da ponte; se faltar, uma frase padrão. None = nada a mostrar."""
    ponte, _, resultado = _ponte_para(evento, estado)
    if ponte is None:
        return None
    modelo = ponte.get("notas", {}).get(resultado)
    if modelo:
        valores = {}
        for moeda in config.MOEDAS:
            normal, final = detalhe_do_custo.get(moeda, (0, 0))
            valores[f"{moeda}_normal"] = abs(normal)
            valores[f"{moeda}_final"] = abs(final)
            valores[f"{moeda}_diferenca"] = abs(final - normal)
        return modelo.format(**valores)
    fator = ponte.get("fator_custo")
    if not fator:
        return None          # ponte só de texto: não há desconto pra explicar
    f = fator.get(resultado, 1.0)
    if f < 1.0:
        return _NOTAS_PADRAO["mais_barato"]
    if f > 1.0:
        return _NOTAS_PADRAO["mais_caro"]
    return _NOTAS_PADRAO["normal"]


# ============================================================
# A ESCOLHA
# ============================================================
def _nome_do_efeito(chave):
    if chave in ROTULOS:
        return ROTULOS[chave]
    if chave == "populacao (via relacao)":
        return ROTULOS["populacao"] + " (via relação)"
    return chave.capitalize()


def _limitar(valor):
    return max(0, min(config.ESCALA_MAXIMA, valor))


def _penalidade_de_falha(estado, conselheira):
    """Perda extra quando o minigame não vai bem (a de cada conselheira está
    em dados/conselheiras.py). Devolve o texto dela."""
    pen = CONSELHEIRAS[conselheira].get("penalidade_falha")
    if not pen:
        return None
    if "operarias" in pen:
        estado.operarias = max(0, estado.operarias + pen["operarias"])
    if "mel" in pen:
        estado.mel = max(0, estado.mel + pen["mel"])
    if "relacao" in pen:
        estado.relacao = _limitar(estado.relacao + pen["relacao"])
    if "enfraquece_proxima_cooperacao" in pen:
        estado.multiplicador_proxima_cooperacao = pen["enfraquece_proxima_cooperacao"]
    return pen.get("texto")


def _aplicar_custo(estado, evento, opcao, multiplicador):
    """Tira (ou põe) as moedas do preço da opção. Devolve {moeda: (normal, final)}:
    o que seria pago SEM o desconto da ponte e o que foi pago COM ele."""
    detalhe = {}

    def delta(moeda, base, escala_pelo_minigame):
        normal = base * multiplicador if (escala_pelo_minigame and base < 0) else base
        final = _ajustar_custo(evento, estado, moeda, normal)
        detalhe[moeda] = (int(round(normal)), int(round(final)))
        return int(round(final))

    custo = opcao["custo"]
    mel = custo.get("mel", 0)
    if mel == "tudo":
        detalhe["mel"] = (-estado.mel, -estado.mel)
        estado.mel = 0
    elif isinstance(mel, (int, float)):
        estado.mel = max(0, estado.mel + delta("mel", mel, True))
    operarias = custo.get("operarias", 0)
    if isinstance(operarias, (int, float)):
        estado.operarias = max(0, estado.operarias + delta("operarias", operarias, True))
    relacao = custo.get("relacao", 0)
    if isinstance(relacao, (int, float)):
        estado.relacao = _limitar(estado.relacao + delta("relacao", relacao, False))
    return detalhe


def _aplicar_efeitos(estado, efeito, multiplicador):
    """Muda a Harmonia. Devolve {chave do efeito: mudança}."""
    aplicados = {}
    espelho = efeito.get("espelho")
    if espelho:                                   # evento-espelho: depende do que foi acumulado
        if espelho == "reserva_mel":
            base = (config.ESPELHO_EFEITO_RESERVA_OU_RELACAO if estado.mel >= config.ESPELHO_MEL_MINIMO
                    else -config.ESPELHO_EFEITO_RESERVA_OU_RELACAO)
            estado.harmonia["populacao"] = _limitar(estado.harmonia["populacao"] + int(base * multiplicador))
            aplicados["populacao"] = int(base * multiplicador)
        elif espelho == "relacao":
            base = (config.ESPELHO_EFEITO_RESERVA_OU_RELACAO if estado.relacao >= config.ESPELHO_RELACAO_MINIMA
                    else -config.ESPELHO_EFEITO_RESERVA_OU_RELACAO)
            estado.harmonia["populacao"] = _limitar(estado.harmonia["populacao"] + int(base * multiplicador))
            aplicados["populacao (via relacao)"] = int(base * multiplicador)
        else:
            atual = estado.harmonia.get(espelho, config.HARMONIA_INICIAL)
            if atual >= config.ESPELHO_EIXO_ALTO:
                base = config.ESPELHO_EFEITO_EIXO
            elif atual < config.ESPELHO_EIXO_BAIXO:
                base = -config.ESPELHO_EFEITO_EIXO
            else:
                base = config.ESPELHO_EFEITO_EIXO_NEUTRO
            estado.harmonia[espelho] = _limitar(estado.harmonia[espelho] + int(base * multiplicador))
            aplicados[espelho] = int(base * multiplicador)
        return aplicados

    for eixo, valor in efeito.get("harmonia", {}).items():
        mudanca = int(round(valor * multiplicador))
        # Relação baixa: a colmeia desmotivada rende menos Produção
        if eixo == "producao" and mudanca > 0 and producao_penalizada(estado):
            mudanca = int(round(mudanca * config.PRODUCAO_COM_RELACAO_BAIXA))
        # Penalidade da Aurora: o próximo ganho de Cooperação vale menos
        if eixo == "cooperacao" and mudanca > 0 and estado.multiplicador_proxima_cooperacao < 1.0:
            mudanca = int(round(mudanca * estado.multiplicador_proxima_cooperacao))
            estado.multiplicador_proxima_cooperacao = 1.0
        estado.harmonia[eixo] = _limitar(estado.harmonia[eixo] + mudanca)
        aplicados[eixo] = mudanca
    return aplicados


def _aplicar_afinidade(estado, conselheira, afinidade):
    estado.afinidade[conselheira] = _limitar(estado.afinidade[conselheira] + afinidade.get("propria", 0))
    for nome in CONSELHEIRAS:
        if nome != conselheira:
            estado.afinidade[nome] = _limitar(estado.afinidade[nome] + afinidade.get("demais", 0))


def resolver(estado, evento, opcao, multiplicador):
    """Fecha uma escolha: penalidade de falha, custo, efeitos, afinidade e
    histórico. `multiplicador` é o desempenho no minigame (1.0, 0.5, 0.25...).
    Muda o `estado` e devolve uma Resolucao com o que mudou, pras telas mostrarem."""
    conselheira = opcao["conselheira"]
    efeito = catalogo.RESULTADOS[evento["id"]]["efeitos"][conselheira]
    res = Resolucao()

    # Relação alta: bônus de diálogo no efeito
    if estado.relacao > config.RELACAO_ALTA and multiplicador >= 1.0:
        multiplicador *= config.BONUS_RELACAO_ALTA
    res.multiplicador = multiplicador
    if multiplicador < 1.0:
        res.penalidade = _penalidade_de_falha(estado, conselheira)

    # (a foto antes serve pra mostrar exatamente quanto mudou de cada moeda)
    antes = {"mel": estado.mel, "operarias": estado.operarias, "relacao": estado.relacao}
    detalhe = _aplicar_custo(estado, evento, opcao, multiplicador)
    aplicados = _aplicar_efeitos(estado, efeito, multiplicador)
    _aplicar_afinidade(estado, conselheira, efeito["afinidade"])

    # a frase do desconto fala do evento ANTERIOR: tem que vir antes de gravar este
    res.nota_da_ponte = _nota_da_ponte(evento, estado, detalhe)
    estado.historico.append((evento["id"], conselheira, multiplicador))

    for moeda in config.MOEDAS:
        mudou = getattr(estado, moeda) - antes[moeda]
        if mudou:
            res.custos[moeda] = mudou
    res.efeitos = [(_nome_do_efeito(chave), valor) for chave, valor in aplicados.items()]
    res.extra = efeito.get("extra")
    return res

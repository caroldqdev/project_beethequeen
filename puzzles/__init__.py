# -*- coding: utf-8 -*-
"""
Ponto unico de acesso aos minigames.

O resto do codigo importa so daqui:

    from puzzles import make_puzzle, get_instructions

FASE ATUAL: os 4 minigames abaixo (um por conselheira) sao usados em
TODOS os eventos por enquanto -- Flora sempre joga "Sob as Folhas",
Melina sempre "Rastro de Pólen", Nectar sempre "Rota de Voo" e Aurora
sempre "Antes da Poda", nao importa o evento. A ideia e ir trocando por
minigames proprios de cada evento aos poucos (como fizemos com o
Evento 1), editando o campo 'puzzle' de cada opcao em data/events/*.py e
criando o minigame novo aqui.
"""
from .base import BasePuzzle
from .sob_as_folhas import SobAsFolhas
from .rastro_de_polen import RastroDePolen
from .rota_de_voo import RotaDeVoo
from .antes_da_poda import AntesDaPoda

_MECHANICS = [
    (SobAsFolhas, "Sob as Folhas"),
    (RastroDePolen, "Rastro de Pólen"),
    (RotaDeVoo, "Rota de Voo"),
    (AntesDaPoda, "Antes da Poda"),
]

# Texto de instrucao mostrado na tela de preparo (briefing), antes do
# minigame comecar de fato.
INSTRUCTIONS = {
    "Sob as Folhas": "Clique nas folhas para remove-las. Embaixo de 6 delas "
                      "ha insetos escondidos -- remova TODAS as folhas sem "
                      "acertar os insetos.",
    "Rastro de Pólen": "Arraste o mouse (mantendo o botao pressionado) para "
                        "polinizar o campo de amarelo. Cubra o maximo "
                        "possivel antes que o tempo acabe.",
    "Rota de Voo": "Clique na flor numero 1 e arraste ate a ultima, passando "
                    "por TODAS as celulas do campo sem repetir nenhuma. Os "
                    "numeros devem ser visitados em ordem. Tecla R reinicia.",
    "Antes da Poda": "Arraste o mouse para polinizar de amarelo antes que o "
                      "jardineiro (vermelho) avance sozinho. Cubra 70% do "
                      "campo antes dele.",
}


def make_puzzle(puzzle_name, rect, difficulty=1, relacao=100):
    """Fabrica: casa o nome do puzzle salvo em data/events/*.py (que pode
    ter um sufixo tipo '(tempo reduzido)') com a mecanica-base correspondente.
    Se o evento ainda nao tem minigame proprio, cai no fallback generico."""
    if not puzzle_name:
        return None
    for cls, base_name in _MECHANICS:
        if puzzle_name.startswith(base_name):
            return cls(rect, difficulty=difficulty, relacao=relacao)
    return BasePuzzle(rect, difficulty=difficulty, relacao=relacao)


def get_instructions(puzzle_name):
    if not puzzle_name:
        return "Uma acao direta sera executada, sem minigame."
    for _, base_name in _MECHANICS:
        if puzzle_name.startswith(base_name):
            return INSTRUCTIONS.get(base_name, "")
    return "Pressione ESPACO para travar o marcador na zona certa."


# Compatibilidade com codigo antigo que importava PuzzleState diretamente.
PuzzleState = BasePuzzle

__all__ = ["make_puzzle", "get_instructions", "BasePuzzle",
           "SobAsFolhas", "RastroDePolen", "RotaDeVoo", "AntesDaPoda"]

# -*- coding: utf-8 -*-
"""
Ponto unico de acesso aos dados do jogo.

O resto do codigo (main.py, game/*) importa so daqui:

    from data import EVENTS, COUNCILORS, FAIL_PENALTY, HARMONIA_AXES, ...

Por baixo dos panos, cada pedaco de conteudo mora no seu proprio arquivo:

    data/events/e01_*.py ... e12_*.py   -> um arquivo por evento
    data/councilors.py                  -> COUNCILORS, FAIL_PENALTY
    data/axes.py                        -> HARMONIA_AXES, HARMONIA_LABELS
    data/profiles.py                    -> PROFILE_TEXTS, ECOLOGY_MESSAGE

Se voce quer editar um evento especifico, vai direto no arquivo dele em
data/events/. Se quer mudar a fala ou o perfil de uma conselheira, vai em
data/councilors.py ou data/profiles.py.
"""
from .events import EVENTS
from .councilors import COUNCILORS, FAIL_PENALTY
from .axes import HARMONIA_AXES, HARMONIA_LABELS
from .profiles import PROFILE_TEXTS, ECOLOGY_MESSAGE

__all__ = [
    "EVENTS", "COUNCILORS", "FAIL_PENALTY",
    "HARMONIA_AXES", "HARMONIA_LABELS",
    "PROFILE_TEXTS", "ECOLOGY_MESSAGE",
]

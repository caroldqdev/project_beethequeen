# -*- coding: utf-8 -*-
"""Junta os 12 eventos (um arquivo por evento) numa lista EVENTS,
na ordem correta, para o resto do jogo consumir como antes."""

from .e01_o_novo_jardim import EVENT as _e01_o_novo_jardim
from .e02_enxame_errante import EVENT as _e02_enxame_errante
from .e03_floracao_de_um_so_tipo import EVENT as _e03_floracao_de_um_so_tipo
from .e04_a_seca_chega import EVENT as _e04_a_seca_chega
from .e05_a_fazenda_com_pesticidas import EVENT as _e05_a_fazenda_com_pesticidas
from .e06_incendio_nas_redondezas import EVENT as _e06_incendio_nas_redondezas
from .e07_colonizar_outro_jardim import EVENT as _e07_colonizar_outro_jardim
from .e08_excesso_de_producao import EVENT as _e08_excesso_de_producao
from .e09_o_conselho_divide_opinioes import EVENT as _e09_o_conselho_divide_opinioes
from .e10_o_frio_chega import EVENT as _e10_o_frio_chega
from .e11_teias_na_entrada import EVENT as _e11_teias_na_entrada
from .e12_a_grande_nevasca import EVENT as _e12_a_grande_nevasca

EVENTS = [
    _e01_o_novo_jardim,
    _e02_enxame_errante,
    _e03_floracao_de_um_so_tipo,
    _e04_a_seca_chega,
    _e05_a_fazenda_com_pesticidas,
    _e06_incendio_nas_redondezas,
    _e07_colonizar_outro_jardim,
    _e08_excesso_de_producao,
    _e09_o_conselho_divide_opinioes,
    _e10_o_frio_chega,
    _e11_teias_na_entrada,
    _e12_a_grande_nevasca,
]


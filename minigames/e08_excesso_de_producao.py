# -*- coding: utf-8 -*-
"""Minigames do Evento 8 — Excesso de Producao.

Aqui fica SÓ a escolha do jogo de cada conselheira neste evento. O código de
cada jogo mora em minigames/jogos/ (e o texto de instrução, dentro de cada jogo).
Para criar um minigame só deste evento, escreva a classe aqui mesmo (ou em um
arquivo novo) e troque o jogo da conselheira abaixo.
"""
from minigames.jogos.rastro_de_polen import RastroDePolen
from minigames.jogos.rota_de_voo import RotaDeVoo
from minigames.jogos.sob_as_folhas import SobAsFolhas

JOGOS = {
    "Melina": RastroDePolen,
    "Nectar": RotaDeVoo,
    "Flora": SobAsFolhas,
    "Aurora": RastroDePolen,
}

# DIFICULDADE = 2   # (opcional) força a dificuldade (1 a 5) só neste evento;
#                   # sem isso, ela vem da estação (config.py)

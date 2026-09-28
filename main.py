# -*- coding: utf-8 -*-
"""
Bee the Queen — Ano 1:

Este arquivo e so o PONTO DE ENTRADA. Todo o codigo de verdade mora em
pastas separadas por responsabilidade:

    data/       -> TODO o conteudo do jogo (os 12 eventos, falas das
                   conselheiras, textos de perfil final). E aqui que
                   voce mexe pra mudar O QUE o jogo diz.
    puzzles/    -> os 8 minigames, um arquivo por mecanica.
    ui/         -> desenho do radar de Harmonia e das barrinhas.
    game/       -> o "motor" do jogo (regras, telas, loop de eventos).
                   E aqui que voce mexe pra mudar COMO o jogo funciona
                   ou aparece.
    assets/     -> imagens (sprites, fundo).

Veja o README.md para o mapa completo de onde encontrar cada coisa.

Como rodar:
    pip install pygame
    python main.py
"""
from game.core import Game

if __name__ == "__main__":
    Game().run()

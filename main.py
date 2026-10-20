# -*- coding: utf-8 -*-
"""
Bee the Queen — Ano 1

ESTE ARQUIVO É SÓ O ORQUESTRADOR: decide a ORDEM das coisas. Para cada
evento ele faz, em sequência:

    1. puxa o EVENTO         eventos/eNN_*.py     e mostra o texto e as 4 opções
    2. puxa o MINIGAME       minigames/eNN_*.py   do que a jogadora escolheu
    3. puxa o RESULTADO      resultados/eNN_*.py  efeitos, consequência e o que
                                                  muda no próximo evento
    4. volta ao passo 1 com o próximo evento

Ele não calcula número nenhum e não desenha nada: chama quem faz isso.

QUEM FAZ O QUE
    main.py          orquestrador: a ordem das telas, as teclas, o laço do jogo
    config.py        todos os números e ajustes (equilíbrio, tempos, fontes)
    regras.py        as regras: custo, efeitos, penalidade, a ponte entre eventos
    catalogo.py      a lista de eventos (carrega os 3 arquivos de cada um)
    eventos/         a SITUAÇÃO: texto, 4 opções, preço
    minigames/       qual JOGO cada conselheira joga em cada evento
      jogos/         o código de cada jogo
    resultados/      o que ACONTECE: efeitos, consequência, o que muda no próximo
    dados/           conselheiras, eixos da Harmonia, perfis finais
    telas/           tudo que aparece na tela (layout.py = posições,
                     textos.py = textos fixos, o resto = uma tela por função)

ONDE MEXER
    texto ou preço de uma opção                 eventos/eNN_*.py
    qual jogo uma conselheira joga              minigames/eNN_*.py
    efeitos, consequência, ponte p/ o próximo   resultados/eNN_*.py
    um número do jogo (mel inicial, bônus...)   config.py
    tempo das telas, letras                     config.py
    posição/cor de algo na tela                 telas/layout.py
    texto fixo de uma tela                      telas/textos.py
    ordem das telas / o que uma tecla faz       este arquivo
    adicionar um evento                         os 3 arquivos + catalogo.py

Como rodar:
    pip install pygame
    python main.py
"""
import sys
import pygame

import catalogo
import config
import regras
from dados.conselheiras import ORDEM
from telas import desenho, layout
from telas.visual import Visual


class Jogo:

    def __init__(self):
        config.verificar()
        catalogo.verificar()
        self.visual = Visual()           # janela, fontes, imagens (telas/visual.py)
        self.estado = regras.Estado()    # os números do jogo      (regras.py)

        # --- onde o jogo está: só o orquestrador mexe nisto ---
        self.tela = config.ABERTURA
        self.indice_do_evento = 0
        self.estacao_atual = None
        self.indice_conselheira = 0
        self.opcao = None                # a opção que a jogadora escolheu
        self.classe_do_minigame = None
        self.minigame = None             # o jogo em andamento
        self.teve_minigame = False       # a escolha tinha minigame? (ação direta = não)
        self.nome_do_minigame = ""
        self.instrucao_do_minigame = ""
        self.dificuldade = 1
        self.tempo_de_preparo = config.TEMPO_DE_PREPARO_DO_MINIGAME
        self.resolucao = None            # o que a escolha produziu (regras.resolver)
        self.tempo_da_tela = 0.0         # há quantos segundos esta tela está aí
        self._chave_da_tela = None

    # ---------------------------------------------------------- o que as telas leem
    @property
    def evento(self):
        return catalogo.EVENTOS[self.indice_do_evento]

    @property
    def dica_visivel(self):
        """Já passou o ATRASO_DA_DICA? (a dica "Pressione ENTER..." só aparece depois)"""
        return self.tempo_da_tela >= config.ATRASO_DA_DICA

    def texto_de_abertura(self):
        """O texto de abertura do evento (pode vir trocado pela ponte do anterior)."""
        return regras.texto_de_abertura(self.evento, self.estado)

    def segundos_ate_avancar(self):
        return config.AVANCO_AUTOMATICO.get(self.tela)

    # ============================================================
    # A ORDEM DAS TELAS
    # ============================================================
    def avancar_tela(self):
        """Passa para a próxima tela de apresentação. É o que o ENTER faz e
        também o que acontece sozinho quando o tempo da tela acaba (veja
        AVANCO_AUTOMATICO em config.py)."""
        if self.tela == config.ABERTURA:
            self.tela = config.CONSELHEIRA
            self.indice_conselheira = 0
        elif self.tela == config.CONSELHEIRA:
            if self.indice_conselheira < len(ORDEM) - 1:
                self.indice_conselheira += 1
            else:
                self.tela = config.NOVA_RAINHA
        elif self.tela == config.NOVA_RAINHA:
            self.iniciar_evento()
        elif self.tela == config.ESTACAO:
            self.tela = config.CONTEXTO
        elif self.tela == config.CONTEXTO:
            self.tela = config.ESCOLHA

    def iniciar_evento(self):
        """1. O EVENTO: mostra o cartão da estação (se mudou) e o texto."""
        if self.evento["estacao"] != self.estacao_atual:
            self.estacao_atual = self.evento["estacao"]
            self.tela = config.ESTACAO
        else:
            self.tela = config.CONTEXTO

    def escolher(self, opcao):
        """2. O MINIGAME: a jogadora escolheu uma opção. Com minigame, vai para
        o preparo; sem minigame (ação direta), resolve na hora."""
        self.opcao = opcao
        evento = self.evento
        classe = catalogo.JOGOS[evento["id"]][opcao["conselheira"]]
        self.classe_do_minigame = classe
        self.teve_minigame = classe is not None
        self.minigame = None
        if classe is None:
            self.concluir_escolha(1.0)
            return
        self.nome_do_minigame = classe.name
        self.instrucao_do_minigame = classe.instrucao
        self.dificuldade = (catalogo.DIFICULDADES[evento["id"]]
                            or config.DIFICULDADE_POR_ESTACAO.get(evento["estacao"], 1))
        self.tempo_de_preparo = config.TEMPO_DE_PREPARO_DO_MINIGAME
        self.tela = config.PREPARO

    def iniciar_minigame(self):
        """Acabou o preparo: cria o minigame e começa."""
        self.minigame = self.classe_do_minigame(
            layout.area_do_minigame(), difficulty=self.dificuldade, relacao=self.estado.relacao)
        self.tela = config.MINIGAME

    def concluir_escolha(self, multiplicador):
        """3. O RESULTADO: o minigame terminou (ou não havia). As REGRAS calculam
        o que mudou (regras.resolver); este método decide a próxima tela."""
        self.resolucao = regras.resolver(self.estado, self.evento, self.opcao, multiplicador)
        self.tela = config.RESULTADO_DO_MINIGAME if self.teve_minigame else config.CONSEQUENCIA

    def proximo_evento(self):
        """4. Próximo evento (ou a tela final, se acabaram)."""
        self.indice_do_evento += 1
        if self.indice_do_evento >= len(catalogo.EVENTOS):
            self.tela = config.FINAL
        else:
            self.iniciar_evento()

    # ============================================================
    # TECLADO E MOUSE
    # ============================================================
    def tratar_evento(self, evento, mouse):
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if evento.type == pygame.KEYDOWN:
            enter = evento.key == pygame.K_RETURN
            if enter and self.tela in config.TELAS_QUE_AVANCAM:
                self.avancar_tela()
            elif enter and self.tela == config.PREPARO:
                self.iniciar_minigame()
            elif self.tela == config.MINIGAME and self.minigame is not None:
                if not self.minigame.done:
                    self.minigame.handle_key(evento.key)
                elif enter:
                    self.concluir_escolha(self.minigame.effect_multiplier())
            elif enter and self.tela == config.RESULTADO_DO_MINIGAME:
                self.tela = config.CONSEQUENCIA
            elif enter and self.tela == config.CONSEQUENCIA:
                self.proximo_evento()

        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if self.tela == config.ESCOLHA:
                opcoes = self.evento["opcoes"]
                for opcao, card in zip(opcoes, layout.retangulos_dos_cards(len(opcoes))):
                    if card.collidepoint(mouse):
                        self.escolher(opcao)
                        break
            elif self.tela == config.MINIGAME and self.minigame is not None and not self.minigame.done:
                self.minigame.handle_click(mouse)

        if evento.type == pygame.MOUSEMOTION:
            if self.tela == config.MINIGAME and self.minigame is not None and not self.minigame.done:
                self.minigame.handle_drag(mouse, bool(evento.buttons[0]))

        if evento.type == pygame.MOUSEBUTTONUP and evento.button == 1:
            if self.tela == config.MINIGAME and self.minigame is not None and not self.minigame.done:
                self.minigame.handle_release(mouse)

    # ============================================================
    # O RELÓGIO DAS TELAS E O LAÇO DO JOGO
    # ============================================================
    def medir_tempo_da_tela(self, dt):
        """Conta há quanto tempo a tela atual está aí (a dica do ENTER usa isso)
        e, passado o AVANCO_AUTOMATICO dela, avança (o mesmo que o ENTER)."""
        chave = (self.tela, self.indice_conselheira)
        if chave != self._chave_da_tela:
            self._chave_da_tela = chave
            self.tempo_da_tela = 0.0
        self.tempo_da_tela += min(dt, 0.25)
        limite = config.AVANCO_AUTOMATICO.get(self.tela)
        if limite and self.tempo_da_tela >= limite:
            self.tempo_da_tela = 0.0
            self.avancar_tela()

    def rodar(self):
        while True:
            dt = self.visual.relogio.tick(config.FPS) / 1000.0
            mouse = pygame.mouse.get_pos()
            for evento in pygame.event.get():
                self.tratar_evento(evento, mouse)

            self.visual.atualizar(dt)
            self.medir_tempo_da_tela(dt)

            if self.tela == config.PREPARO:
                self.tempo_de_preparo -= dt
                if self.tempo_de_preparo <= 0:
                    self.iniciar_minigame()

            if self.tela == config.MINIGAME and self.minigame is not None:
                self.minigame.update(dt)

            desenho.desenhar(self.visual, self, mouse)


if __name__ == "__main__":
    Jogo().rodar()

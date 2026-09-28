# Bee the Queen

Mesma jogabilidade da versao anterior, agora reorganizada em arquivos e
pastas separados por responsabilidade, para ser mais facil de editar e de
navegar.

## Como rodar

```bash
pip install pygame
python main.py
```

## Mapa do projeto — onde encontrar cada coisa

```
BeeTheQueen_v2/
├── main.py                 <- ponto de entrada (so 6 linhas)
│
├── data/                   <- TODO O CONTEUDO/TEXTO do jogo
│   ├── events/
│   │   ├── e01_o_novo_jardim.py        <- Evento 1 (contexto, falas, custos)
│   │   ├── e02_enxame_errante.py       <- Evento 2
│   │   ├── ...                          ... um arquivo por evento, 12 no total
│   │   └── e12_a_grande_nevasca.py
│   ├── councilors.py        <- Flora/Melina/Nectar/Aurora: motto, cor,
│   │                            texto de introducao, penalidade de falha
│   ├── axes.py              <- nomes dos 5 eixos da Harmonia
│   └── profiles.py          <- textos de perfil final + mensagem da OS
│
├── puzzles/                 <- os 8 minigames, um arquivo por mecanica
│   ├── base.py                <- classe BasePuzzle (fallback) + helper de dificuldade
│   ├── espalhar_polen.py
│   ├── corredores_verdes.py
│   ├── organizar_favos.py
│   ├── salvar_flores.py
│   ├── danca_abelhas.py
│   ├── resgatar_operarias.py
│   ├── flores_resistentes.py
│   ├── defesa_colmeia.py
│   └── __init__.py            <- make_puzzle() + INSTRUCTIONS (texto da tela de preparo)
│
├── ui/
│   └── harmonia.py           <- desenho do radar de Harmonia e das barrinhas
│
├── game/                     <- o "motor": regras, telas e loop principal
│   ├── constants.py            <- tamanho de tela, cores, nomes dos estados
│   ├── utils.py                 <- funcoes de desenho genericas (quebrar texto, card)
│   ├── logic.py                 <- REGRAS: custos, efeitos, penalidades, trocar de tela
│   ├── screens.py                <- TELAS: cada render_xxx() desenha uma tela
│   ├── input.py                   <- teclado/mouse + loop principal (run)
│   └── core.py                    <- junta logic+screens+input na classe Game
│
└── assets/                   <- imagens (sprites da abelha, fundo)
```

## Guia rapido: "eu quero mudar..."

| Eu quero mudar... | Vou em... |
|---|---|
| O texto/falas/custo de um evento especifico | `data/events/eXX_*.py` (ache pelo numero ou nome) |
| A personalidade/motto/titulo de uma conselheira | `data/councilors.py` |
| A penalidade de falha de uma conselheira | `data/councilors.py`, dicionario `FAIL_PENALTY` |
| O texto de perfil final ou a mensagem da OS | `data/profiles.py` |
| A instrucao mostrada na tela de preparo do minigame | `puzzles/__init__.py`, dicionario `INSTRUCTIONS` |
| A jogabilidade de UM minigame especifico | `puzzles/<nome_do_minigame>.py` |
| O texto da tela de abertura ou da tela "Nova Rainha" | `game/screens.py` (`render_intro`, `render_queen_intro`) |
| A posicao/cor/tamanho de qualquer coisa na tela | `game/screens.py` |
| Quanto custa mel/operarias/relacao ter Relacao baixa, bonus de dialogo etc. | `game/logic.py` |
| O que uma tecla faz em cada tela | `game/input.py` |

**Regra geral:** conteudo (texto, numeros de balanceamento) fica em
`data/` e `puzzles/__init__.py`. Comportamento e visual ficam em `game/`.
Isso significa que pra ajustar o "jogo" (fala, custo, texto) quase nunca
precisa abrir a pasta `game/` — e pra ajustar a "engine" quase nunca
precisa abrir `data/`.

## Como main.py conecta tudo

```python
from game.core import Game

if __name__ == "__main__":
    Game().run()
```

`game/core.py` monta a classe `Game` juntando 3 "pedacos" (mixins):

```python
class Game(GameLogic, GameScreens, GameInput):
    def __init__(self):
        ...  # cria tela, fontes, estado inicial (mel=100, harmonia=50, etc.)
```

- `GameLogic` (`game/logic.py`) sabe **as regras**: aplicar custo de uma
  escolha, penalidade de falha, quando ir pra tela de resumo, etc.
- `GameScreens` (`game/screens.py`) sabe **desenhar**: cada tela do jogo
  tem um metodo `render_algumacoisa()`.
- `GameInput` (`game/input.py`) sabe **o que fazer com ENTER, setas,
  cliques** — e roda o loop principal do jogo (`run()`).

Como sao 3 pedacos da MESMA classe `Game`, qualquer metodo de um consegue
usar dados/metodos dos outros dois (ex.: `render_result()`, que esta em
`screens.py`, chama `self.imbalance_warning()`, que esta em `logic.py`)
sem precisar importar nada extra — e assim que o Python trata heranca
multipla.

## O que mudou versus a v2 "tudo num arquivo so"

Nada em termos de jogabilidade — testei um playthrough completo (Primavera
a Inverno) antes e depois da reorganizacao e os resultados numericos
batem 100%. So o codigo mudou de lugar.

## Pendencias conscientes (herdadas da v2, fora do escopo desta reorganizacao)

- As 48 variacoes especificas evento×conselheira da tabela do documento
  ainda nao foram implementadas 1 a 1 (dificuldade escala por estacao e
  Relacao, mas nao por combinacao especifica).
- Persistencia de consequencias entre estacoes/anos.
- Desbloqueio/afastamento de conselheiras por afinidade (>=70% / <=20%).
- Eventos de correcao automatica por desequilibrio de Harmonia.
- Dados reais sobre queda de polinizadores na mensagem da OS ainda
  marcados como `[NOTA: ... validar fonte]` em `data/profiles.py`.
- Repetir a estrutura para os anos 2-4.

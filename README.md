# Bee the Queen — Protótipo MVP (pygame)

Protótipo jogável do **Ano 1** de Bee the Queen (Primavera → Verão → Outono →
Inverno, 12 eventos), construído a partir de:

- `Bee_the_Queen_Roteiro_Narrativo.docx` — todos os 12 eventos, falas das
  conselheiras, custos, efeitos e consequências permanentes vieram direto
  deste documento (`events_data.py`).
- `Abelhuda_Default.ase` — sprite da abelha (32x32, 9 frames de animação),
  exportado para `assets/bee_frame_0..8.png` e usado como mascote animado.
- `Paisagem_Campo_Florido.ase` — cenário, achatado e recortado para
  `assets/bg_scene.png` (fundo de todas as telas).

## Como rodar

```bash
pip install pygame
python main.py
```

Controles: **mouse** para escolher a proposta de uma conselheira, **ESPAÇO**
para travar o puzzle de execução, **ENTER** para avançar telas de texto.

## O que o protótipo já implementa

- Fluxo completo do documento: **contexto → Conselho propõe → jogador
  escolhe → puzzle de execução → consequência permanente** (seção 1 do
  Roteiro).
- Os 12 eventos das 4 estações, com os textos e custos exatamente como
  descritos no documento (`events_data.py`).
- Painel de Harmonia da Colmeia com os 5 eixos (Biodiversidade, Produção,
  População, Cooperação, Inovação), renderizado como radar chart.
- Recursos (Mel / Operárias) com custo/gasto por escolha.
- Afinidade das 4 conselheiras: +2 para a escolhida, -1 (ou -2 em eventos de
  conflito, 0 quando a proposta é de mediação) para as demais, seguindo a
  regra da seção 4.
- Evento 12 ("A Grande Nevasca") é tratado como **evento-espelho**: seu
  efeito depende do estado acumulado do eixo correspondente (Biodiversidade,
  Inovação, Cooperação ou reserva de Mel), e não de um valor fixo — como
  pede a seção 8 do documento.
- Aviso textual quando o painel de Harmonia fica muito desequilibrado
  (referência ao "evento de correção automática" da seção 4, ainda não
  implementado como evento de fato).
- Tela final ("O Legado da Colmeia") com o radar final, recursos, afinidades
  e uma frase de legado baseada no eixo mais forte/mais fraco.

## Simplificação proposital deste MVP

O GDD descreve **8 puzzles diferentes** (Espalhar Pólen, Corredores Verdes,
Organizar os Favos, Salvar Flores, Dança das Abelhas, Resgatar Operárias,
Flores Resistentes, Defesa da Colmeia). Implementar as 8 mecânicas é
trabalho de sprint futuro. Por ora, `puzzle.py` usa **um único mini-jogo
genérico de "execução com risco"** (barra + zona alvo + ESPAÇO para travar)
que já entrega a mesma função estrutural: a execução pode ser bem-sucedida,
parcial ou falhar, alterando o efeito final da escolha. O nome do puzzle do
GDD é mostrado na tela como referência.

## Próximos passos sugeridos (Sprint 3+)

1. Substituir `puzzle.py` pelas 8 mecânicas reais (mapeamento já está em
   `events_data.py`, campo `puzzle`).
2. Persistir as consequências no mapa entre estações/anos (hoje o texto é
   mostrado mas não altera eventos futuros).
3. Implementar o desbloqueio/afastamento de conselheiras por afinidade
   (≥70% / ≤20%, seção 4).
4. Implementar os eventos de correção automática por desequilíbrio de
   Harmonia.
5. Repetir a estrutura para os anos 2–4 com variantes condicionadas ao
   histórico de decisões (seção 10).

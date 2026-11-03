# -*- coding: utf-8 -*-
"""
OS TEXTOS FIXOS DAS TELAS: tudo que está escrito nas telas e não vem dos
eventos. (O texto de cada evento está em eventos/ e resultados/; o das
conselheiras, em dados/conselheiras.py; o dos perfis finais, em dados/perfis.py.)

O que vem entre chaves, como {titulo}, é preenchido pelo jogo: não apague a
palavra entre chaves, só mude o texto em volta dela. Para quebrar linha,
use \\n.
"""

# ------------------------------------------------------------ abertura
TITULO_DO_JOGO = "BEE THE QUEEN"
SUBTITULO_DO_JOGO = "Ano 1"
ABERTURA_1 = (
    "A Rainha Anciã se aposenta e escolhe você como sucessora.\n"
    "Você governa por 4 estações, apoiada por quatro conselheiras:")
ABERTURA_CONSELHEIRAS = "Flora, Melina, Nectar e Aurora"
ABERTURA_2 = (
    "Cada escolha altera o painel de Harmonia da Colmeia, a Relação\n"
    "com a Colmeia, consome recursos e muda a afinidade das\n"
    "conselheiras. Não existe final único! existe o reino que você constrói.")
DICA_ABERTURA = "Pressione ENTER para conhecer o Conselho."

# ------------------------------------------------------ as conselheiras
DICA_CONSELHEIRA = "Pressione ENTER para a próxima conselheira"

# ---------------------------------------------------------- Nova Rainha
NOVA_RAINHA_TITULO = "A Nova Rainha"
NOVA_RAINHA_TEXTO = (
    "Você é a nova Rainha. A cada estação, o Conselho vai propor 4 caminhos. "
    "Não existe caminho perfeito! existe o caminho que você escolhe sustentar.")
DICA_NOVA_RAINHA = "Pressione ENTER para começar o reinado"

# ------------------------------------------------------------- estação
DICA_ESTACAO = "Pressione ENTER para continuar"
# como cada estação aparece escrita (a chave é o nome usado nos arquivos dos eventos)
NOMES_DAS_ESTACOES = {"Verao": "Verão"}

# --------------------------------------------------- texto e escolha
CABECALHO_DO_EVENTO = "{estacao} - Evento {id}: {titulo}"
DICA_CONTEXTO = "Pressione ENTER para reunir o Conselho"
CABECALHO_DA_ESCOLHA = "O Conselho se reúne: {titulo}"
# as moedas na linha de preço de cada card
CARD_CUSTO_MEL = "Mel {valor}"
CARD_CUSTO_MEL_TUDO = "Mel: tudo"
CARD_CUSTO_OPERARIAS = "Operárias {valor:+d}"
CARD_CUSTO_RELACAO = "Relação {valor:+d}"
CARD_SEM_CUSTO = "Sem custo direto"

# ------------------------------------------------------------ minigame
PREPARO_TITULO = "Preparando: {nome}"
PROPOSTA = "{conselheira} propôs: {acao}"
DICA_PREPARO = "Pressione ENTER para começar agora"
MINIGAME_TITULO = "Execução: {nome}"
MINIGAME_SEM_JOGO = "Ação direta"
DICA_MINIGAME = "Pressione ENTER para ver o resultado"

# o resultado do minigame ("sucesso", "parcial" ou "falha" -- como o jogo termina)
RESULTADO_TITULO = {
    "sucesso": "Execução bem-sucedida!",
    "parcial": "Execução parcial.",
    "falha": "A execução falhou.",
}
# {pct} é a porcentagem do efeito que valeu (vem do multiplicador do minigame)
RESULTADO_DETALHE = {
    "sucesso": "O efeito da escolha foi aplicado por completo ({pct}%).",
    "parcial": "Apenas metade do efeito da escolha foi aplicado ({pct}%).",
    "falha": "Só {pct}% do efeito foi aplicado, e ainda veio uma penalidade extra.",
}
RESULTADO_EFEITOS = "Efeitos nesta rodada: {linhas}"
RESULTADO_SEM_EFEITOS = "(efeito condicional)"
RESULTADO_CUSTO = "Custo desta escolha: {linhas}"
RESULTADO_PENALIDADE = "Penalidade extra de {conselheira}: {texto}"
DICA_RESULTADO_DO_MINIGAME = "Pressione ENTER para ver a consequência"

# a mesma moeda escrita nas listas de efeito/custo
NOMES_DAS_MOEDAS = {"mel": "Mel", "operarias": "Operárias", "relacao": "Relação"}

# -------------------------------------------------------- consequência
CONSEQUENCIA_TITULO = "Consequência: {titulo}"
CONSEQUENCIA_EFEITOS = "Efeitos: {linhas}"
AVISO_DE_DESEQUILIBRIO = (
    "O painel de Harmonia está muito desequilibrado -- em sprints futuros "
    "isso desencadeia eventos de correção automática (ex.: pragas por "
    "excesso de Produção sem Biodiversidade).")
DICA_CONSEQUENCIA = "Pressione ENTER para continuar"

# ---------------------------------------------------------------- HUD
HUD_MEL = "Mel: {valor}"
HUD_OPERARIAS = "Operárias: {valor}"
HUD_RELACAO = "Relação com a Colmeia: {valor}"
HUD_AVISO_DE_PRODUCAO = "Relação baixa: produção com penalidade!"
HUD_AFINIDADE = "Afinidade das Conselheiras"

# --------------------------------------------------------- tela final
FINAL_TITULO = "O Legado da Colmeia"
FINAL_RECURSOS = "Recursos finais"
FINAL_AFINIDADE = "Afinidade final"
FINAL_LINHA_DE_AFINIDADE = "{nome}: {valor} ({situacao})"
FINAL_SITUACAO = {"aliada": "aliada próxima", "afastada": "afastada", "neutra": "neutra"}
FINAL_PERFIL = "Perfil: {nome}"

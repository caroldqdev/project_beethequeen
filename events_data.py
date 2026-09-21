# -*- coding: utf-8 -*-
"""
Banco de eventos de Bee the Queen — Ano 1 (ciclo completo de 4 estações).
Fonte: Bee_the_Queen_Roteiro_Narrativo.docx (seções 5 a 8).

Cada evento tem:
  id, season, title, context
  options: lista de escolhas do Conselho, cada uma com:
      councilor   -> nome da conselheira
      action      -> texto da proposta (fala/ação)
      cost        -> dict {'mel': int, 'operarias': int} (negativo = gasto)
      effects     -> dict com deltas nos 5 eixos da Harmonia
                     ('biodiversidade','producao','populacao','cooperacao','inovacao')
      extra       -> efeitos textuais/condicionais que o roteiro descreve
                     mas que não plotamos como número puro (ex.: saúde,
                     efeitos que dependem de decisões passadas)
      affinity    -> dict {'self': +N, 'others': -N} (aplicado às 3 conselheiras não escolhidas)
      puzzle      -> nome do puzzle do GDD que representaria a execução
  consequence -> texto da consequência permanente (mostrado ao jogador;
                 em sprints futuros deve gravar uma flag persistente no mapa)

Este arquivo é a "fonte direta para popular o banco de eventos" citada na
seção 10 do roteiro (Sprint 2).
"""

EVENTS = [
    # ---------------- PRIMAVERA ----------------
    {
        "id": 1,
        "season": "Primavera",
        "title": "O Novo Jardim",
        "context": "Exploradoras encontram um jardim particular ainda nao polinizado "
                   "por ninguem -- mas outros insetos tambem o notaram.",
        "options": [
            {"councilor": "Flora", "action": "Mapear com cuidado, respeitando as especies "
             "nativas antes de polinizar",
             "cost": {"mel": -10, "operarias": 0},
             "effects": {"biodiversidade": 8, "producao": 3},
             "affinity": {"self": 2, "others": -1}, "puzzle": "Espalhar Polen"},
            {"councilor": "Melina", "action": "Polinizar tudo o quanto antes, antes que "
             "outra especie tome o jardim",
             "cost": {"mel": 0, "operarias": -5},
             "effects": {"producao": 8, "biodiversidade": -5},
             "affinity": {"self": 2, "others": -1}, "puzzle": "Espalhar Polen (tempo reduzido)"},
            {"councilor": "Nectar", "action": "Testar uma rota de voo experimental mais eficiente",
             "cost": {"mel": -15, "operarias": 0},
             "effects": {"inovacao": 8, "producao": 4},
             "affinity": {"self": 2, "others": -1}, "puzzle": "Danca das Abelhas"},
            {"councilor": "Aurora", "action": "Negociar com o jardineiro humano um plantio conjunto",
             "cost": {"mel": -2, "operarias": 0},
             "effects": {"cooperacao": 8},
             "affinity": {"self": 2, "others": -1}, "puzzle": "Corredores Verdes"},
        ],
        "consequence": "O jardim passa a existir permanentemente no mapa; a forma como foi "
                       "ocupado define se ele aparecera depois como aliado (Aurora/Flora) "
                       "ou como fonte de conflito com outros polinizadores (Melina/Nectar).",
    },
    {
        "id": 2,
        "season": "Primavera",
        "title": "Enxame Errante",
        "context": "Um enxame de abelhas selvagens sem colmeia pede abrigo. Aceita-las muda "
                   "a composicao genetica e social da colonia.",
        "options": [
            {"councilor": "Flora", "action": "Acolher e integrar respeitando a diversidade "
             "genetica do enxame",
             "cost": {"mel": -20, "operarias": 0},
             "effects": {"biodiversidade": 8, "populacao": 5},
             "affinity": {"self": 2, "others": -1}, "puzzle": "Corredores Verdes"},
            {"councilor": "Melina", "action": "Recruta-las como forca de trabalho extra imediatamente",
             "cost": {"mel": -10, "operarias": 30},
             "effects": {"producao": 8, "populacao": 6},
             "affinity": {"self": 2, "others": -1}, "puzzle": "Organizar os Favos"},
            {"councilor": "Nectar", "action": "Usar o encontro para testar uma nova tecnica "
             "de comunicacao entre colmeias",
             "cost": {"mel": -10, "operarias": 0},
             "effects": {"inovacao": 8},
             "affinity": {"self": 2, "others": -1}, "puzzle": "Danca das Abelhas"},
            {"councilor": "Aurora", "action": "Formar uma colmeia satelite aliada, sem anexacao total",
             "cost": {"mel": -5, "operarias": 0},
             "effects": {"cooperacao": 8, "populacao": 3},
             "affinity": {"self": 2, "others": -1}, "puzzle": "Corredores Verdes"},
        ],
        "consequence": "O enxame se torna uma faccao interna permanente. Dependendo da escolha, "
                       "reaparece como reforco numa crise futura (alianca) ou como fonte de "
                       "atrito por recursos (anexacao forcada).",
    },
    {
        "id": 3,
        "season": "Primavera",
        "title": "Floracao de Um So Tipo",
        "context": "Um campo proximo floresce com uma unica especie, em grande quantidade -- "
                   "tentador, mas uma monocultura empobrece o solo com o tempo.",
        "options": [
            {"councilor": "Flora", "action": "Recusar o excesso e priorizar campos diversos, "
             "mesmo rendendo menos agora",
             "cost": {"mel": -5, "operarias": 0},
             "effects": {"biodiversidade": 8, "producao": -3},
             "affinity": {"self": 2, "others": -1}, "puzzle": "Flores Resistentes"},
            {"councilor": "Melina", "action": "Explorar ao maximo enquanto a floracao dura",
             "cost": {"mel": 0, "operarias": 0},
             "effects": {"producao": 8, "biodiversidade": -6},
             "affinity": {"self": 2, "others": -1}, "puzzle": "Organizar os Favos"},
            {"councilor": "Nectar", "action": "Desenvolver uma tecnica de estocagem para "
             "aproveitar picos sazonais",
             "cost": {"mel": -15, "operarias": 0},
             "effects": {"inovacao": 8, "producao": 4},
             "affinity": {"self": 2, "others": -1}, "puzzle": "Organizar os Favos (avancado)"},
            {"councilor": "Aurora", "action": "Compartilhar a descoberta com colmeias vizinhas",
             "cost": {"mel": -5, "operarias": 0},
             "effects": {"cooperacao": 8},
             "affinity": {"self": 2, "others": -1}, "puzzle": "Corredores Verdes"},
        ],
        "consequence": "Se explorada sem cuidado, a monocultura empobrece o solo e o campo se "
                       "torna esteril nas proximas estacoes, reduzindo opcoes futuras de "
                       "forrageamento naquela regiao do mapa.",
    },

    # ---------------- VERAO ----------------
    {
        "id": 4,
        "season": "Verao",
        "title": "A Seca Chega",
        "context": "Semanas sem chuva deixam flores murchando e reservas de agua escassas.",
        "options": [
            {"councilor": "Flora", "action": "Priorizar o resgate das flores nativas mais ameacadas",
             "cost": {"mel": -15, "operarias": 0},
             "effects": {"biodiversidade": 8, "producao": -4},
             "affinity": {"self": 2, "others": -1}, "puzzle": "Salvar Flores"},
            {"councilor": "Melina", "action": "Racionar as reservas de mel para garantir a "
             "sobrevivencia da producao",
             "cost": {"mel": -30, "operarias": 0},
             "effects": {"producao": 8, "populacao": -2},
             "affinity": {"self": 2, "others": -1}, "puzzle": "Organizar os Favos"},
            {"councilor": "Nectar", "action": "Pesquisar uma rota alternativa ate fontes de "
             "agua distantes",
             "cost": {"mel": -20, "operarias": 0},
             "effects": {"inovacao": 8},
             "affinity": {"self": 2, "others": -1}, "puzzle": "Danca das Abelhas"},
            {"councilor": "Aurora", "action": "Pedir ajuda e agua a colmeias vizinhas",
             "cost": {"mel": -10, "operarias": 0},
             "effects": {"cooperacao": 8},
             "affinity": {"self": 2, "others": -1}, "puzzle": "Corredores Verdes"},
        ],
        "consequence": "Flores nao resgatadas nesta estacao nao voltam a florescer sozinhas -- "
                       "precisarao ser replantadas manualmente em uma estacao futura, com custo maior.",
    },
    {
        "id": 5,
        "season": "Verao",
        "title": "A Fazenda com Pesticidas",
        "context": "Uma fazenda vizinha comecou a usar pesticidas. O Conselho se reune com "
                   "urgencia -- cada conselheira ve o problema de um angulo diferente.",
        "options": [
            {"councilor": "Flora", "action": "Restaurar habitats alternativos, afastando a "
             "colonia da area contaminada",
             "cost": {"mel": -20, "operarias": 0},
             "effects": {"biodiversidade": 8, "producao": -4},
             "affinity": {"self": 2, "others": -1}, "puzzle": "Flores Resistentes"},
            {"councilor": "Melina", "action": "Aproveitar o campo intensamente antes da "
             "proxima pulverizacao",
             "cost": {"mel": 0, "operarias": 0},
             "effects": {"producao": 8},
             "extra": "Saude da colonia cai de forma lenta e continua nas proximas estacoes.",
             "affinity": {"self": 2, "others": -1}, "puzzle": "Organizar os Favos"},
            {"councilor": "Nectar", "action": "Desenvolver novas rotas de forrageamento que "
             "evitem a area tratada",
             "cost": {"mel": -15, "operarias": 0},
             "effects": {"inovacao": 8, "producao": 4},
             "affinity": {"self": 2, "others": -1}, "puzzle": "Danca das Abelhas"},
            {"councilor": "Aurora", "action": "Negociar diretamente com os agricultores por "
             "uma faixa livre de pesticidas",
             "cost": {"mel": -10, "operarias": 0},
             "effects": {"cooperacao": 8, "biodiversidade": 4},
             "affinity": {"self": 2, "others": -1}, "puzzle": "Corredores Verdes"},
        ],
        "consequence": "A relacao com a fazenda fica marcada: negociar (Aurora) cria uma faixa "
                       "segura permanente; ignorar (Melina) faz a Saude da colonia cair de "
                       "forma lenta e continua nas estacoes seguintes.",
    },
    {
        "id": 6,
        "season": "Verao",
        "title": "Incendio nas Redondezas",
        "context": "Fumaca no horizonte -- um incendio se aproxima da colmeia. E preciso decidir agora.",
        "options": [
            {"councilor": "Melina", "action": "Apagar o fogo agora com o que houver disponivel",
             "cost": {"mel": -5, "operarias": -50},
             "effects": {},
             "extra": "Alto risco de Populacao, mas salva o territorio.",
             "affinity": {"self": 2, "others": -1}, "puzzle": "Defesa da Colmeia"},
            {"councilor": "Aurora", "action": "Salvar as operarias do local, abandonando "
             "parte do territorio",
             "cost": {"mel": -15, "operarias": -5},
             "effects": {"producao": -6},
             "extra": "Preserva Populacao.",
             "affinity": {"self": 2, "others": -1}, "puzzle": "Resgatar Operarias"},
            {"councilor": "Nectar", "action": "Investir em colmeias a prova de fogo para o futuro",
             "cost": {"mel": -20, "operarias": -10},
             "effects": {"inovacao": 8},
             "extra": "Reduz dano de incendios futuros.",
             "affinity": {"self": 2, "others": -1}, "puzzle": "Defesa da Colmeia"},
            {"councilor": "Flora", "action": "Restaurar a area queimada depois, criando uma "
             "barreira verde natural",
             "cost": {"mel": -15, "operarias": 0},
             "effects": {"biodiversidade": 6},
             "affinity": {"self": 2, "others": -1}, "puzzle": "Flores Resistentes"},
        ],
        "consequence": "A opcao escolhida define a 'cicatriz' visual do mapa: area queimada "
                       "permanente (Melina), colmeia realocada (Aurora), infraestrutura "
                       "resistente a fogo (Nectar) ou barreira verde regenerada (Flora).",
    },

    # ---------------- OUTONO ----------------
    {
        "id": 7,
        "season": "Outono",
        "title": "Colonizar Outro Jardim",
        "context": "Um jardim vizinho, ainda livre, pode se tornar uma extensao da colonia "
                   "antes do inverno.",
        "options": [
            {"councilor": "Melina", "action": "Colonizar o jardim para garantir mais uma "
             "fonte de reservas",
             "cost": {"mel": -2, "operarias": -2},
             "effects": {"producao": 8},
             "affinity": {"self": 2, "others": -1}, "puzzle": "Espalhar Polen"},
            {"councilor": "Flora", "action": "Colonizar de forma gradual, preservando a "
             "vegetacao ja existente",
             "cost": {"mel": -8, "operarias": 0},
             "effects": {"biodiversidade": 8, "producao": 3},
             "affinity": {"self": 2, "others": -1}, "puzzle": "Corredores Verdes"},
            {"councilor": "Nectar", "action": "Usar o novo jardim como posto avancado de pesquisa",
             "cost": {"mel": -10, "operarias": 0},
             "effects": {"inovacao": 8},
             "affinity": {"self": 2, "others": -1}, "puzzle": "Danca das Abelhas"},
            {"councilor": "Aurora", "action": "Propor a colonizacao conjunta com outra colmeia amiga",
             "cost": {"mel": -5, "operarias": 0},
             "effects": {"cooperacao": 8, "producao": 4},
             "affinity": {"self": 2, "others": -1}, "puzzle": "Corredores Verdes"},
        ],
        "consequence": "O novo territorio passa a contar como fonte de recursos todo inverno "
                       "-- sua qualidade (diversa, industrial, experimental ou compartilhada) "
                       "e definida agora e nao muda mais neste ciclo.",
    },
    {
        "id": 8,
        "season": "Outono",
        "title": "Excesso de Producao",
        "context": "A colheita do ano rendeu mais mel do que a estrutura atual comporta -- "
                   "sem espaco, parte dele sera perdido.",
        "options": [
            {"councilor": "Melina", "action": "Expandir os favos as pressas para nao perder nada",
             "cost": {"mel": -25, "operarias": 0},
             "effects": {"producao": 8},
             "affinity": {"self": 2, "others": -1}, "puzzle": "Organizar os Favos"},
            {"councilor": "Nectar", "action": "Testar um novo formato hexagonal mais "
             "eficiente de armazenamento",
             "cost": {"mel": -15, "operarias": 0},
             "effects": {"inovacao": 8, "producao": 6},
             "affinity": {"self": 2, "others": -1}, "puzzle": "Organizar os Favos (avancado)"},
            {"councilor": "Flora", "action": "Doar o excedente para polinizar areas que "
             "precisam de recuperacao",
             "cost": {"mel": 0, "operarias": 0},
             "effects": {"biodiversidade": 8, "producao": -4},
             "affinity": {"self": 2, "others": -1}, "puzzle": "Espalhar Polen"},
            {"councilor": "Aurora", "action": "Repartir o excedente com colonias vizinhas em dificuldade",
             "cost": {"mel": 0, "operarias": 0},
             "effects": {"cooperacao": 8, "producao": -4},
             "affinity": {"self": 2, "others": -1}, "puzzle": "Corredores Verdes"},
        ],
        "consequence": "A capacidade de estoque construida aqui (Melina/Nectar) reduz o risco "
                       "de fome no Inverno; doar (Flora/Aurora) reduz o estoque mas garante "
                       "aliados ou territorio recuperado.",
    },
    {
        "id": 9,
        "season": "Outono",
        "title": "O Conselho Divide Opinioes",
        "context": "Pela primeira vez, duas conselheiras discordam abertamente na frente da "
                   "colonia sobre qual prioridade definira o preparo para o inverno.",
        "options": [
            {"councilor": "Flora", "action": "Dar prioridade total a recuperacao do "
             "ecossistema antes do frio",
             "cost": {"mel": -15, "operarias": 0},
             "effects": {"biodiversidade": 8},
             "affinity": {"self": 2, "others": -2}, "puzzle": "Danca das Abelhas"},
            {"councilor": "Melina", "action": "Dar prioridade total ao acumulo de reservas",
             "cost": {"mel": -10, "operarias": 0},
             "effects": {"producao": 8},
             "affinity": {"self": 2, "others": -2}, "puzzle": "Organizar os Favos"},
            {"councilor": "Nectar", "action": "Propor uma solucao tecnica que tente "
             "equilibrar as duas demandas",
             "cost": {"mel": -20, "operarias": 0},
             "effects": {"inovacao": 8, "biodiversidade": 2, "producao": 2},
             "affinity": {"self": 2, "others": -1}, "puzzle": "Danca das Abelhas"},
            {"councilor": "Aurora", "action": "Mediar o debate publicamente e buscar "
             "consenso entre as conselheiras",
             "cost": {"mel": -5, "operarias": 0},
             "effects": {"cooperacao": 8},
             "affinity": {"self": 2, "others": 0}, "puzzle": "Corredores Verdes"},
        ],
        "consequence": "Este e o primeiro evento em que a afinidade das conselheiras nao "
                       "escolhidas pode cair alem do padrao -- se alguma afinidade ja "
                       "estiver baixa, ela passa a discordar abertamente em eventos "
                       "futuros, reduzindo bonus.",
    },

    # ---------------- INVERNO ----------------
    {
        "id": 10,
        "season": "Inverno",
        "title": "O Frio Chega",
        "context": "As primeiras geadas testam tudo o que foi construido no Outono. As "
                   "reservas acumuladas -- ou a falta delas -- decidem o tom do inverno.",
        "options": [
            {"councilor": "Melina", "action": "Consumir as reservas de forma controlada, "
             "priorizando a producao minima",
             "cost": {"mel": -40, "operarias": 0},
             "effects": {"producao": 6},
             "affinity": {"self": 2, "others": -1}, "puzzle": "Organizar os Favos"},
            {"councilor": "Flora", "action": "Manter parte da colonia ativa cuidando de "
             "plantas resistentes ao frio",
             "cost": {"mel": -10, "operarias": 0},
             "effects": {"biodiversidade": 6},
             "affinity": {"self": 2, "others": -1}, "puzzle": "Flores Resistentes"},
            {"councilor": "Nectar", "action": "Testar um metodo de aquecimento coletivo mais eficiente",
             "cost": {"mel": -15, "operarias": 0},
             "effects": {"inovacao": 6},
             "extra": "Reduz perdas por frio no futuro.",
             "affinity": {"self": 2, "others": -1}, "puzzle": "Danca das Abelhas"},
            {"councilor": "Aurora", "action": "Formar um circulo de aquecimento com todas "
             "as operarias disponiveis",
             "cost": {"mel": -5, "operarias": 0},
             "effects": {"cooperacao": 6, "populacao": 3},
             "affinity": {"self": 2, "others": -1}, "puzzle": "Corredores Verdes"},
        ],
        "consequence": "O saldo de Mel acumulado nos eventos 7 e 8 e o que realmente e "
                       "gasto aqui -- colonias com pouca reserva sofrem perda automatica "
                       "de Populacao, tornando visivel o resultado das decisoes do Outono.",
    },
    {
        "id": 11,
        "season": "Inverno",
        "title": "Teias na Entrada",
        "context": "Uma aranha construiu teias perto da entrada da colmeia. Operarias "
                   "forrageadoras estao presas.",
        "options": [
            {"councilor": "Aurora", "action": "Organizar um resgate coletivo, evitando as teias",
             "cost": {"mel": -10, "operarias": 0},
             "effects": {"cooperacao": 6},
             "extra": "Salva a maioria das operarias.",
             "affinity": {"self": 2, "others": -1}, "puzzle": "Resgatar Operarias"},
            {"councilor": "Melina", "action": "Sacrificar as presas e seguir em frente para "
             "nao perder mais recursos",
             "cost": {"mel": 0, "operarias": -10},
             "effects": {"producao": 5, "populacao": -4},
             "affinity": {"self": 2, "others": -1}, "puzzle": None},
            {"councilor": "Nectar", "action": "Testar uma rota alternativa de entrada que "
             "evite a area da teia",
             "cost": {"mel": -15, "operarias": 0},
             "effects": {"inovacao": 6},
             "affinity": {"self": 2, "others": -1}, "puzzle": "Danca das Abelhas"},
            {"councilor": "Flora", "action": "Deixar a aranha em paz e replantar arbustos "
             "que naturalmente a afastem",
             "cost": {"mel": -10, "operarias": 0},
             "effects": {"biodiversidade": 6},
             "affinity": {"self": 2, "others": -1}, "puzzle": "Flores Resistentes"},
        ],
        "consequence": "A entrada da colmeia e redesenhada visualmente conforme a escolha: "
                       "rota de resgate marcada, nova entrada tecnica ou cinturao de "
                       "arbustos -- cada uma altera o risco de eventos de predador em "
                       "invernos futuros.",
    },
    {
        "id": 12,
        "season": "Inverno",
        "title": "A Grande Nevasca",
        "context": "O evento culminante do ano: uma nevasca severa ameaca tudo o que foi "
                   "construido. A resposta da colonia reflete diretamente o equilibrio "
                   "(ou desequilibrio) acumulado no painel de Harmonia.",
        "mirror_event": True,  # efeito depende do estado acumulado de Harmonia
        "options": [
            {"councilor": "Melina", "action": "Fechar a colmeia e sobreviver apenas com o "
             "que foi guardado",
             "cost": {"mel": "all", "operarias": 0},
             "mirror_axis": "mel_reserve",
             "affinity": {"self": 2, "others": -1}, "puzzle": "Defesa da Colmeia"},
            {"councilor": "Flora", "action": "Confiar nos corredores ecologicos criados ao "
             "longo do ano para abrigo extra",
             "cost": {"mel": 0, "operarias": 0},
             "mirror_axis": "biodiversidade",
             "affinity": {"self": 2, "others": -1}, "puzzle": "Corredores Verdes"},
            {"councilor": "Nectar", "action": "Ativar as inovacoes desenvolvidas ao longo do ano",
             "cost": {"mel": 0, "operarias": 0},
             "mirror_axis": "inovacao",
             "affinity": {"self": 2, "others": -1}, "puzzle": "Danca das Abelhas"},
            {"councilor": "Aurora", "action": "Pedir abrigo as colonias aliadas formadas "
             "durante o ano",
             "cost": {"mel": 0, "operarias": 0},
             "mirror_axis": "cooperacao",
             "affinity": {"self": 2, "others": -1}, "puzzle": "Resgatar Operarias"},
        ],
        "consequence": "Este e o evento-espelho do ano: cada opcao so funciona bem se o "
                       "jogador investiu naquele eixo ao longo das estacoes anteriores. "
                       "E aqui que a 'Harmonia da Colmeia' deixa de ser um numero e vira "
                       "sobrevivencia real -- reforcando a mensagem central de que nao "
                       "existe atalho para o equilibrio.",
    },
]

COUNCILORS = {
    "Flora":  {"emoji": "\U0001F33C", "motto": "As flores alimentam o futuro.",
               "color": (110, 179, 92)},
    "Melina": {"emoji": "\U0001F36F", "motto": "O inverno sempre chega.",
               "color": (214, 158, 46)},
    "Nectar": {"emoji": "\U0001F680", "motto": "Quem evolui primeiro sobrevive.",
               "color": (86, 130, 214)},
    "Aurora": {"emoji": "\U0001F91D", "motto": "Nenhuma colmeia floresce sozinha.",
               "color": (196, 108, 196)},
}

HARMONIA_AXES = ["biodiversidade", "producao", "populacao", "cooperacao", "inovacao"]
HARMONIA_LABELS = {
    "biodiversidade": "Biodiversidade",
    "producao": "Producao",
    "populacao": "Populacao",
    "cooperacao": "Cooperacao",
    "inovacao": "Inovacao",
}

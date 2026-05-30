# ============================================================================
# NOUTRORA RPG — CONFIGURAÇÕES CENTRALIZADAS
# ============================================================================
# Todos os valores do jogo vêm daqui. Balancear = mudar aqui.

# --------------------------------------------------------------------------
# JOGADOR
# --------------------------------------------------------------------------
PLAYER_INICIAL = {
    "vida": 100,
    "forca": 10,
    "velocidade": 5,
}

NOME_MINIMO = 3

# --------------------------------------------------------------------------
# GOBLINS
# --------------------------------------------------------------------------
GOBLINS_STATS = {
    1:  {"vida": 30,  "forca": 5,  "velocidade": 2},
    2:  {"vida": 40,  "forca": 7,  "velocidade": 3},
    3:  {"vida": 50,  "forca": 10, "velocidade": 4},
    4:  {"vida": 60,  "forca": 15, "velocidade": 5},
    5:  {"vida": 70,  "forca": 18, "velocidade": 5},
    6:  {"vida": 80,  "forca": 22, "velocidade": 6},
    7:  {"vida": 90,  "forca": 26, "velocidade": 6},
    8:  {"vida": 100, "forca": 30, "velocidade": 7},
    9:  {"vida": 110, "forca": 35, "velocidade": 7},
    10: {"vida": 120, "forca": 40, "velocidade": 8},
}

GOBLINS_MUTANTES_STATS = {
    1:  {"vida": 50,  "forca": 10, "velocidade": 3},
    2:  {"vida": 70,  "forca": 15, "velocidade": 4},
    3:  {"vida": 90,  "forca": 20, "velocidade": 5},
    4:  {"vida": 110, "forca": 25, "velocidade": 6},
    5:  {"vida": 130, "forca": 30, "velocidade": 7},
    6:  {"vida": 150, "forca": 35, "velocidade": 8},
    7:  {"vida": 170, "forca": 40, "velocidade": 9},
    8:  {"vida": 190, "forca": 45, "velocidade": 10},
    9:  {"vida": 210, "forca": 50, "velocidade": 11},
    10: {"vida": 230, "forca": 55, "velocidade": 12},
}

VARIACAO_DANO = 5

# --------------------------------------------------------------------------
# CENÁRIOS (pool procedural — ordem muda a cada run)
# --------------------------------------------------------------------------
CENARIOS = {
    1:  "um corredor barulhento",
    2:  "uma sala coberta por corpos antigos",
    3:  "um corredor inundado até seus joelhos",
    4:  "uma biblioteca abandonada",
    5:  "uma capela destruída iluminada por velas vermelhas",
    6:  "um túnel estreito com sons de correntes",
    7:  "uma sala silenciosa demais",
    8:  "um corredor cheio de símbolos estranhos",
    9:  "uma ponte quebrada sobre um abismo",
    10: "uma sala completamente escura",
}

TIPOS_INIMIGOS = {
    1: "1 goblin",
    2: "2 goblins",
    3: "3 goblins",
    4: "um goblin de armadura",
}

# --------------------------------------------------------------------------
# SISTEMA DE MEMÓRIA — GDD: "NPCs lembram escolhas, ajuda, traições"
# --------------------------------------------------------------------------
# Chaves de memória armazenadas no save
MEMORIA_KEYS = [
    "ajudou_mercador",       # Ajudou o Mercador Sombrio
    "traiu_goblin_rei",      # Traiu o Rei Goblin após acordo
    "salvou_elfo",           # Salvou o Elfo Ferido
    "destruiu_caverna",      # Destruiu a Caverna dos Anciões
    "pacto_demonio",         # Fez pacto com entidade demoníaca
    "mortes_totais",         # Contador de mortes (runs anteriores)
    "runs_completadas",      # Quantas runs foram concluídas
    "runs_iniciadas",        # Total de runs iniciadas
    "maior_sala_alcancada",  # Recorde de profundidade
    "faccao_escolhida",      # Última facção escolhida
    "inimigos_derrotados",   # Total histórico de inimigos derrotados
]

# --------------------------------------------------------------------------
# FACÇÕES — GDD: "relações, facções"
# --------------------------------------------------------------------------
FACCOES = {
    "Guilda dos Perdidos":   "Aventureiros renegados que sobreviveram a Noutrora.",
    "Culto do Abismo":       "Seguidores das entidades que habitam as profundezas.",
    "Ordem dos Mercadores":  "Comerciantes que lucram com a tragédia da masmorra.",
    "Sem Facção":            "Você caminha sozinho. Ninguém confia em você — nem você neles.",
}

# --------------------------------------------------------------------------
# DISTRIBUIÇÃO DE SALAS — GDD: "estrutura procedural"
# --------------------------------------------------------------------------
CHANCE_SALA_COMBATE  = 60   # %
CHANCE_SALA_TESOURO  = 80   # % cumulativo (20% tesouro)
CHANCE_SALA_CURA     = 92   # % cumulativo (12% cura)
# restante = 8% venda (rara)

# --------------------------------------------------------------------------
# XP E PROGRESSÃO
# --------------------------------------------------------------------------
XP_POR_VITORIA        = 50
XP_POR_SALA_EXPLORADA = 10
XP_LEVEL_BASE         = 100   # XP para nível 2
XP_MULTIPLICADOR      = 1.5   # Cada nível exige 1.5x mais

# --------------------------------------------------------------------------
# ECONOMIA
# --------------------------------------------------------------------------
DINHEIRO_INICIAL = 500
RECOMPENSA_VITORIA_MIN = 10
RECOMPENSA_VITORIA_MAX = 40

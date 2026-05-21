# ============================================================================
# CONFIGURAÇÕES CENTRALIZADAS DO JOGO
# ============================================================================
# Princípio: Todos os valores "mágicos" vêm daqui. Fácil balancear o jogo
# sem procurar em 5 arquivos diferentes.

# Atributos iniciais do jogador
PLAYER_INICIAL = {
    "vida": 100,
    "forca": 10,
    "velocidade": 5,
}

# Definição de goblins por nível de dificuldade
GOBLINS_STATS = {
    1: {"vida": 30, "forca": 5, "velocidade": 2},
    2: {"vida": 40, "forca": 7, "velocidade": 3},
    3: {"vida": 50, "forca": 10, "velocidade": 4},
    4: {"vida": 60, "forca": 15, "velocidade": 5},
    5: {"vida": 70, "forca": 18, "velocidade": 5},
    6: {"vida": 80, "forca": 22, "velocidade": 6},
    7: {"vida": 90, "forca": 26, "velocidade": 6},
    8: {"vida": 100, "forca": 30, "velocidade": 7},
    9: {"vida": 110, "forca": 35, "velocidade": 7},
    10: {"vida": 120, "forca": 40, "velocidade": 8},
}

# Goblins mutantes (inimigos mais poderosos)
GOBLINS_MUTANTES_STATS = {
    1: {"vida": 50, "forca": 10, "velocidade": 3},
    2: {"vida": 70, "forca": 15, "velocidade": 4},
    3: {"vida": 90, "forca": 20, "velocidade": 5},
    4: {"vida": 110, "forca": 25, "velocidade": 6},
    5: {"vida": 130, "forca": 30, "velocidade": 7},
    6: {"vida": 150, "forca": 35, "velocidade": 8},
    7: {"vida": 170, "forca": 40, "velocidade": 9},
    8: {"vida": 190, "forca": 45, "velocidade": 10},
    9: {"vida": 210, "forca": 50, "velocidade": 11},
    10: {"vida": 230, "forca": 55, "velocidade": 12},
}

# Cálculo de dano: forca + aleatório de 0 a VARIACAO_DANO
VARIACAO_DANO = 5

# Mínimo de caracteres no nome do jogador
NOME_MINIMO = 3

# Cenários da masmorra
CENARIOS = {
    1: "um corredor barulhento",
    2: "uma sala coberta por corpos antigos",
    3: "um corredor inundado até seus joelhos",
    4: "uma biblioteca abandonada",
    5: "uma capela destruída iluminada por velas vermelhas",
    6: "um túnel estreito com sons de correntes",
    7: "uma sala silenciosa demais",
    8: "um corredor cheio de símbolos estranhos",
    9: "uma ponte quebrada sobre um abismo",
    10: "uma sala completamente escura",
}

# Tipos de inimigos possíveis
TIPOS_INIMIGOS = {
    1: "1 goblin",
    2: "2 goblins",
    3: "3 goblins",
    4: "um goblin de armadura",
}

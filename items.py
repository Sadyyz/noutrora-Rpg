# ============================================================================
# NOUTRORA RPG — SISTEMA DE ITENS
# ============================================================================

import random


class Item:
    def __init__(self, nome, descricao, raridade, efeito_tipo, valor_efeito):
        self.nome         = nome
        self.descricao    = descricao
        self.raridade     = raridade
        self.efeito_tipo  = efeito_tipo
        self.valor_efeito = valor_efeito

    _icones = {"comum": "o", "raro": "*", "epico": "#", "lendario": "@"}

    def __repr__(self):
        icone = self._icones.get(self.raridade, "-")
        return f"[{icone}] {self.nome} ({self.raridade})"

    def aplicar_efeito(self, jogador):
        if self.efeito_tipo == "cura":
            cura = jogador.curar(self.valor_efeito)
            return f"Você foi curado em {cura} pontos de vida."
        elif self.efeito_tipo == "forca":
            jogador.forca += self.valor_efeito
            return f"Sua força aumentou em {self.valor_efeito}."
        elif self.efeito_tipo == "velocidade":
            jogador.velocidade += self.valor_efeito
            return f"Sua velocidade aumentou em {self.valor_efeito}."
        return "Item usado."


# --------------------------------------------------------------------------
# CATÁLOGO
# --------------------------------------------------------------------------

ITENS_COMUNS = [
    Item("Pao",             "Cura básica",       "comum",    "cura",       20),
    Item("Maca",            "Uma maçã fresca",   "comum",    "cura",       15),
    Item("Erva Medicinal",  "Cura simples",      "comum",    "cura",       25),
]

ITENS_RAROS = [
    Item("Elixir",          "Cura potente",      "raro",     "cura",       50),
    Item("Pedra de Poder",  "Aumenta força",     "raro",     "forca",       3),
    Item("Bota Encantada",  "Aumenta velocidade","raro",     "velocidade",  2),
]

ITENS_EPICOS = [
    Item("Pocao Divina",    "Cura completa",     "epico",    "cura",      100),
    Item("Runa de Fogo",    "Força massiva",     "epico",    "forca",       6),
    Item("Vento Veloz",     "Velocidade extrema","epico",    "velocidade",  4),
]

ITENS_LENDARIOS = [
    Item("Elixir Eterno",   "Cura suprema",      "lendario", "cura",      150),
    Item("Espada Lendaria", "Força lendária",    "lendario", "forca",      10),
    Item("Asas de Hermes",  "Velocidade divina", "lendario", "velocidade",  6),
]

TODOS_ITENS = {
    "comum":    ITENS_COMUNS,
    "raro":     ITENS_RAROS,
    "epico":    ITENS_EPICOS,
    "lendario": ITENS_LENDARIOS,
}


def gerar_loot_aleatorio():
    p = random.randint(1, 100)
    if p <= 60:
        return random.choice(ITENS_COMUNS)
    elif p <= 85:
        return random.choice(ITENS_RAROS)
    elif p <= 98:
        return random.choice(ITENS_EPICOS)
    else:
        return random.choice(ITENS_LENDARIOS)


def gerar_multiplos_itens(quantidade=3):
    return [gerar_loot_aleatorio() for _ in range(quantidade)]

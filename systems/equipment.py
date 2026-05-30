# ============================================================================
# NOUTRORA RPG — SISTEMA DE EQUIPAMENTOS
# ============================================================================

import random


class Equipamento:
    def __init__(self, nome, tipo, descricao, bonus_forca=0, bonus_velocidade=0,
                 preco=0, raridade="comum"):
        self.nome             = nome
        self.tipo             = tipo
        self.descricao        = descricao
        self.bonus_forca      = bonus_forca
        self.bonus_velocidade = bonus_velocidade
        self.preco            = preco
        self.raridade         = raridade
        self.nivel_upgrade    = 1

    def fazer_upgrade(self):
        if self.nivel_upgrade < 10:
            self.nivel_upgrade    += 1
            self.bonus_forca      += 1
            self.bonus_velocidade += 1
            return True
        return False

    def obter_bonus_total(self):
        return {
            "forca":      self.bonus_forca      + (self.nivel_upgrade - 1) // 2,
            "velocidade": self.bonus_velocidade + (self.nivel_upgrade - 1) // 3,
        }

    def __repr__(self):
        nivel = f" +{self.nivel_upgrade}" if self.nivel_upgrade > 1 else ""
        return f"[{self.raridade[0].upper()}] {self.nome}{nivel} ({self.tipo})"

    def obter_status(self):
        b = self.obter_bonus_total()
        return {
            "nome":             self.nome,
            "tipo":             self.tipo,
            "raridade":         self.raridade,
            "nivel":            self.nivel_upgrade,
            "bonus_forca":      b["forca"],
            "bonus_velocidade": b["velocidade"],
            "preco":            self.preco,
        }


# --------------------------------------------------------------------------
# CATÁLOGO
# --------------------------------------------------------------------------

ARMAS_COMUNS    = [Equipamento("Espada Ferrugenta", "arma",     "Espada antiga",       bonus_forca=2,  preco=50,   raridade="comum")]
ARMAS_RARAS     = [Equipamento("Espada de Ferro",   "arma",     "Boa espada de ferro", bonus_forca=4,  preco=150,  raridade="raro")]
ARMAS_EPICAS    = [Equipamento("Espada Flamejante", "arma",     "Chamas na lamina",    bonus_forca=8,  bonus_velocidade=2, preco=400, raridade="epico")]
ARMAS_LENDARIAS = [Equipamento("Excalibur",         "arma",     "A espada suprema",    bonus_forca=12, bonus_velocidade=3, preco=1000, raridade="lendario")]

ARMADURAS_COMUNS    = [Equipamento("Armadura de Couro", "armadura", "Proteção básica",  bonus_velocidade=-1, preco=60,   raridade="comum")]
ARMADURAS_RARAS     = [Equipamento("Armadura de Ferro", "armadura", "Proteção sólida",  bonus_forca=1, bonus_velocidade=-2, preco=200, raridade="raro")]
ARMADURAS_EPICAS    = [Equipamento("Armadura de Mithril","armadura","Metal mágico leve",bonus_forca=3, bonus_velocidade=1,  preco=500, raridade="epico")]
ARMADURAS_LENDARIAS = [Equipamento("Armadura Celestial","armadura","Proteção divina",   bonus_forca=5, bonus_velocidade=2,  preco=1500,raridade="lendario")]

CATALOGO = {
    "arma":     {"comum": ARMAS_COMUNS,     "raro": ARMAS_RARAS,     "epico": ARMAS_EPICAS,     "lendario": ARMAS_LENDARIAS},
    "armadura": {"comum": ARMADURAS_COMUNS, "raro": ARMADURAS_RARAS, "epico": ARMADURAS_EPICAS, "lendario": ARMADURAS_LENDARIAS},
}


def obter_equipamento_aleatorio():
    p = random.randint(1, 100)
    if p <= 60:    raridade = "comum"
    elif p <= 85:  raridade = "raro"
    elif p <= 98:  raridade = "epico"
    else:          raridade = "lendario"
    tipo = random.choice(["arma", "armadura"])
    return random.choice(CATALOGO[tipo][raridade])


def obter_equipamentos_venda(quantidade=4):
    return [obter_equipamento_aleatorio() for _ in range(quantidade)]

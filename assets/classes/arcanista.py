# ============================================================================
# NOUTRORA RPG — CLASSE: ARCANISTA
# ============================================================================
# Estudioso das runas proibidas de Noutrora. Alto dano mágico, frágil.
# Depende de mana para tudo — fica fraco sem ela. Altíssimo teto de dano.
#
# STATS BASE: Força +2 | Vida -15 | Velocidade -1 | Mana 80
# IDENTIDADE: Caster de alto dano. Explosivo mas precisa gerenciar mana.
# ============================================================================

import random
from player import Player
from assets.classes.base_classe import BaseClasse, Habilidade


class Arcanista(Player, BaseClasse):

    DESCRICAO = (
        "Estudioso das runas proibidas que cobrem as paredes de Noutrora.\n"
        "  Dano massivo de mana. Fragil. Sem mana, e indefeso.\n"
        "  Forca +2 | Vida -15 | Velocidade -1 | Mana 80"
    )

    def __init__(self, nome):
        Player.__init__(self, nome)
        self._init_habilidades(mana_max=80)

        self.forca       += 2
        self.vida_maxima -= 15
        self.vida        -= 15
        self.velocidade  -= 1

        self._cargas_runa = 0    # Acumuladas por certas habilidades

        self.habilidades = [
            Habilidade(
                "Rajada Arcana",
                "Projétil de mana pura. Dano magico escalado por mana atual.",
                custo=12,
                fn_executar=_rajada_arcana,
            ),
            Habilidade(
                "Runa de Fraqueza",
                "Reduz a forca do inimigo em 30% por 3 turnos.",
                custo=10,
                fn_executar=_runa_fraqueza,
            ),
            Habilidade(
                "Convergencia",
                "Absorve energia do ambiente. Recupera 25 mana.",
                custo=0,
                fn_executar=_convergencia,
            ),
            Habilidade(
                "Tempestade de Runas",
                "3 explosoes sequenciais. Custo alto, dano devastador.",
                custo=30,
                fn_executar=_tempestade_runas,
            ),
            Habilidade(
                "Escudo Arcano",
                "Barreira magica. Absorve os proximos 2 ataques.",
                custo=15,
                fn_executar=_escudo_arcano,
            ),
        ]

    def turno_passivo(self):
        msgs = super().turno_passivo()
        # Arcanista regenera mana gradualmente
        self.recuperar_mana(4)
        return msgs


# ============================================================================
# HABILIDADES
# ============================================================================

def _rajada_arcana(usuario, alvo):
    # Dano escala com mana atual (mais mana = mais dano)
    escala = 1.0 + (usuario.mana / usuario.mana_maxima) * 0.8
    dano   = int(usuario.obter_forca_total() * escala) + random.randint(5, 15)
    alvo.tomar_dano(dano)
    return (
        f"  Uma rajada de energia arcana pura!\n"
        f"  Escala de mana: {escala:.1f}x\n"
        f"  Dano magico: {dano}"
    )


def _runa_fraqueza(usuario, alvo):
    reducao = int(alvo.forca * 0.3)
    alvo.forca = max(1, alvo.forca - reducao)
    alvo.aplicar_efeito("Runa de Fraqueza", {
        "tipo":   "dano",
        "valor":  0,
        "turnos": 3,
    })
    # Guarda para restaurar depois — simplificado: só reduz permanentemente neste combate
    return (
        f"  Uma runa brilha na testa do {alvo.obter_status()['tipo'].lower()}!\n"
        f"  Forca reduzida em {reducao}. ({alvo.forca} restante)\n"
        f"  Efeito dura 3 turnos."
    )


def _convergencia(usuario, alvo):
    recuperou = 25
    usuario.recuperar_mana(recuperou)
    return (
        f"  Voce fecha os olhos. Runas ao seu redor pulsam.\n"
        f"  +{recuperou} mana recuperada.\n"
        f"  Mana atual: {usuario.mana}/{usuario.mana_maxima}"
    )


def _tempestade_runas(usuario, alvo):
    total = 0
    danos = []
    for i in range(3):
        d = int(usuario.obter_forca_total() * 1.2) + random.randint(8, 20)
        alvo.tomar_dano(d)
        danos.append(d)
        total += d
    return (
        f"  TEMPESTADE DE RUNAS!\n"
        f"  Explosao 1: {danos[0]} | Explosao 2: {danos[1]} | Explosao 3: {danos[2]}\n"
        f"  TOTAL: {total} de dano devastador!"
    )


def _escudo_arcano(usuario, alvo):
    usuario._escudo_cargas = 2
    return (
        "  Um escudo de energia runica envolve seu corpo!\n"
        "  Os proximos 2 ataques serao completamente absorvidos."
    )

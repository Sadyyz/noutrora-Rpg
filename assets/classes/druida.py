# ============================================================================
# NOUTRORA RPG — CLASSE: DRUIDA
# ============================================================================
# Guardiões do equilíbrio natural. Manipulam venenos, toxinas e cura.
# Fraco no dano direto, mas enfraquece e sangra inimigos ao longo do tempo.
#
# STATS BASE: Velocidade +2 | Força -2 | Mana 60
# IDENTIDADE: DoT (dano por turno), debuffs, sustain de cura.
# ============================================================================

import random
import time
from player import Player
from assets.classes.base_classe import BaseClasse, Habilidade


class Druida(Player, BaseClasse):

    DESCRICAO = (
        "Guardioes do equilibrio natural.\n"
        "  Envenenam, sangram e curam. Fraco no golpe direto, letal com o tempo.\n"
        "  Velocidade +2 | Forca -2 | Mana 60"
    )

    def __init__(self, nome):
        Player.__init__(self, nome)
        self._init_habilidades(mana_max=60)

        # Bônus de classe
        self.velocidade += 2
        self.forca      -= 2

        # Recurso exclusivo
        self.cargas_veneno = 3

        self.habilidades = [
            Habilidade(
                "Esporos Toxicos",
                "Aplica veneno: 8 dano por turno por 4 turnos.",
                custo=10,
                fn_executar=_esporos_toxicos,
            ),
            Habilidade(
                "Sarjeta da Floresta",
                "Causa dano + aplica Sangramento por 3 turnos.",
                custo=12,
                fn_executar=_sarjeta,
            ),
            Habilidade(
                "Cura da Terra",
                "Cura 40 HP imediato + regenera 8 HP por 3 turnos.",
                custo=15,
                fn_executar=_cura_terra,
            ),
            Habilidade(
                "Raiz Paralisante",
                "Prende o inimigo. Atordoa por 2 turnos.",
                custo=18,
                fn_executar=_raiz,
            ),
            Habilidade(
                "Explosao de Fungos",
                "Dano em area (narrativo). Alto dano unico. Sem efeito de turno.",
                custo=20,
                fn_executar=_explosao_fungos,
            ),
        ]

    def regenerar_veneno(self):
        self.cargas_veneno = min(self.cargas_veneno + 1, 5)

    def turno_passivo(self):
        msgs = super().turno_passivo()
        self.recuperar_mana(3)   # Druida regenera mana passivamente
        return msgs


# ============================================================================
# FUNÇÕES DAS HABILIDADES
# ============================================================================

def _esporos_toxicos(usuario, alvo):
    alvo.aplicar_efeito("Veneno Druida", {
        "tipo":   "dano",
        "valor":  8,
        "turnos": 4,
    })
    dano_imediato = int(usuario.obter_forca_total() * 0.5) + random.randint(2, 8)
    alvo.tomar_dano(dano_imediato)
    return (
        f"  Esporos verdes envolvem o {alvo.obter_status()['tipo'].lower()}!\n"
        f"  Dano imediato: {dano_imediato}\n"
        f"  Veneno aplicado: 8 dano/turno por 4 turnos."
    )


def _sarjeta(usuario, alvo):
    dano = int(usuario.obter_forca_total() * 0.8) + random.randint(3, 10)
    alvo.tomar_dano(dano)
    alvo.aplicar_efeito("Sangramento", {
        "tipo":   "dano",
        "valor":  5,
        "turnos": 3,
    })
    return (
        f"  Garras cobertas de toxina rasgam carne!\n"
        f"  Dano: {dano}\n"
        f"  Sangramento: 5 dano/turno por 3 turnos."
    )


def _cura_terra(usuario, alvo):
    cura = usuario.curar(40)
    usuario.aplicar_efeito("Regen Terra", {
        "tipo":   "cura",
        "valor":  8,
        "turnos": 3,
    })
    return (
        f"  Raizes de luz emergem do chao e te envolvem.\n"
        f"  Cura imediata: +{cura} HP\n"
        f"  Regeneracao: +8 HP/turno por 3 turnos."
    )


def _raiz(usuario, alvo):
    alvo._atordoado       = True
    alvo._turnos_atordoado = 2
    dano = int(usuario.obter_forca_total() * 0.4) + random.randint(0, 5)
    alvo.tomar_dano(dano)
    return (
        f"  Raizes negras brotam do chao e prendem o {alvo.obter_status()['tipo'].lower()}!\n"
        f"  Dano: {dano}\n"
        f"  Atordoado por 2 turnos — nao pode atacar!"
    )


def _explosao_fungos(usuario, alvo):
    dano = int(usuario.obter_forca_total() * 2.0) + random.randint(10, 25)
    alvo.tomar_dano(dano)
    return (
        f"  Uma explosao de esporos luminescentes devasta tudo a frente!\n"
        f"  DANO MASSIVO: {dano}!"
    )

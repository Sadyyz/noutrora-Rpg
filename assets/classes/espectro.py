# ============================================================================
# NOUTRORA RPG — CLASSE: ESPECTRO
# ============================================================================
# Alma entre dois mundos. Manipula sombras, esquiva e ataca de forma invisível.
# Alta velocidade, baixa vida. Joga com evasão e burst damage.
#
# STATS BASE: Velocidade +4 | Vida -20 | Força +1 | Mana 50
# IDENTIDADE: Assassino. Alta esquiva, golpes críticos, fuga garantida.
# ============================================================================

import random
from player import Player
from assets.classes.base_classe import BaseClasse, Habilidade


class Espectro(Player, BaseClasse):

    DESCRICAO = (
        "Uma alma presa entre dois mundos. Nem vivo, nem morto.\n"
        "  Alta evasao, golpes criticos letais. Fraco se preso em duelo direto.\n"
        "  Velocidade +4 | Vida -20 | Forca +1 | Mana 50"
    )

    def __init__(self, nome):
        Player.__init__(self, nome)
        self._init_habilidades(mana_max=50)

        self.velocidade  += 4
        self.vida_maxima -= 20
        self.vida        -= 20
        self.forca       += 1

        self._evasao_ativa  = False   # Se True, tem chance de esquivar
        self._critico_bonus = 0       # Acumulado pelo Acumulo de Sombras

        self.habilidades = [
            Habilidade(
                "Golpe Fantasma",
                "Ataque rapido. Ignora 40% da defesa. Alto critico.",
                custo=8,
                fn_executar=_golpe_fantasma,
            ),
            Habilidade(
                "Passo das Sombras",
                "Garante esquiva no proximo ataque. Recupera mana.",
                custo=6,
                fn_executar=_passo_sombras,
            ),
            Habilidade(
                "Lamina Espectral",
                "Dois golpes rapidos seguidos. Menor dano por golpe.",
                custo=14,
                fn_executar=_lamina_espectral,
            ),
            Habilidade(
                "Acumulo de Sombras",
                "Nao ataca. Acumula poder: proximo golpe critico garantido.",
                custo=5,
                fn_executar=_acumulo_sombras,
            ),
            Habilidade(
                "Dissolucao",
                "Se torna intangivel por 2 turnos. Nao recebe dano.",
                custo=20,
                fn_executar=_dissolucao,
            ),
        ]

    def tentar_esquiva(self):
        """Chamado pelo sistema de combate quando inimigo ataca."""
        if self._evasao_ativa:
            self._evasao_ativa = False
            return True   # Esquivou
        # Chance base de esquiva por velocidade
        chance = min(self.obter_velocidade_total() * 2, 30)
        return random.randint(1, 100) <= chance

    def turno_passivo(self):
        msgs = super().turno_passivo()
        self.recuperar_mana(2)
        return msgs


# ============================================================================
# HABILIDADES
# ============================================================================

def _golpe_fantasma(usuario, alvo):
    crit   = (random.randint(1, 100) <= 35 + usuario._critico_bonus)
    mult   = 1.8 if crit else 1.0
    dano   = int(usuario.obter_forca_total() * mult) + random.randint(2, 10)
    alvo.tomar_dano(dano)
    usuario._critico_bonus = 0
    texto  = "  CRITICO!" if crit else "  "
    return (
        f"  Voce emerge das sombras como um relampago!\n"
        f"{texto} Golpe Fantasma: {dano} de dano."
    )


def _passo_sombras(usuario, alvo):
    usuario._evasao_ativa = True
    usuario.recuperar_mana(4)
    return (
        "  Voce se dissolve nas sombras.\n"
        "  Proximo ataque sera esquivado automaticamente.\n"
        "  +4 mana recuperada."
    )


def _lamina_espectral(usuario, alvo):
    d1 = int(usuario.obter_forca_total() * 0.7) + random.randint(0, 5)
    d2 = int(usuario.obter_forca_total() * 0.7) + random.randint(0, 5)
    alvo.tomar_dano(d1)
    alvo.tomar_dano(d2)
    return (
        f"  Duas laminas de sombra rasgam o ar!\n"
        f"  Primeiro golpe: {d1} | Segundo golpe: {d2}\n"
        f"  Total: {d1+d2} de dano."
    )


def _acumulo_sombras(usuario, alvo):
    usuario._critico_bonus += 40
    return (
        "  Voce se concentra. Sombras se condensam ao seu redor.\n"
        "  Proximo golpe tera critico garantido (+40% chance acumulada)."
    )


def _dissolucao(usuario, alvo):
    usuario.aplicar_efeito("Intangivel", {
        "tipo":   "cura",
        "valor":  0,
        "turnos": 2,
    })
    usuario._intangivel    = True
    usuario._turnos_intang = 2
    return (
        "  Seu corpo se dissolve em particulas de sombra.\n"
        "  Por 2 turnos voce e intangivel — nenhum ataque fisico te acerta."
    )

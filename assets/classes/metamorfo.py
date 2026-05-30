# ============================================================================
# NOUTRORA RPG — CLASSE: METAMORFO
# ============================================================================
# Absorve a essência de inimigos derrotados, transformando-a em poder.
# Quanto mais mata, mais forte fica — mas perde a humanidade aos poucos.
#
# STATS BASE: Força +3 | Velocidade -1 | Mana 40
# IDENTIDADE: Guerreiro que escala com kills, habilidades de transformação.
# ============================================================================

import random
import time
from player import Player
from assets.classes.base_classe import BaseClasse, Habilidade


class Metamorfo(Player, BaseClasse):

    DESCRICAO = (
        "Criaturas que abandonaram a própria humanidade em busca de poder.\n"
        "  Cada inimigo morto os torna mais fortes — e menos humanos.\n"
        "  Força +3 | Velocidade -1 | Mana 40"
    )

    def __init__(self, nome):
        Player.__init__(self, nome)
        self._init_habilidades(mana_max=40)

        # Bônus de classe
        self.forca      += 3
        self.velocidade -= 1

        # Recursos exclusivos
        self.essencias        = []   # Essências acumuladas
        self.forma_ativa      = None # "besta" | "sombra" | None
        self._turnos_forma    = 0

        # Registra habilidades
        self.habilidades = [
            Habilidade(
                "Golpe Selvagem",
                "Ataque brutal. 140% de dano. Chance de atordoar.",
                custo=8,
                fn_executar=_golpe_selvagem,
            ),
            Habilidade(
                "Absorver Essencia",
                "Drena força vital do inimigo. Cura você enquanto causa dano.",
                custo=12,
                fn_executar=_absorver_essencia,
            ),
            Habilidade(
                "Forma de Besta",
                "Transforma por 3 turnos: +50% dano, -30% defesa.",
                custo=18,
                fn_executar=_forma_besta,
            ),
            Habilidade(
                "Grito Primordial",
                "Paralisa o inimigo por 1 turno. Causa dano psíquico.",
                custo=15,
                fn_executar=_grito_primordial,
            ),
            Habilidade(
                "Espinhos da Mutacao",
                "Reveste seu corpo de espinhos. Inimigos sofrem dano ao atacar.",
                custo=10,
                fn_executar=_espinhos,
            ),
        ]

    def absorver_essencia_pos_vitoria(self, goblin):
        """Chamado automaticamente após vitória no combate."""
        bonus_f = goblin.forca // 5
        bonus_v = goblin.velocidade // 5
        self.essencias.append({"tipo": goblin.obter_status()["tipo"], "f": bonus_f, "v": bonus_v})
        self.forca      += bonus_f
        self.velocidade += bonus_v
        self.recuperar_mana(5)
        return f"Essencia absorvida. +{bonus_f} forca, +{bonus_v} velocidade."

    def turno_passivo(self):
        msgs = super().turno_passivo()
        # Reduz turno da forma
        if self.forma_ativa and self._turnos_forma > 0:
            self._turnos_forma -= 1
            if self._turnos_forma == 0:
                self.forma_ativa = None
                msgs.append("  [Forma de Besta] encerrada. Você retorna ao normal.")
        return msgs

    def obter_forca_total(self):
        base = super().obter_forca_total()
        if self.forma_ativa == "besta":
            return int(base * 1.5)
        return base


# ============================================================================
# FUNÇÕES DAS HABILIDADES
# ============================================================================

def _golpe_selvagem(usuario, alvo):
    dano = int(usuario.obter_forca_total() * 1.4) + random.randint(0, 8)
    alvo.tomar_dano(dano)
    atordoou = random.randint(1, 100) <= 30
    msgs = [
        f"  Voce se lanca com furia animal!",
        f"  Golpe Selvagem causa {dano} de dano!",
    ]
    if atordoou:
        alvo._atordoado = True
        msgs.append("  O inimigo esta atordoado — perde o proximo turno!")
    return "\n".join(msgs)


def _absorver_essencia(usuario, alvo):
    dano = int(usuario.obter_forca_total() * 0.9) + random.randint(0, 5)
    alvo.tomar_dano(dano)
    cura = int(dano * 0.5)
    real = usuario.curar(cura)
    return (
        f"  Voce drena a forca vital do {alvo.obter_status()['tipo'].lower()}!\n"
        f"  Dano: {dano}  |  Cura recebida: +{real} HP"
    )


def _forma_besta(usuario, alvo):
    if usuario.forma_ativa == "besta":
        return "  Voce ja esta em Forma de Besta."
    usuario.forma_ativa   = "besta"
    usuario._turnos_forma = 3
    return (
        "  Seus ossos estalam. Sua pele escurece.\n"
        "  FORMA DE BESTA ativada por 3 turnos!\n"
        "  Dano +50% | Defesa -30%"
    )


def _grito_primordial(usuario, alvo):
    dano = int(usuario.obter_forca_total() * 0.6) + random.randint(5, 15)
    alvo.tomar_dano(dano)
    alvo._atordoado = True
    return (
        f"  Um grito que nao e humano rasga o corredor!\n"
        f"  Dano psiquico: {dano}\n"
        f"  {alvo.obter_status()['tipo']} paralisa por 1 turno!"
    )


def _espinhos(usuario, alvo):
    usuario.aplicar_efeito("Espinhos", {
        "tipo":      "especial_espinhos",
        "valor":     int(usuario.obter_forca_total() * 0.3),
        "turnos":    4,
        "descricao": "Inimigos tomam dano ao atacar",
    })
    # Marca no usuario para o sistema de combate verificar
    usuario._espinhos_ativos = True
    usuario._dano_espinhos   = int(usuario.obter_forca_total() * 0.3)
    return (
        "  Espinhos osseos emergem da sua pele!\n"
        f"  Por 4 turnos, inimigos tomam {usuario._dano_espinhos} de dano ao te atacar."
    )

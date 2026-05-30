# ============================================================================
# NOUTRORA RPG — CLASSE: PORTADOR DA MASMORRA
# ============================================================================
# Um ser que carrega a maldição de Noutrora no próprio corpo.
# Usa a própria vida como recurso. Quanto mais perto da morte, mais forte.
# Única classe sem mana — tudo custa HP.
#
# STATS BASE: Vida +30 | Força +2 | Velocidade 0 | Mana 0
# IDENTIDADE: Tank/berserker. Escala dano com HP baixo. Compra poder com vida.
# ============================================================================

import random
from player import Player
from assets.classes.base_classe import BaseClasse, Habilidade


class Portador(Player, BaseClasse):

    DESCRICAO = (
        "Carrega a maldicao de Noutrora no proprio corpo.\n"
        "  Usa HP em vez de mana. Quanto mais ferido, mais perigoso.\n"
        "  Vida +30 | Forca +2 | Velocidade 0 | Sem mana"
    )

    def __init__(self, nome):
        Player.__init__(self, nome)
        self._init_habilidades(mana_max=1)  # Simbólico

        self.vida_maxima += 30
        self.vida        += 30
        self.forca       += 2

        self.mana         = 999   # Sempre "tem mana" — o custo real é HP
        self.mana_maxima  = 999

        self.habilidades = [
            Habilidade(
                "Golpe da Maldicao",
                "Custa 10 HP. Dano escala: quanto menos vida, mais forte.",
                custo=0,  # Custo tratado internamente em HP
                fn_executar=_golpe_maldicao,
            ),
            Habilidade(
                "Absorver Dor",
                "Custa 15 HP. Converte sua propria dor em forca temporaria.",
                custo=0,
                fn_executar=_absorver_dor,
            ),
            Habilidade(
                "Resistencia da Maldicao",
                "Custa 8 HP. Reduz o proximo dano recebido em 80%.",
                custo=0,
                fn_executar=_resistencia,
            ),
            Habilidade(
                "Grito da Agonia",
                "Custa 20 HP. Causa dano baseado no HP perdido.",
                custo=0,
                fn_executar=_grito_agonia,
            ),
            Habilidade(
                "Pacto Ultimo",
                "Custa 30 HP. Ataque devastador. Mata voce se HP chegar a 0.",
                custo=0,
                fn_executar=_pacto_ultimo,
            ),
        ]

    def usar_habilidade(self, indice, alvo):
        """Override: custo é HP, não mana."""
        if not (0 <= indice < len(self.habilidades)):
            return "Habilidade inválida."
        return self.habilidades[indice].executar(self, alvo)

    def listar_habilidades(self):
        custos_hp = [10, 15, 8, 20, 30]
        linhas = ["  Habilidades (custam HP, nao mana):"]
        for i, h in enumerate(self.habilidades):
            custo = custos_hp[i] if i < len(custos_hp) else "?"
            linhas.append(f"    [{i}] [{custo} HP] {h.nome}  — {h.descricao}")
        return "\n".join(linhas)

    def obter_forca_total(self):
        """Portador fica mais forte quanto menos HP tem."""
        base = super().obter_forca_total()
        ratio = 1.0 - (self.vida / self.vida_maxima)  # 0.0 (full) a 1.0 (morto)
        bonus = int(ratio * base * 0.6)
        return base + bonus

    def turno_passivo(self):
        msgs = super().turno_passivo()
        # Portador regenera levemente se HP crítico
        if self.vida <= self.vida_maxima * 0.2:
            real = self.curar(3)
            msgs.append(f"  [Maldicao] Limiar critico — regenerou {real} HP.")
        return msgs


# ============================================================================
# HABILIDADES
# ============================================================================

def _golpe_maldicao(usuario, alvo):
    custo_hp = 10
    if usuario.vida <= custo_hp:
        return "  HP insuficiente para usar esta habilidade."
    usuario.tomar_dano(custo_hp)
    ratio = 1.0 - (usuario.vida / usuario.vida_maxima)
    mult  = 1.0 + ratio * 1.5
    dano  = int(usuario.obter_forca_total() * mult) + random.randint(3, 12)
    alvo.tomar_dano(dano)
    return (
        f"  A maldicao em seu corpo explode para fora!\n"
        f"  -{custo_hp} HP proprio.  Multiplicador: {mult:.1f}x\n"
        f"  Dano causado: {dano}"
    )


def _absorver_dor(usuario, alvo):
    custo_hp = 15
    if usuario.vida <= custo_hp:
        return "  HP insuficiente."
    usuario.tomar_dano(custo_hp)
    bonus = int(custo_hp * 1.5)
    usuario.forca += bonus
    usuario.aplicar_efeito("Dor Absorvida", {
        "tipo":   "especial",
        "valor":  0,
        "turnos": 2,
    })
    return (
        f"  Voce absorve a propria agonia e a transforma em raiva!\n"
        f"  -{custo_hp} HP  |  +{bonus} forca por 2 turnos!"
    )


def _resistencia(usuario, alvo):
    custo_hp = 8
    if usuario.vida <= custo_hp:
        return "  HP insuficiente."
    usuario.tomar_dano(custo_hp)
    usuario._resistencia_ativa = True
    return (
        f"  A maldicao endurece sua carne!\n"
        f"  -{custo_hp} HP proprio.\n"
        f"  Proximo dano recebido reduzido em 80%."
    )


def _grito_agonia(usuario, alvo):
    custo_hp = 20
    if usuario.vida <= custo_hp:
        return "  HP insuficiente."
    usuario.tomar_dano(custo_hp)
    hp_perdido = usuario.vida_maxima - usuario.vida
    dano = int(hp_perdido * 0.6) + random.randint(5, 15)
    alvo.tomar_dano(dano)
    return (
        f"  Um grito que vem de dentro da maldicao!\n"
        f"  HP perdido total: {hp_perdido}  ->  Dano: {dano}\n"
        f"  O {alvo.obter_status()['tipo'].lower()} recua."
    )


def _pacto_ultimo(usuario, alvo):
    custo_hp = 30
    if usuario.vida <= custo_hp + 1:
        return "  HP insuficiente. Este golpe te mataria."
    usuario.tomar_dano(custo_hp)
    dano = int(usuario.obter_forca_total() * 3.0) + random.randint(15, 30)
    alvo.tomar_dano(dano)
    return (
        f"  PACTO ULTIMO!\n"
        f"  Toda a maldicao de Noutrora flui pelo seu corpo de uma vez!\n"
        f"  -{custo_hp} HP proprio.\n"
        f"  DANO DEVASTADOR: {dano}!"
    )

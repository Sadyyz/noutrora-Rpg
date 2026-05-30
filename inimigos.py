# ============================================================================
# NOUTRORA RPG — SISTEMA DE INIMIGOS VARIADOS
# ============================================================================
# Substitui e expande goblin.py.
# Cada inimigo tem: stats, tipo de ataque especial, comportamento próprio.
# ============================================================================

import random
from config import VARIACAO_DANO

try:
    from systems.audio import audio_manager
except ImportError:
    audio_manager = None


# ============================================================================
# CLASSE BASE DE INIMIGO
# ============================================================================

class Inimigo:
    """
    Base para todos os inimigos.
    O sistema de combate em batalhas.py usa esta interface.
    """

    TIPO = "Inimigo"

    def __init__(self, nivel=1):
        self.nivel        = nivel
        self.vida         = 0
        self.vida_maxima  = 0
        self.forca        = 0
        self.velocidade   = 0
        self._atordoado         = False
        self._turnos_atordoado  = 0
        self._efeitos           = {}   # Mesmo sistema que player

    # ------------------------------------------------------------------
    # INTERFACE OBRIGATÓRIA (compatível com goblin.py legado)
    # ------------------------------------------------------------------

    def tomar_dano(self, dano):
        self.vida = max(0, self.vida - dano)

    def esta_vivo(self):
        return self.vida > 0

    def obter_status(self):
        return {
            "tipo":        self.TIPO,
            "vida":        self.vida,
            "vida_maxima": self.vida_maxima,
            "forca":       self.forca,
            "velocidade":  self.velocidade,
        }

    def descrever_visualmente(self):
        return f"Um {self.TIPO.lower()} de nível {self.nivel}."

    def aplicar_efeito(self, nome, dados):
        self._efeitos[nome] = dados.copy()

    def turno_passivo(self):
        """Processa efeitos de duração sobre o inimigo."""
        msgs  = []
        vazar = []
        for nome, ef in self._efeitos.items():
            if ef["tipo"] == "dano" and ef["valor"] > 0:
                self.tomar_dano(ef["valor"])
                msgs.append(f"  [{nome}] -{ef['valor']} HP no {self.TIPO.lower()}")
            ef["turnos"] -= 1
            if ef["turnos"] <= 0:
                vazar.append(nome)
        for n in vazar:
            del self._efeitos[n]
        return msgs

    def calcular_dano_ataque(self):
        """Dano base do ataque normal."""
        return self.forca + random.randint(0, VARIACAO_DANO)

    def acao_especial(self, player):
        """
        Ação especial do inimigo (chamada com ~25% de chance).
        Retorna string descritiva. Cada subclasse sobrescreve.
        """
        return None   # Sem ação especial na base

    def esta_atordoado(self):
        if self._atordoado:
            if self._turnos_atordoado > 0:
                self._turnos_atordoado -= 1
            if self._turnos_atordoado <= 0:
                self._atordoado = False
            return True
        return False

    def __str__(self):
        return f"{self.TIPO} nv{self.nivel} — Vida {self.vida}/{self.vida_maxima} | Forca {self.forca}"
    
    def tocar_som(self, evento="acerto"):
        """Toca som do inimigo: 'aparecimento', 'acerto' ou 'morte'."""
        if audio_manager:
            audio_manager.tocar_som_inimigo(self.TIPO, evento)


# ============================================================================
# GOBLIN  (inimigo clássico — compatível com salas.py legado)
# ============================================================================

_GOBLIN_STATS = {
    1:  (30,  5, 2), 2:  (40,  7, 3), 3:  (50, 10, 4),
    4:  (60, 15, 5), 5:  (70, 18, 5), 6:  (80, 22, 6),
    7:  (90, 26, 6), 8: (100, 30, 7), 9: (110, 35, 7),
    10: (120, 40, 8),
}

_GOBLIN_MUTANTE_STATS = {
    1:  (50,  10, 3), 2:  (70,  15, 4), 3:  (90,  20, 5),
    4:  (110, 25, 6), 5:  (130, 30, 7), 6:  (150, 35, 8),
    7:  (170, 40, 9), 8:  (190, 45, 10), 9: (210, 50, 11),
    10: (230, 55, 12),
}

_GOBLIN_DESC = [
    "Um pequeno goblin com pele pálida. Olhos malignos. Dentes podres.",
    "Um goblin musculoso coberto de cicatrizes. Ele já matou antes.",
    "Um guerreiro goblin quase humanóide. Inteligência tática nos olhos.",
    "Um campeão goblin com armadura de ossos. Veterano de dezenas de batalhas.",
    "Um líder goblin. Carrega uma arma forjada com propósito maligno.",
    "Uma criatura mais monstro que goblin. Pele como couro queimado.",
    "Uma abominação goblin. Veias vermelhas pulsam visivelmente.",
    "Um campeão antigo. Deveria estar morto há séculos.",
    "Uma criatura que perdeu a humanidade goblin. Puro instinto predatório.",
    "O goblin supremo — uma perfeição em morte e destruição.",
]

_GOBLIN_MUTANTE_DESC = [
    "Pele vermelha com veias luminosas. Olhos que brilham em amarelo.",
    "Musculatura retorcida fora da anatomia normal. Espículas na coluna.",
    "Múltiplos braços atrofiados. Sangue goteja de feridas que nunca fecham.",
    "Colosso deformado. Pele que muda de cor. Substância viscosa goteja.",
    "Criatura primordial. Ácido goteja da boca. Séculos de existência.",
    "Titã translúcido. Órgãos impossíveis visíveis sob a pele.",
    "Entidade quase demoníaca. Símbolos antigos escritos na pele.",
    "Terror antropomórfico. Múltiplas camadas de pele sobrepostas.",
    "Forma instável e pulsante. Fraturas na realidade ao redor.",
    "Presença que distorce a masmorra. Sua existência é um erro cósmico.",
]


class Goblin(Inimigo):
    TIPO = "Goblin"

    def __init__(self, nivel=None, mutante=False):
        super().__init__(nivel or random.randint(1, 10))
        self.mutante = mutante
        tabela = _GOBLIN_MUTANTE_STATS if mutante else _GOBLIN_STATS
        n = max(1, min(self.nivel, 10))
        v, f, vel = tabela[n]
        self.vida = self.vida_maxima = v
        self.forca = f
        self.velocidade = vel
        if mutante:
            self.TIPO = "Goblin Mutante"

    def descrever_visualmente(self):
        descricoes = _GOBLIN_MUTANTE_DESC if self.mutante else _GOBLIN_DESC
        return descricoes[min(self.nivel - 1, len(descricoes) - 1)]

    def acao_especial(self, player):
        if self.mutante and random.randint(1, 100) <= 30:
            dano = int(self.forca * 1.5)
            player.tomar_dano(dano)
            return f"  Goblin Mutante usa INVESTIDA! -{dano} HP em voce!"
        return None


# ============================================================================
# SOMBRA ERRANTE
# ============================================================================

_SOMBRA_STATS = {
    1: (25, 8, 6), 2: (35, 12, 7), 3: (45, 16, 8),
    4: (55, 20, 9), 5: (65, 24, 10),
}

_SOMBRA_DESC = [
    "Uma silhueta sem corpo definido. Olhos brancos no escuro. Absolutamente silenciosa.",
    "Uma forma de sombra densa que absorve a luz ao redor. Você sente o frio antes de vê-la.",
    "Uma entidade de escuridão pura. Ela se move sem tocar o chão.",
    "Uma Sombra antiga que ganhou consciência. Ela te observa com conhecimento.",
    "A Sombra Maior. Uma coluna de trevas que distorce o espaço ao redor.",
]


class SombraErrante(Inimigo):
    TIPO = "Sombra Errante"

    def __init__(self, nivel=None):
        super().__init__(nivel or random.randint(1, 5))
        n = max(1, min(self.nivel, 5))
        v, f, vel = _SOMBRA_STATS[n]
        self.vida = self.vida_maxima = v
        self.forca = f
        self.velocidade = vel
        self._drenou_turno = False

    def descrever_visualmente(self):
        return _SOMBRA_DESC[min(self.nivel - 1, 4)]

    def acao_especial(self, player):
        """Drena vida ao invés de atacar normalmente."""
        if random.randint(1, 100) <= 35:
            drenado = random.randint(5, 12)
            player.tomar_dano(drenado)
            self.vida = min(self.vida + drenado, self.vida_maxima)
            return (
                f"  DRENO DE VIDA! A sombra absorve {drenado} HP de voce!\n"
                f"  Ela se cura em {drenado} HP."
            )
        return None


# ============================================================================
# ESQUELETO GUARDIÃO
# ============================================================================

_ESQUELETO_STATS = {
    1: (40, 6, 2), 2: (55, 9, 3), 3: (70, 13, 4),
    4: (85, 17, 4), 5: (100, 22, 5),
}

_ESQUELETO_DESC = [
    "Um esqueleto remontado às pressas. Ossos que rangemcom cada passo.",
    "Um guardião esquelético com armadura de ferro enferrujada. Olhos vazios mas atentos.",
    "Um cavaleiro morto-vivo que ainda empunha sua lança. A memória muscular permanece.",
    "Um Esqueleto Maior, mais alto que o normal. Seus ossos têm gravuras de batalhas.",
    "O Guardião Supremo. Um esqueleto de um herói lendário, corrompido pela masmorra.",
]


class EsqueletoGuardiao(Inimigo):
    TIPO = "Esqueleto Guardiao"

    def __init__(self, nivel=None):
        super().__init__(nivel or random.randint(1, 5))
        n = max(1, min(self.nivel, 5))
        v, f, vel = _ESQUELETO_STATS[n]
        self.vida = self.vida_maxima = v
        self.forca = f
        self.velocidade = vel
        self._reconstruindo = False

    def descrever_visualmente(self):
        return _ESQUELETO_DESC[min(self.nivel - 1, 4)]

    def tomar_dano(self, dano):
        """Esqueleto tem 20% de chance de ignorar dano (estrutura óssea)."""
        if random.randint(1, 100) <= 20:
            print("  Os ossos deflectem o golpe! (resistencia ossea)")
            dano = int(dano * 0.3)
        super().tomar_dano(dano)

    def acao_especial(self, player):
        if random.randint(1, 100) <= 25:
            dano = int(self.forca * 1.2)
            player.tomar_dano(dano)
            return f"  GOLPE DE LANCA! O esqueleto arremessa a lanca! -{dano} HP!"
        return None


# ============================================================================
# AMALGAMA DE CARNE
# ============================================================================

_AMALGAMA_STATS = {
    1: (60, 10, 1), 2: (80, 15, 2), 3: (100, 20, 2),
    4: (125, 27, 3), 5: (150, 34, 3),
}

_AMALGAMA_DESC = [
    "Uma massa de carne e ossos que se move por conta própria. Cheiro insuportável.",
    "Um aglomerado de corpos parcialmente fundidos. Múltiplas bocas gemem ao mesmo tempo.",
    "Uma Amalgama maior. Rostos reconhecíveis emergem e desaparecem de sua superfície.",
    "Amalgama Maior. Parece crescer conforme você olha. Tentáculos de carne se estendem.",
    "A Grande Amalgama. Uma montanha de carne viva. A masmorra criou algo que não deveria existir.",
]


class AmalgamaDeCarne(Inimigo):
    TIPO = "Amalgama de Carne"

    def __init__(self, nivel=None):
        super().__init__(nivel or random.randint(1, 5))
        n = max(1, min(self.nivel, 5))
        v, f, vel = _AMALGAMA_STATS[n]
        self.vida = self.vida_maxima = v
        self.forca = f
        self.velocidade = vel

    def descrever_visualmente(self):
        return _AMALGAMA_DESC[min(self.nivel - 1, 4)]

    def tomar_dano(self, dano):
        """Regenera 20% do dano recebido."""
        super().tomar_dano(dano)
        regen = int(dano * 0.2)
        if regen > 0:
            self.vida = min(self.vida + regen, self.vida_maxima)

    def acao_especial(self, player):
        if random.randint(1, 100) <= 30:
            dano1 = int(self.forca * 0.7)
            dano2 = int(self.forca * 0.7)
            player.tomar_dano(dano1 + dano2)
            player.aplicar_efeito("Infeccao", {
                "tipo": "dano", "valor": 4, "turnos": 3
            })
            return (
                f"  TENTACULOS DE CARNE! Dois golpes simultâneos!\n"
                f"  -{dano1+dano2} HP + Infecção: 4 dano/turno por 3 turnos!"
            )
        return None


# ============================================================================
# ENTIDADE DORME-ACORDA (boss raro)
# ============================================================================

_ENTIDADE_STATS = {
    1: (80, 18, 5), 2: (110, 25, 6), 3: (150, 35, 7),
}

_ENTIDADE_DESC = [
    "Uma coisa que não deveria existir nesta dimensão. Sua forma contradiz a geometria.",
    "Uma entidade que dormiu por séculos. Você a acordou. Ela não está satisfeita.",
    "A Entidade Completa. Cada olho vê uma dimensão diferente. Sua sanidade resiste.",
]


class EntidadeAntica(Inimigo):
    TIPO = "Entidade Antica"

    def __init__(self, nivel=None):
        super().__init__(nivel or random.randint(1, 3))
        n = max(1, min(self.nivel, 3))
        v, f, vel = _ENTIDADE_STATS[n]
        self.vida = self.vida_maxima = v
        self.forca = f
        self.velocidade = vel
        self._fase       = 1   # Muda de fase em 50% HP

    def descrever_visualmente(self):
        return _ENTIDADE_DESC[min(self.nivel - 1, 2)]

    def tomar_dano(self, dano):
        era_fase1 = self._fase == 1
        super().tomar_dano(dano)
        # Transição de fase
        if era_fase1 and self.vida <= self.vida_maxima * 0.5:
            self._fase = 2
            self.forca = int(self.forca * 1.4)
            print("\n  *** A ENTIDADE MUDA DE FASE! ***")
            print(f"  Sua forca aumenta para {self.forca}!")

    def acao_especial(self, player):
        if random.randint(1, 100) <= 40:
            acao = random.choice(["sanidade", "olhar", "toque"])
            if acao == "sanidade":
                dano = random.randint(10, 20)
                player.tomar_dano(dano)
                player.velocidade = max(1, player.velocidade - 1)
                return f"  ATAQUE PSIQUICO! -{dano} HP e -1 velocidade permanente neste combate!"
            elif acao == "olhar":
                dano = int(self.forca * 1.8)
                player.tomar_dano(dano)
                return f"  O OLHAR DO VAZIO! Dano massivo: -{dano} HP!"
            elif acao == "toque":
                player.aplicar_efeito("Maldição Antica", {
                    "tipo": "dano", "valor": 10, "turnos": 4
                })
                return "  TOQUE DA MALDICAO! 10 dano/turno por 4 turnos!"
        return None


# ============================================================================
# FÁBRICA — gera inimigo aleatório por profundidade
# ============================================================================

def criar_inimigo_aleatorio(profundidade=1):
    """
    Gera inimigo com tipo e nível baseado na profundidade da masmorra.
    Profundidade = sala atual do jogador.
    """
    nivel = max(1, min(profundidade // 2 + random.randint(0, 2), 10))

    # Chance de cada tipo varia com a profundidade
    rolagem = random.randint(1, 100)

    if profundidade <= 5:
        # Começo: só goblins
        return Goblin(nivel, mutante=(rolagem <= 15))

    elif profundidade <= 12:
        # Meio: goblins + sombras + esqueletos
        if rolagem <= 45:
            return Goblin(nivel, mutante=(rolagem <= 10))
        elif rolagem <= 70:
            return SombraErrante(min(nivel, 5))
        else:
            return EsqueletoGuardiao(min(nivel, 5))

    elif profundidade <= 20:
        # Profundo: variedade completa
        if rolagem <= 30:
            return Goblin(nivel, mutante=(rolagem <= 8))
        elif rolagem <= 50:
            return SombraErrante(min(nivel, 5))
        elif rolagem <= 65:
            return EsqueletoGuardiao(min(nivel, 5))
        elif rolagem <= 90:
            return AmalgamaDeCarne(min(nivel, 5))
        else:
            return EntidadeAntica(min(nivel // 3 + 1, 3))

    else:
        # Abissal: inimigos pesados
        if rolagem <= 20:
            return Goblin(10, mutante=True)
        elif rolagem <= 40:
            return AmalgamaDeCarne(5)
        elif rolagem <= 70:
            return EntidadeAntica(random.randint(2, 3))
        else:
            return EsqueletoGuardiao(5)


def criar_goblin_aleatorio():
    """Compatibilidade com salas.py legado."""
    return Goblin(random.randint(1, 10))

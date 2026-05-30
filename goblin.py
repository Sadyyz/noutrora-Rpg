# ============================================================================
# NOUTRORA RPG — CLASSE GOBLIN
# ============================================================================

import random
from config import GOBLINS_STATS, GOBLINS_MUTANTES_STATS, TIPOS_INIMIGOS


class Goblin:
    """Representa um goblin (inimigo) na masmorra."""

    def __init__(self, nivel=None, mutante=False):
        tabela = GOBLINS_MUTANTES_STATS if mutante else GOBLINS_STATS
        if nivel is None or nivel < 1 or nivel > 10:
            nivel = random.randint(1, 10)
        stats = tabela[nivel]

        self.nivel        = nivel
        self.mutante      = mutante
        self.vida         = stats["vida"]
        self.vida_maxima  = stats["vida"]
        self.forca        = stats["forca"]
        self.velocidade   = stats["velocidade"]

    def tomar_dano(self, dano):
        self.vida = max(0, self.vida - dano)

    def esta_vivo(self):
        return self.vida > 0

    def obter_status(self):
        return {
            "tipo":         "Goblin Mutante" if self.mutante else "Goblin",
            "vida":         self.vida,
            "vida_maxima":  self.vida_maxima,
            "forca":        self.forca,
            "velocidade":   self.velocidade,
        }

    def descrever_visualmente(self):
        """Descrição cinematográfica baseada em nível."""
        if self.mutante:
            descricoes = [
                "Uma criatura de pele vermelha com veias luminosas pulsando.",
                "Um mutante maior, com musculatura retorcida que não segue anatomia normal.",
                "Uma abominação com múltiplos braços atrofiados saindo de seu corpo.",
                "Um colosso deformado com pele que muda de cor conforme move.",
                "Uma criatura primordial que mal parece goblin. Ácido goteja de sua boca.",
                "Um titã de pesadelo. Sua pele é translúcida e você vê órgãos que não deveriam existir.",
                "Uma entidade quase demoníaca envolvida em um brilho negro que absorve luz.",
                "Um terror antropomórfico. Múltiplas camadas de pele transparente.",
                "Uma criatura que desafia descrição. Seu corpo flutua levemente do chão.",
                "Um deus abominável. Sua presença distorce a masmorra ao seu redor.",
            ]
        else:
            descricoes = [
                "Um pequeno goblin com pele pálida e enrugada. Seus olhos são pequenos mas malignos.",
                "Um goblin mais musculoso com cicatrizes pelo corpo.",
                "Um guerreiro goblin de aparência quase humanóide.",
                "Um campeão goblin com armadura caseira feita de ossos.",
                "Um goblin líder, maior e mais forte que seus pares.",
                "Uma criatura que é mais monstro que goblin.",
                "Uma abominação goblin que transcende a biologia normal.",
                "Um campeão antigo que deveria estar morto há séculos.",
                "Uma criatura que perdeu quase sua humanidade goblin.",
                "O goblin ultimate — uma perfeição em morte e destruição.",
            ]
        idx = min(self.nivel - 1, len(descricoes) - 1)
        return descricoes[idx]

    def __str__(self):
        tipo = "Goblin Mutante" if self.mutante else "Goblin"
        return f"{tipo} nv{self.nivel} — Vida {self.vida}/{self.vida_maxima} | Força {self.forca}"


def criar_goblin_aleatorio():
    return Goblin(random.randint(1, 10))


def obter_tipo_inimigo_aleatorio():
    return TIPOS_INIMIGOS[random.randint(1, len(TIPOS_INIMIGOS))]

# ============================================================================
# CLASSE GOBLIN - Encapsula toda a lógica do inimigo
# ============================================================================

import random
from config import GOBLINS_STATS, GOBLINS_MUTANTES_STATS, TIPOS_INIMIGOS


class Goblin:
    """Representa um goblin na masmorra."""

    def __init__(self, nivel, mutante=False):
        """
        Inicializa um goblin com nível de dificuldade.
        
        Args:
            nivel (int): Nível de dificuldade (1-10)
            mutante (bool): Se True, é um goblin mutante (mais poderoso)
        """
        stats_table = GOBLINS_MUTANTES_STATS if mutante else GOBLINS_STATS

        # Garante que o nível está no intervalo válido
        if nivel < 1 or nivel > 10:
            nivel = random.randint(1, 10)

        stats = stats_table[nivel]
        self.vida = stats["vida"]
        self.vida_maxima = stats["vida"]
        self.forca = stats["forca"]
        self.velocidade = stats["velocidade"]
        self.mutante = mutante

    def tomar_dano(self, dano):
        """
        Goblin recebe dano. Não pode ficar com vida negativa.
        
        Args:
            dano (int): Quantidade de dano recebido
        """
        self.vida = max(0, self.vida - dano)

    def esta_vivo(self):
        """Verifica se o goblin está vivo."""
        return self.vida > 0

    def obter_status(self):
        """Retorna dicionário com status atual."""
        tipo = "Goblin Mutante" if self.mutante else "Goblin"
        return {
            "tipo": tipo,
            "vida": self.vida,
            "vida_maxima": self.vida_maxima,
            "forca": self.forca,
            "velocidade": self.velocidade,
        }

    def __str__(self):
        """Representação em string do goblin."""
        tipo = "Goblin Mutante" if self.mutante else "Goblin"
        return (
            f"{tipo} - Vida: {self.vida}/{self.vida_maxima} | "
            f"Força: {self.forca} | Velocidade: {self.velocidade}"
        )


def criar_goblin_aleatorio():
    """
    Cria um goblin com nível aleatório.
    
    Returns:
        Goblin: Um novo goblin com nível 1-10
    """
    nivel = random.randint(1, 10)
    return Goblin(nivel)


def obter_tipo_inimigo_aleatorio():
    """
    Retorna uma descrição aleatória de inimigos para narrativa.
    
    Returns:
        str: Descrição do tipo de inimigo (ex: "1 goblin", "3 goblins")
    """
    indice = random.randint(1, len(TIPOS_INIMIGOS))
    return TIPOS_INIMIGOS[indice]

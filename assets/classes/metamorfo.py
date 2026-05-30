# ============================================================================
# NOUTRORA RPG — CLASSE METAMORFO
# ============================================================================

from player import Player


class Metamorfo(Player):
    """
    Metamorfos absorvem a essência de monstros derrotados,
    transformando almas inimigas em armas devastadoras.
    """

    def __init__(self, nome="Metamorfo"):
        super().__init__(nome)
        self.forca     += 3
        self.velocidade -= 1
        self.essencias  = []   # Essências absorvidas de inimigos

    def absorver_essencia(self, goblin):
        """Absorve essência ao derrotar um inimigo."""
        essencia = {
            "tipo":       "Goblin Mutante" if goblin.mutante else "Goblin",
            "forca":      goblin.forca // 4,
            "velocidade": goblin.velocidade // 4,
        }
        self.essencias.append(essencia)
        self.forca      += essencia["forca"]
        self.velocidade += essencia["velocidade"]
        return f"Essência absorvida! +{essencia['forca']} força, +{essencia['velocidade']} velocidade."

    def listar_essencias(self):
        if not self.essencias:
            return "  Nenhuma essência absorvida."
        return "\n".join(f"  Essência de {e['tipo']}" for e in self.essencias)

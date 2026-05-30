# ============================================================================
# NOUTRORA RPG — CLASSE DRUIDA
# ============================================================================

from player import Player


class Druida(Player):
    """
    Guardiões do equilíbrio natural.
    Enfraquecendo lentamente qualquer inimigo que cruze seu caminho.
    """

    def __init__(self, nome="Druida"):
        super().__init__(nome)
        self.velocidade += 2
        self.forca      -= 2
        self.veneno_cargas = 3   # Cargas de veneno disponíveis

    def envenenar(self, goblin):
        """
        Aplica veneno. Causa dano ao longo de turnos futuros.
        Simplificado: causa dano imediato proporcional à velocidade.
        """
        if self.veneno_cargas <= 0:
            return "Sem cargas de veneno."

        dano = self.velocidade * 2
        goblin.tomar_dano(dano)
        self.veneno_cargas -= 1
        return f"Veneno aplicado! {dano} dano.  ({self.veneno_cargas} cargas restantes)"

    def regenerar_veneno(self):
        """Regenera uma carga de veneno (fontes, altares)."""
        self.veneno_cargas = min(self.veneno_cargas + 1, 5)

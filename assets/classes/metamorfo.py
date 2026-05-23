from assets.classes.config_classe import ClasseBase
import random


class Metamorfo(ClasseBase):

    def __init__(self):
        super().__init__()

        self.nome = "Metamorfo"
        self.vida = 90
        self.forca = 12
        self.velocidade = 8

        self.essencia = None

    def tentar_absorver(self):
        chance = random.randint(1, 100)

        if chance <= 30:
            self.essencia = "Goblin"
            print("Você absorveu a essência do Goblin!")

    def usar_essencia(self):
        if self.essencia:
            print("Você usou o ataque da essência!")
            return random.randint(1, 40)

        print("Você não possui essência.")
        return 0
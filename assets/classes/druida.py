from assets.classes.config_classe import ClasseBase


class Druida(ClasseBase):

    def __init__(self):
        super().__init__()

        self.nome = "Druida"
        self.vida = 110
        self.forca = 8
        self.velocidade = 6

        self.contador_ataques = 0
        self.veneno = 2

    def atacar(self):
        self.contador_ataques += 1

        print("Druida atacou!")

    def pode_envenenar(self):
        return self.contador_ataques >= 3

    def usar_veneno(self):
        if self.pode_envenenar():
            self.contador_ataques = 0

            print("Inimigo envenenado!")
            return self.veneno

        print("Skill ainda carregando.")
        return 0
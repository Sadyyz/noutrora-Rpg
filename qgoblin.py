import random

def status_goblins():
    gstatus = {
        1: {"vida": 30, "forca": 5, "velocidade": 2},
        2: {"vida": 40, "forca": 7, "velocidade": 3},
        3: {"vida": 50, "forca": 10, "velocidade": 4},
        4: {"vida": 60, "forca": 15, "velocidade": 5},
        5: {"vida": 70, "forca": 18, "velocidade": 5},
        6: {"vida": 80, "forca": 22, "velocidade": 6},
        7: {"vida": 90, "forca": 26, "velocidade": 6},
        8: {"vida": 100, "forca": 30, "velocidade": 7},
        9: {"vida": 110, "forca": 35, "velocidade": 7},
        10: {"vida": 120, "forca": 40, "velocidade": 8},
    }
    return gstatus[random.randint(1, 10)]

def golins_mutantes():
    gmutantes = {
        1: {"vida": 50, "forca": 10, "velocidade": 3},
        2: {"vida": 70, "forca": 15, "velocidade": 4},
        3: {"vida": 90, "forca": 20, "velocidade": 5},
        4: {"vida": 110, "forca": 25, "velocidade": 6},
        5: {"vida": 130, "forca": 30, "velocidade": 7},
        6: {"vida": 150, "forca": 35, "velocidade": 8},
        7: {"vida": 170, "forca": 40, "velocidade": 9},
        8: {"vida": 190, "forca": 45, "velocidade": 10},
        9: {"vida": 210, "forca": 50, "velocidade": 11},
        10: {"vida": 230, "forca": 55, "velocidade": 12},
    }
    return gmutantes[random.randint(1, 10)]

# aqui tem a função que gera a quantidade de goblins aleatoriamente para cada cenario, o que torna cada jogo diferente do outro


def quantidade_goblins():
    qgoblins = {
        1: "1 inimigo",
        2: "2 inimigos",
        3: "3 inimigos",
        4: "um goblin de armadura",
    }
    valor = random.randint(1, 4)
    return qgoblins[valor]
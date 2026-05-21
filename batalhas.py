import random
import time 
import splayer
import qgoblin  


def turno(nome, player_status, goblin_status):


    dano_player = player_status["forca"] + random.randint(0, 5)
    dano_goblin = goblin_status["forca"] + random.randint(0, 5)

    goblin_status["vida"] -= dano_player
    player_status["vida"] -= dano_goblin

    print(f"Você causou {dano_player} de dano ao goblin!")
    time.sleep(1)
    if goblin_status["vida"] <= 0:

        print("Você derrotou o goblin!")

        return "vitória"
    
    print(f"Vida restante do goblin: {goblin_status['vida']}")
    print(f"o goblin é tomado pela dor de seu ataque, contra-ataca com ferocidade!")
    time.sleep(3)
    print(f"O goblin causou {dano_goblin} de dano a você!")
    if player_status["vida"] <= 0:

        print("Você foi derrotado pelo goblin...")
        return "derrota"
    


        

def encontro_cavernas(nome, cenario_text):
    
    player_status = splayer.status_player()
    goblin_status = qgoblin.status_goblins()
    if player_status["vida"] <= 0:
        player_status["vida"] = 0

    if goblin_status["vida"] <= 0:
        goblin_status["vida"] = 0

    print(cenario_text)

    while True: 


        

        print("1 - batalhar")
        print("2 - correr")

        acao = input(f"{nome} qual sera sua decisao ")

        if acao == "1":


            print("Um duelo se aproxima nas sombras da caverna.")

            print(f"vida: {player_status['vida']}")
            print(f"forca: {player_status['forca']}")
            print(f"velocidade: {player_status['velocidade']}")

            print(f"status do goblin: {goblin_status}")

            if goblin_status["velocidade"] <= player_status["velocidade"]:

                print("voce foi mais rapido que o goblin")

                print("1 - atacar")
                print("2 - defender")

                escolha = input("digite sua escolha: ")

                if escolha == "1":

                    turno(nome, player_status, goblin_status)
                    acao = "0"

            elif acao == "2" or player_status["vida"] <= 0 or goblin_status["vida"] <= 0:
                print("fim de jogo...")
                return "fim de jogo"
            
                
            else:

                print("o goblin foi mais rapido!")

                turno(nome, player_status, goblin_status)
                
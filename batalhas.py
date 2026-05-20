import random
import time 
import qgoblin
import player

def encontro_cavernas(nome, cenario_text):
    """Inicia o encontro nas cavernas."""
    print(cenario_text)
    print("1 - batalhar")
    print("2 - correr")
    acao = input(f"{nome} qual sera sua decisao")
    
    if acao == "1":
        goblin_status = qgoblin.status_goblins()
        print("voce entrou em batalha")
        print("antes da luta, voce observa seu inimigo e descobre seus status")
        print(f"voce tem {player.pvida} de vida")
        print(f"os status do goblin sao: {goblin_status}")
        print("nao da pra continuar mais pq eu nao terminei")

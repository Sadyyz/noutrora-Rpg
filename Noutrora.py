import random
vidap = 100
vidag = 40
qgoblins = {
    1: "1 inimigo",
    2: "2 inimigos",
    3: "3 inimigos",
    4: "um goblin de armadura"
}
qvalor = random.randint(1,4)
goblin = qgoblins[qvalor]
cenariosmg = {
    1: f"um corredor barulhento onde voce se depara com {goblin}",

    2: f"uma sala coberta por corpos antigos onde aparecem {goblin}",

    3: f"um corredor inundado ate seus joelhos onde algo observa voce junto de {goblin}",

    4: f"uma biblioteca abandonada onde livros se movem sozinhos e {goblin} bloqueiam seu caminho",

    5: f"uma capela destruida iluminada apenas por velas vermelhas onde surgem {goblin}",

    6: f"um tunel estreito onde sons de correntes ecoam enquanto {goblin} se aproximam",

    7: f"uma sala silenciosa demais onde voce encontra {goblin} olhando fixamente para voce",

    8: f"um corredor cheio de simbolos estranhos onde {goblin} aparecem das sombras",

    9: f"uma ponte quebrada sobre um abismo sem fim onde {goblin} impedem sua passagem",

    10: f"uma sala completamente escura onde apenas os olhos de {goblin} podem ser vistos"
}
cenarios = random.randint(1,10)
print("Bem vindo ao Noutrora. Um rpg de texto com elementos de terror e suspense. um agradecimento de Sady, bom jogo avenntureiro")
print("Você faz parte de um vilareijo de nome stormcloak, onde voce e sua familia vendem armas para o reino vizinho: nofengard.") 
print(" Um dia, lendo o jornal da guilda voce teve a brilhante ideia de pegar seu equipamento e ir em direção de uma masmorra conhecida como: Noitrora. Sua jornada começa aqui aventureiro. Mas antes, eu gostaria de perguntar...")
nome = input(" Qual seria seu nome")
print(cenariosmg[cenarios])
print("1 - batalhar")
print(" 2 - correr ")
acao = input(f"{nome} qual sera sua decisao")
if acao == "1":
    print("voce entrou em batalha")
    print(f"voce tem {vidap} de vida")
    print(f"goblin tem {vidag} de vida")
    print("nao da pra continuar mais pq eu nao terminei")
import random
import time
from batalhas import encontro_cavernas
import qgoblin
import player

# bibliotecas

goblin = qgoblin.quantidade_goblins()
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
    10: f"uma sala completamente escura onde apenas os olhos de {goblin} podem ser vistos",
}
cenarios = random.randint(1, 10)
# acima o comando de aleatoriedade de cenario

def start_game():
    while True:
        skip = input("deseja pular prologo? sim/nao").lower()
        if skip == "nao" or skip == "não":
            print(
                "A chuva caía violentamente sobre os telhados de Stormcloak naquela noite."
            )
            time.sleep(3)
            print(
                "O pequeno vilarejo, conhecido por seus ferreiros e comerciantes de armas, parecia mais silencioso do que o normal. As poucas pessoas que ainda caminhavam pelas ruas evitavam olhar umas para as outras, como se algo ruim estivesse prestes a acontecer"
            )
            time.sleep(8)
            print("Você cresceu naquele lugar...")
            time.sleep(2)
            print(
                "Filho de uma família de artesãos, passou a maior parte da vida ajudando na forja e ouvindo histórias sobre aventureiros, monstros e ruínas esquecidas pelo reino. Histórias que pareciam absurdas… até agora."
            )
            time.sleep(8)
            print(
                "Enquanto organizava algumas mercadorias antigas da oficina, seus olhos encontraram um jornal amassado da Guilda dos Aventureiros."
            )
            time.sleep(6)
            print("Em destaque, uma manchete chamava atenção:")
            print("A Masmorra de Noutrora volta a emitir sinais de atividade após decadas")
            time.sleep(7)
            print(
                "Diziam que Noutrora era uma masmorra amaldiçoada localizada nas profundezas das montanhas ao norte. Muitos aventureiros entraram naquele lugar em busca de riqueza, fama ou respostas… mas poucos retornaram."
            )
            time.sleep(5)
            print("E os que voltaram jamais foram os mesmos.")
            print(
                "Naquela mesma noite, tomado pela curiosidade — ou talvez por algo pior — você decide preparar seu equipamento e partir em direção às montanhas."
            )
            time.sleep(5)
            print(
                "O vento gelado sopra contra seu rosto enquanto a enorme entrada da masmorra surge diante de você."
            )
            time.sleep(5)
            print("Sua jornada começa agora.")
            print("mas... nao existe heroi sem nome...")
            time.sleep(2)
            print("nao é mesmo?")
            time.sleep(4)
            print("me diga...")
            time.sleep(2)
            print("qual")
            time.sleep(1)
            print("é")
            time.sleep(1)
            print("o")
            print("seu")
            time.sleep(1)
            print("nome")
            break
        # prologo + quebra do loop
        elif skip == "sim":
            print("prologo pulado!")
            break
        else:
            print("digite sua respota corretamente!")

    while True:
        nome = input("Digite seu nome: ")

        # Verifica se o comprimento do nome é menor ou igual a 3 caracteres
        if len(nome) <= 3:
            print("Nome inválido! O nome deve ter mais de 3 letras.")
        else:
            print("boa sorte aventureiro... sua aventura comeca agora")
            break  # Sai do loop porque o nome está correto

    encontro_cavernas(nome, cenariosmg[cenarios])

if __name__ == "__main__":
    start_game()

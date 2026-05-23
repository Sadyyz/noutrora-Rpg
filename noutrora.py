import random
import time
from batalhas import encontro_combate
from player import Player
from goblin import criar_goblin_aleatorio
from salas import gerar_sala_aleatoria, SalaCombate, SalaTesourou, SalaCura, SalaVenda
from config import NOME_MINIMO
from assets.classes.metamorfo import Metamorfo
from assets.classes.druida import Druida
import colorama
from colorama import Fore, Style, init

init(autoreset=True)
print(Fore.LIGHTGREEN_EX + r"""

███╗   ██╗ ██████╗ ██╗   ██╗████████╗██████╗  ██████╗ ██████╗  █████╗ 
████╗  ██║██╔═══██╗██║   ██║╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██╔══██╗
██╔██╗ ██║██║   ██║██║   ██║   ██║   ██████╔╝██║   ██║██████╔╝███████║
██║╚██╗██║██║   ██║██║   ██║   ██║   ██╔══██╗██║   ██║██╔══██╗██╔══██║
██║ ╚████║╚██████╔╝╚██████╔╝   ██║   ██║  ██║╚██████╔╝██║  ██║██║  ██║
╚═╝  ╚═══╝ ╚═════╝  ╚═════╝    ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝
         Onde almas esquecidas vagam pela escuridão..."
""")


def escolher_classe():

    print("Escolha sua classe:")
    print("1 - Metamorfo")
    print("2 - Druida")

    opcao = input(">> ")

    if opcao == "1":
        jogador = Metamorfo()
        print("Metamorfo...")
        print("Criaturas que abandonaram a própria humanidade em busca de poder.")
        print("Metamorfos absorvem a essência de monstros derrotados,")
        print("transformando almas inimigas em armas devastadoras.")
    

    elif opcao == "2":
        jogador = Druida()
        print("Druida...")
        print("Guardiões do equilíbrio natural.")
        print("Druidas manipulam toxinas e energias da floresta,")
        print("enfraquecendo lentamente qualquer inimigo que cruze seu caminho.")

    else:
        print("Classe inválida.")
        return None

    print(f"Classe escolhida: {jogador.nome}")

    return jogador

def start_game():
    """Controlador principal do jogo. Gerencia o fluxo narrativo e exploração."""
    
    # ========== FASE 1: PRÓLOGO ==========
    _exibir_prologo()

    # ========== FASE 2: CRIAR JOGADOR ==========
    nome = _obter_nome_jogador()
    classep = escolher_classe()
    player = Player(nome)
    
    print(f"\n✨ Bem-vindo, {player.nome}!")
    print(f"Seus atributos iniciais:")
    print(f"  • Vida: {player.vida}")
    print(f"  • Força: {player.forca}")
    print(f"  • Velocidade: {player.velocidade}")
    time.sleep(3)

    # ========== FASE 3: LAÇO PRINCIPAL DE EXPLORAÇÃO ==========
    _explorar_masmorr(nome, player)


def _exibir_prologo():
    """Exibe o prólogo do jogo (pode ser pulado)."""
    while True:
        skip = input("\nDeseja pular o prólogo? (sim/nao): ").lower().strip()
        
        if skip in ["nao", "não"]:
            print(
                "\n" + "=" * 60
                + "\n\n⛈️  A chuva caía como punhos de um colosso invisível sobre os telhados de Stormcloak."
            )
            time.sleep(3)
            print(
                "Os brilhos dos raios iluminavam a cidade de forma fosca e antinatural. O pequeno vilarejo, "
                "conhecido por seus ferreiros e comerciantes de armas, parecia ter sido abandonado há séculos. "
                "As poucas pessoas que ainda caminhavam pelas ruas de paralelepípedo molhado evitavam não apenas "
                "olhar umas para as outras, mas evitavam olhar para cima. Era como se algo pairasse sobre a cidade "
                "— uma presença invisível que sugava toda esperança."
            )
            time.sleep(8)
            print("\n🌙 Você cresceu naquele lugar de desesperança...")
            time.sleep(2)
            print(
                "Filho de uma família de artesãos, passou a maior parte de sua vida mergulhado em fuligem e calor, "
                "ajudando seu pai a forjar espadas que ninguém mais encomendava. Noites inteiras ouvindo histórias "
                "sobre aventureiros lendários, monstros que desafiavam a compreensão humana, e ruínas de civilizações "
                "que o próprio tempo parecia querer esquecer. Histórias que pareciam absurdas... até que começaram a "
                "fazer sentido. Até que começou a acreditar que talvez fossem verdadeiras."
            )
            time.sleep(8)
            print(
                "\n📰 Enquanto organizava mercadorias antigas na oficina — coisas que pertenciam ao seu avô, talvez até "
                "ao avô do seu avó — seus dedos encontraram um jornal amassado, metade comido por traças, da Guilda "
                "dos Aventureiros. A data era de três meses atrás."
            )
            time.sleep(6)
            print("\n✍️  Em destaque, uma manchete que seu coração não conseguiu ignorar:")
            print("\n>>> ⚠️  A MASMORRA DE NOUTRORA VOLTA A EMITIR SINAIS DE ATIVIDADE APÓS 200 ANOS <<<\n")
            time.sleep(7)
            print(
                "Noutrora. O nome sozinho era suficiente para fazer o sangue esfriar. Uma masmorra amaldiçoada "
                "localizada nas profundezas das montanhas ao norte, além da Floresta Negra, em um lugar que os mapas "
                "oficiais deixavam em branco. Histórias contadas em sussurros falam de uma estrutura que não deveria "
                "existir, construída por uma civilização que foi apagada da história. Muitos aventureiros — os melhores, "
                "os mais destemidos — entraram naquele abismo em busca de riqueza imensurável, fama eterna, ou respostas "
                "para perguntas que nem sabiam que tinham. Mas poucos retornaram. Muito poucos."
            )
            time.sleep(5)
            print("\n💀 E os que voltaram... não eram mais as mesmas pessoas.")
            time.sleep(2)
            print(
                "Um deles foi encontrado três dias depois de sua saída, envelhecido 20 anos em uma semana. Outro perdeu "
                "a visão, mas insistia que ainda via coisas que os olhos não deveriam ver. Uma mulher voltou falando em "
                "linguagens que ninguém conseguia identificar, escrevendo símbolos que queimavam a vista quando alguém "
                "tentava olhar."
            )
            time.sleep(5)
            print(
                "\n🔥 Naquela mesma noite, algo mudou em você. Talvez fosse curiosidade. Talvez fosse ganância. Ou talvez "
                "fosse algo mais antigo — uma chamada que você não conseguia explicar, como se Noutrora estivesse te sussurrando "
                "através do tempo e da distância, dizendo que você era o que faltava. O que tinha sido prometido."
            )
            time.sleep(5)
            print(
                "Você retirou uma velha mochila de debaixo do seu colchão, preparou seu melhor equipamento com as mãos tremendo, "
                "e naquela madrugada — sem avisar ninguém, como se soubesse que ninguém poderia conter você — você partiu em direção "
                "às montanhas. A chuva no seu rosto não era mais chuva. Era advertência."
            )
            time.sleep(5)
            print(
                "\n🌑 Depois de semanas de jornada através de florestas que pareciam estar vivas e respirando, você chegou. "
                "A entrada de Noutrora não é grande ou impressionante — é muito pior. É exatamente do tamanho certo para parecer "
                "que foi feita especificamente para você. O ar que sai do interior é quente e carregado de um cheiro que seus instintos "
                "primitivos identificam imediatamente como morte. O vento que passa pela entrada parece sussurrar palavras que você "
                "quase consegue entender.\n"
            )
            time.sleep(5)
            print("Este é o limiar.")
            time.sleep(2)
            print("Este é o ponto de não-retorno.")
            time.sleep(2)
            print("Você sente o peso de toda a história respirando nas sombras da masmorra.")
            time.sleep(2)
            print("\n🎭 Mas a verdade é simples...")
            time.sleep(2)
            print("Herói ou condenado.")
            time.sleep(1)
            print("Lendário ou esquecido.")
            time.sleep(1)
            print("Você precisa de um nome.")
            time.sleep(4)
            print("\n⚔️  Diga-me...")
            time.sleep(1)
            print("\nQual")
            time.sleep(1)
            print("é")
            time.sleep(1)
            print("seu")
            time.sleep(1)
            print("verdadeiro")
            time.sleep(1)
            print("nome?")
            time.sleep(2)
            break
            
        elif skip == "sim":
            print("\n⏭️  Prólogo pulado!")
            break
        else:
            print("\n⚠️  Digite 'sim' ou 'nao'!")
            time.sleep(1)


def _obter_nome_jogador():
    """Solicita nome do jogador com validação."""
    while True:
        nome = input("\nDigite seu nome: ").strip()

        if len(nome) <= NOME_MINIMO:
            print(f"⚠️  Nome inválido! O nome deve ter mais de {NOME_MINIMO} letras.")
            time.sleep(1)
        else:
            print(f"\n✅ Bem-vindo, {nome}!")
            print("Boa sorte aventureiro... sua aventura começa agora!")
            time.sleep(2)
            return nome


def _explorar_masmorr(nome, player):
    """
    Laço principal de exploração da masmorra.
    Jogador encontra diferentes tipos de salas aleatoriamente.
    
    Tipos de sala:
    - 60%: Salas de combate com goblins
    - 20%: Salas com baús de tesouro
    - 12%: Salas com fontes de cura
    - 8%: Salas de venda (RARA)
    """
    salas_exploradas = 0
    
    while player.esta_vivo():
        salas_exploradas += 1
        print(f"\n{'='*60}")
        print(f"SALA {salas_exploradas}")
        print(f"{'='*60}")
        print(f"Vida: {player.vida}/{player.vida_maxima} | Inventário: {len(player.inventario)} itens")
        
        # Gerar sala aleatória
        sala = gerar_sala_aleatoria()
        
        # Executar a sala
        if isinstance(sala, SalaCombate):
            # Sala de combate
            resultado = encontro_combate(nome, player, sala.goblin, sala.descricao)
            
            if resultado == "vitoria":
                print(f"\n✅ Após uma longa luta aonde sua pobre e vazia vida foi posta em riscos desnecessarios por talvez algo que voce nunca con siga por suas sujas maos, te restam apenas {player.vida} HP")
                print("\nSeus pés rastejam adiante na masmorra...")
                time.sleep(2)
                
            elif resultado == "derrota":
                print(f"\n💀 Você foi derrotado na sala {salas_exploradas}.")
                print(f"Você conquistou: {salas_exploradas - 1} salas")
                print(f"Experiência acumulada: {player.experiencia}")
                return
                
            elif resultado == "fugiu":
                print(f"\n🏃 Você fugiu da masmorra após explorar {salas_exploradas} salas.")
                print(f"Experiência acumulada: {player.experiencia}")
                return
        
        elif isinstance(sala, SalaTesourou):
            # Sala com baú
            sala.executar(player)
            print("\nVocê continua sua jornada...")
            time.sleep(1)
        
        elif isinstance(sala, SalaCura):
            # Sala com cura
            sala.executar(player)
            print("\nVocê continua sua jornada...")
            time.sleep(1)
        
        elif isinstance(sala, SalaVenda):
            # Sala de venda (rara!)
            print("\n🎉 WOW! parece que padomay está ao seu lado aventureiro, voce encontra uma pobre alma posta sobre escombross")
            print("a pobre alma abre suas maos segurando alguns itens")
            sala.executar(player)
            print("\nVocê continua sua jornada...")
            time.sleep(1)
    
    print(f"\n💀 Você morreu na sala {salas_exploradas}!")


if __name__ == "__main__":
    start_game()
    
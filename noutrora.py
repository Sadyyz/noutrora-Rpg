import random
import time
from batalhas import encontro_combate
from player import Player
from goblin import criar_goblin_aleatorio
from salas import gerar_sala_aleatoria, SalaCombate, SalaTesourou, SalaCura, SalaVenda
from config import NOME_MINIMO


def start_game():
    """Controlador principal do jogo. Gerencia o fluxo narrativo e exploração."""
    
    # ========== FASE 1: PRÓLOGO ==========
    _exibir_prologo()

    # ========== FASE 2: CRIAR JOGADOR ==========
    nome = _obter_nome_jogador()
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
                + "\n\nA chuva caía violentamente sobre os telhados de Stormcloak naquela noite."
            )
            time.sleep(3)
            print(
                "O pequeno vilarejo, conhecido por seus ferreiros e comerciantes de armas, "
                "parecia mais silencioso do que o normal. As poucas pessoas que ainda caminhavam "
                "pelas ruas evitavam olhar umas para as outras, como se algo ruim estivesse prestes "
                "a acontecer."
            )
            time.sleep(8)
            print("Você cresceu naquele lugar...")
            time.sleep(2)
            print(
                "Filho de uma família de artesãos, passou a maior parte da vida ajudando na forja "
                "e ouvindo histórias sobre aventureiros, monstros e ruínas esquecidas pelo reino. "
                "Histórias que pareciam absurdas… até agora."
            )
            time.sleep(8)
            print(
                "Enquanto organizava algumas mercadorias antigas da oficina, seus olhos encontraram "
                "um jornal amassado da Guilda dos Aventureiros."
            )
            time.sleep(6)
            print("\nEm destaque, uma manchete chamava atenção:")
            print(">>> A Masmorra de Noutrora volta a emitir sinais de atividade após décadas <<<")
            time.sleep(7)
            print(
                "Diziam que Noutrora era uma masmorra amaldiçoada localizada nas profundezas das "
                "montanhas ao norte. Muitos aventureiros entraram naquele lugar em busca de riqueza, "
                "fama ou respostas… mas poucos retornaram."
            )
            time.sleep(5)
            print("\nE os que voltaram jamais foram os mesmos.")
            time.sleep(2)
            print(
                "Naquela mesma noite, tomado pela curiosidade — ou talvez por algo pior — você "
                "decide preparar seu equipamento e partir em direção às montanhas."
            )
            time.sleep(5)
            print(
                "O vento gelado sopra contra seu rosto enquanto a enorme entrada da masmorra "
                "surge diante de você."
            )
            time.sleep(5)
            print("\nSua jornada começa agora.")
            time.sleep(2)
            print("Mas... não existe herói sem nome...")
            time.sleep(2)
            print("Não é mesmo?")
            time.sleep(4)
            print("\nMe diga...")
            time.sleep(1)
            print("\nQual")
            time.sleep(1)
            print("é")
            time.sleep(1)
            print("o")
            time.sleep(1)
            print("seu")
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
    
# ============================================================================
# SISTEMA DE COMBATE INTERATIVO
# ============================================================================
# O jogador escolhe suas ações a cada turno.
# Fluxo: Exibir status → Jogador escolhe ação → Executar ação → Goblin reage

import time
import random
from config import VARIACAO_DANO


def calcular_dano(forca):
    """
    Calcula dano baseado em força + variação aleatória.
    
    Args:
        forca (int): Força do atacante
        
    Returns:
        int: Dano total (força + 0 a VARIACAO_DANO)
    """
    return forca + random.randint(0, VARIACAO_DANO)


def determinar_iniciativa(velocidade_player, velocidade_goblin):
    """
    Determina quem ataca primeiro baseado em velocidade.
    
    Args:
        velocidade_player (int): Velocidade do jogador
        velocidade_goblin (int): Velocidade do goblin
        
    Returns:
        bool: True se jogador é mais rápido, False se goblin é mais rápido
    """
    return velocidade_player >= velocidade_goblin


def exibir_status_combate(player, goblin, numero_turno):
    """Exibe o status atual do combate."""
    forca_player = player.obter_forca_total()
    velocidade_player = player.obter_velocidade_total()
    
    print(f"\n{'='*60}")
    print(f"TURNO {numero_turno}")
    print(f"{'='*60}")
    print(f"\n👤 {player.nome}:")
    print(f"   Vida: {player.vida}/{player.vida_maxima} HP")
    print(f"   Força: {forca_player} | Velocidade: {velocidade_player}")
    if player.arma_equipada:
        print(f"   🗡️  Arma: {player.arma_equipada.nome}")
    print(f"\n⚔️  {goblin.obter_status()['tipo']}:")
    print(f"   Vida: {goblin.vida}/{goblin.vida_maxima} HP")
    print(f"   Força: {goblin.forca} | Velocidade: {goblin.velocidade}")


def obter_acao_jogador(player):
    """
    Solicita a ação do jogador no turno.
    
    Args:
        player (Player): O jogador
        
    Returns:
        str: Ação escolhida ("atacar", "defender", "usar_item", "fugir")
    """
    while True:
        print(f"\n{'='*60}")
        print("SUAS AÇÕES:")
        print(f"{'='*60}")
        print(f"[1] Atacar")
        print(f"[2] Defender")
        if player.inventario:
            print(f"[3] Usar Item ({len(player.inventario)} itens)")
        print(f"[4] Fugir")
        
        opcao = input("\nO que fazer? ").strip()
        
        if opcao == "1":
            return "atacar"
        elif opcao == "2":
            return "defender"
        elif opcao == "3" and player.inventario:
            return "usar_item"
        elif opcao == "4":
            return "fugir"
        else:
            print("⚠️  Opção inválida!")


def processar_acao_jogador(player, goblin, acao):
    """
    Processa a ação escolhida pelo jogador.
    
    Args:
        player (Player): O jogador
        goblin (Goblin): O goblin
        acao (str): Ação ("atacar", "defender", "usar_item", "fugir")
        
    Returns:
        str: Resultado ("atacar", "defender", "fugiu", "usar_item")
    """
    if acao == "atacar":
        forca_player = player.obter_forca_total()  # COM BÔNUS
        dano = calcular_dano(forca_player)
        goblin.tomar_dano(dano)
        print(f"\n⚔️  Você atacou com força!")
        print(f"💥 Causou {dano} de dano ao {goblin.obter_status()['tipo'].lower()}!")
        time.sleep(1)
        return "atacou"
    
    elif acao == "defender":
        print(f"\n🛡️  Você se posiciona defensivamente!")
        print(f"A próxima defesa reduzirá o dano...")
        time.sleep(1)
        return "defendeu"
    
    elif acao == "usar_item":
        print(f"\n{player.listar_inventario()}")
        try:
            indice = int(input("Qual item usar? ").strip())
            resultado = player.usar_item(indice)
            print(f"✨ {resultado}")
            time.sleep(1)
        except ValueError:
            print("⚠️  Digite um número válido!")
        return "usou_item"
    
    elif acao == "fugir":
        chance_fuga = random.randint(1, 100)
        if chance_fuga > 50:
            print(f"\n🏃 Você correu para fora da batalha!")
            time.sleep(1)
            return "fugiu"
        else:
            print(f"\n❌ Você não conseguiu fugir!")
            print(f"O inimigo bloqueia o caminho!")
            time.sleep(1)
            return "falhou_fuga"


def executar_turno_interativo(player, goblin, numero_turno):
    """
    Executa um turno completo e interativo de combate.
    
    Args:
        player (Player): O jogador
        goblin (Goblin): O goblin
        numero_turno (int): Número do turno atual
        
    Returns:
        tuple: (resultado, continua_combate)
               resultado: "vitoria", "derrota", "fugiu"
               continua_combate: bool
    """
    exibir_status_combate(player, goblin, numero_turno)
    
    # ========== AÇÃO DO JOGADOR ==========
    acao_jogador = obter_acao_jogador(player)
    resultado_acao = processar_acao_jogador(player, goblin, acao_jogador)
    
    # Se tentou fugir
    if resultado_acao == "fugiu":
        return "fugiu", False
    
    # Se falhou na fuga, continua o combate
    if resultado_acao == "falhou_fuga":
        pass  # Continua para reação do goblin
    
    # Verificar se goblin morreu
    if not goblin.esta_vivo():
        print(f"\n🎉 Vitória! Você derrotou o {goblin.obter_status()['tipo'].lower()}!")
        player.ganhar_experiencia(50)
        time.sleep(2)
        return "vitoria", False
    
    # ========== REAÇÃO DO GOBLIN ==========
    print(f"\n{'='*60}")
    print("REAÇÃO DO INIMIGO")
    print(f"{'='*60}")
    
    # Goblin escolhe atacar ou tentar fugir (50/50)
    if random.randint(1, 2) == 1:
        # Goblin ataca
        dano = calcular_dano(goblin.forca)
        
        # Se player defendeu, reduz dano
        if resultado_acao == "defendeu":
            dano = int(dano * 0.5)
            print(f"\n🛡️  Sua defesa foi eficaz!")
        
        player.tomar_dano(dano)
        print(f"\n💥 O {goblin.obter_status()['tipo'].lower()} te atacou!")
        print(f"🤕 Você recebeu {dano} de dano!")
    else:
        print(f"\n😈 O {goblin.obter_status()['tipo'].lower()} estranha em sua posição de combate...")
        print(f"Ambos se observam cautelosamente...")
    
    time.sleep(1)
    
    # Verificar se player morreu
    if not player.esta_vivo():
        print(f"\n💀 Você foi derrotado!")
        time.sleep(2)
        return "derrota", False
    
    return "em_andamento", True


def encontro_combate(nome, player, goblin, cenario_text):
    """
    Controlador de um encontro de combate.
    Permite o jogador batalhar ou correr antes de combate.
    
    Args:
        nome (str): Nome do jogador
        player (Player): O jogador
        goblin (Goblin): O goblin
        cenario_text (str): Descrição do cenário
        
    Returns:
        str: "vitoria", "derrota", "fugiu"
    """
    print(f"\n{cenario_text}")
    time.sleep(2)
    print(f"\n⚠️  {goblin.obter_status()['tipo']} aparece das sombras!")
    time.sleep(2)
    
    # Menu pré-combate
    while True:
        print("\n" + "=" * 50)
        print("[1] Entrar em Combate")
        print("[2] Tentar Fugir")
        print("=" * 50)
        
        opcao = input(f"\n{nome}, qual será sua decisão? ").strip()
        
        if opcao == "1":
            # Iniciar combate
            print("\n" + "=" * 60)
            print("⚔️  UM DUELO SE APROXIMA!")
            print("=" * 60)
            time.sleep(2)
            
            # Combate interativo
            numero_turno = 1
            while player.esta_vivo() and goblin.esta_vivo():
                resultado, continua = executar_turno_interativo(player, goblin, numero_turno)
                
                if not continua:
                    return resultado
                
                numero_turno += 1
                input("\nPressione ENTER para continuar...")
        
        elif opcao == "2":
            # Tentar fugir ANTES de combate
            chance_fuga = random.randint(1, 100)
            if chance_fuga > 40:
                print("\n✅ Você conseguiu fugir com sucesso!")
                time.sleep(1)
                return "fugiu"
            else:
                print("\n❌ Você não conseguiu fugir! O combate é inevitável!")
                print("Você será forçado a lutar...")
                time.sleep(2)
                # Volta ao loop para iniciar combate
        
        else:
            print("\n⚠️  Opção inválida!")
                
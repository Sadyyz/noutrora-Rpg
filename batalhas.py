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
    """Exibe o status atual do combate com descrições imersivas."""
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
    print(f"\n🔴 O que você vê:")
    print(f"   {goblin.descrever_visualmente()}")



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
        if player.nome == "Metamorfo":
            print("2 - Usar Essência")
        elif player.nome == "Druida":
            print("2 - Envenenar")
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
        
        # Descrições cinematográficas variadas
        ataques = [
            f"⚔️  Você avança com toda sua força! Sua arma corta o ar com um assobio de morte.",
            f"⚔️  Um grito de batalha sai de seus pulmões enquanto você se lança para o ataque!",
            f"⚔️  Você vê uma abertura e ataca com tudo que tem!",
            f"⚔️  Seus músculos ardem enquanto você executa o golpe!",
        ]
        print(f"\n{random.choice(ataques)}")
        print(f"💥 IMPACTO! Você causou {dano} de dano devastador ao {goblin.obter_status()['tipo'].lower()}!")
        
        if goblin.vida <= 0:
            print(f"🩸 A criatura grita de agonia, seu sangue banhando o chão!")
        else:
            print(f"🩸 Ferimento aberto! O {goblin.obter_status()['tipo'].lower()} rosna de dor!")
        
        time.sleep(1)
        return "atacou"
    
    elif acao == "defender":
        print(f"\n🛡️  Você se posiciona defensivamente, elevando sua guarda!")
        print(f"Seu corpo se tensa... você está pronto para qualquer ataque.")
        print(f"A defesa reduzirá significativamente o dano do próximo golpe!")
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
            print(f"\n🏃 Seus instintos de sobrevivência explodem! Você se vira e CORRE!")
            print(f"Você consegue abrir espaço e desaparece pela escuridão da masmorra!")
            time.sleep(1)
            return "fugiu"
        else:
            print(f"\n❌ Você tenta fugir desesperadamente!")
            print(f"😈 Mas a criatura é mais rápida! Ela bloqueia seu caminho com um rosnado aterrorizante!")
            print(f"Você está preso aqui. Não há escapatória.")
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
            print(f"\n🛡️  Sua defesa foi eficaz! Você bloqueia o golpe, reduzindo o impacto!")
        
        player.tomar_dano(dano)
        
        # Descrições variadas do ataque do goblin
        ataques_goblin = [
            f"O {goblin.obter_status()['tipo'].lower()} solta um grito ensurdecedor e avança como uma besta acuada!",
            f"A criatura se move com velocidade aterradora, seus olhos brilhando de pura malevolência!",
            f"O {goblin.obter_status()['tipo'].lower()} salta para o ataque com garras estendidas!",
            f"Um rosnado primitivo ecoa enquanto o inimigo executa seu contra-ataque!",
        ]
        print(f"\n😈 {random.choice(ataques_goblin)}")
        print(f"💥 BAQUE! Você sente o impacto devastador!")
        print(f"🤕 Você recebeu {dano} de dano! Sangue quente escorre pelo seu corpo...")
    else:
        print(f"\n😈 O {goblin.obter_status()['tipo'].lower()} parece ponderar seu próximo movimento...")
        print(f"A criatura rosna baixo, avaliando suas opções. Ambos respiram pesadamente.")
        print(f"O silêncio é absoluto, exceto pelo seu coração acelerado.")

    
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
    print(f"\n⚠️  ENCONTRO! {goblin.obter_status()['tipo']} aparece das sombras!")
    print(f"\n{goblin.descrever_visualmente()}")
    time.sleep(2)
    
    # Menu pré-combate
    while True:
        print("\n" + "=" * 60)
        print("[1] ⚔️  Entrar em Combate")
        print("[2] 🏃 Tentar Fugir Agora")
        print("=" * 60)
        
        opcao = input(f"\n{nome}, qual será sua decisão? ").strip()
        
        if opcao == "1":
            # Iniciar combate
            print("\n" + "=" * 60)
            print("⚔️  UM DUELO À MORTE COMEÇA!")
            print("As garras se esticam. Os olhos brilham. Não há volta agora.")
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
                
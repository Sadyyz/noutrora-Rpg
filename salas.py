# ============================================================================
# SISTEMA DE SALAS
# ============================================================================
# Define diferentes tipos de salas que o jogador pode encontrar.

import random
from items import gerar_loot_aleatorio, gerar_multiplos_itens


class Sala:
    """Classe base para salas na masmorra."""
    
    def __init__(self, tipo, descricao):
        self.tipo = tipo  # "combate", "tesouro", "cura", "venda"
        self.descricao = descricao
    
    def executar(self, player):
        """
        Executa a lógica da sala.
        
        Args:
            player (Player): O jogador
            
        Returns:
            str: Resultado da sala ("continua", "morte", "fugiu")
        """
        raise NotImplementedError


class SalaCombate(Sala):
    """Sala com um inimigo para combater."""
    
    def __init__(self, goblin, descricao):
        super().__init__("combate", descricao)
        self.goblin = goblin
    
    def executar(self, player):
        """Retorna o goblin para iniciar combate."""
        return self.goblin


class SalaTesourou(Sala):
    """Sala com um baú contendo itens."""
    
    def __init__(self, descricao, quantidade_itens=3):
        super().__init__("tesouro", descricao)
        self.itens = gerar_multiplos_itens(quantidade_itens)
    
    def executar(self, player):
        """Abre o baú e oferece itens ao jogador."""
        print(f"\n{'='*60}")
        print("✨ Você encontrou um baú brilhante!")
        print(f"{'='*60}")
        print(f"\n{self.descricao}\n")
        
        print(f"\nItens no baú:")
        for i, item in enumerate(self.itens):
            print(f"  [{i}] {item}")
        
        print(f"\n[{len(self.itens)}] Pegar todos")
        print(f"[{len(self.itens) + 1}] Não pegar nada")
        
        import time
        while True:
            try:
                opcao = int(input("\nQual item deseja? ").strip())
                
                if 0 <= opcao < len(self.itens):
                    item = self.itens.pop(opcao)
                    player.adicionar_item(item)
                    print(f"\n✅ Você adicionou {item} ao inventário!")
                    time.sleep(1)
                    return "continua"
                
                elif opcao == len(self.itens):
                    # Pegar todos
                    for item in self.itens:
                        player.adicionar_item(item)
                    print(f"\n✅ Você pegou todos os itens!")
                    time.sleep(1)
                    return "continua"
                
                elif opcao == len(self.itens) + 1:
                    print(f"\nVocê deixou o baú para trás...")
                    time.sleep(1)
                    return "continua"
                
                else:
                    print(f"\n⚠️  Opção inválida!")
            
            except ValueError:
                print(f"\n⚠️  Digite um número válido!")


class SalaCura(Sala):
    """Sala com uma fonte mágica de cura."""
    
    def __init__(self, descricao, cura_total=50):
        super().__init__("cura", descricao)
        self.cura_total = cura_total
    
    def executar(self, player):
        """Oferece cura ao jogador."""
        print(f"\n{'='*60}")
        print("💧 Você encontrou uma fonte mágica!")
        print(f"{'='*60}")
        print(f"\n{self.descricao}\n")
        
        print(f"\nSua vida atual: {player.vida}/{player.vida_maxima}")
        
        import time
        while True:
            print(f"\n[1] Beber da fonte (cura {self.cura_total})")
            print(f"[2] Continuar")
            
            opcao = input("\nO que fazer? ").strip()
            
            if opcao == "1":
                cura_real = player.curar(self.cura_total)
                print(f"\n✅ Você foi curado em {cura_real} pontos!")
                print(f"Vida atual: {player.vida}/{player.vida_maxima}")
                time.sleep(1)
                return "continua"
            
            elif opcao == "2":
                print(f"\nVocê continua sua jornada...")
                time.sleep(1)
                return "continua"
            
            else:
                print(f"\n⚠️  Opção inválida!")


class SalaVenda(Sala):
    """Sala com um vendedor (RARA!)."""
    
    def __init__(self, descricao):
        super().__init__("venda", descricao)
        self.itens_venda = gerar_multiplos_itens(5)  # Sempre 5 itens
    
    def executar(self, player):
        """Oferece itens para venda."""
        print(f"\n{'='*60}")
        print("🛍️  Um misterioso vendedor aparece!")
        print(f"{'='*60}")
        print(f"\n{self.descricao}\n")
        
        import time
        while True:
            print(f"\nItens à venda:")
            for i, item in enumerate(self.itens_venda):
                print(f"  [{i}] {item}")
            
            print(f"\n[{len(self.itens_venda)}] Sair")
            
            try:
                opcao = int(input("\nQual item deseja comprar? ").strip())
                
                if 0 <= opcao < len(self.itens_venda):
                    item = self.itens_venda.pop(opcao)
                    player.adicionar_item(item)
                    print(f"\n✅ Você comprou {item}!")
                    time.sleep(1)
                    
                    if opcao == len(self.itens_venda):
                        return "continua"
                
                elif opcao == len(self.itens_venda):
                    print(f"\n👋 O vendedor desaparece nas sombras...")
                    time.sleep(1)
                    return "continua"
                
                else:
                    print(f"\n⚠️  Opção inválida!")
            
            except ValueError:
                print(f"\n⚠️  Digite um número válido!")


# ============================================================================
# GERADOR DE SALAS ALEATÓRIAS
# ============================================================================

DESCRICOES_COMBATE = [
    "Um corredor barulhento onde você se depara com inimigos",
    "Uma sala coberta por corpos antigos onde aparecem criadores",
    "Um corredor inundado até seus joelhos onde algo observa você",
    "Uma biblioteca abandonada onde livros se movem sozinhos",
    "Uma capela destruída iluminada apenas por velas vermelhas",
    "Um túnel estreito onde sons de correntes ecoam",
    "Uma sala silenciosa demais onde você encontra inimigos olhando fixamente",
    "Um corredor cheio de símbolos estranhos onde criaturas aparecem",
    "Uma ponte quebrada sobre um abismo sem fim",
    "Uma sala completamente escura onde apenas olhos podem ser vistos",
]

DESCRICOES_TESOURO = [
    "Uma câmara dourada com ouro e joias brilhando",
    "Um cofre antigo repleto de relíquias esquecidas",
    "Uma caverna cristalina onde itens mágicos pulsam com luz",
    "Uma câmara subterrânea com a riqueza de um reino",
]

DESCRICOES_CURA = [
    "Uma gruta com uma fonte de água cristalina que brilha",
    "Um santuário antigo com uma aura de poder curativo",
    "Um oásis mágico que emana paz e cura",
]

DESCRICOES_VENDA = [
    "Uma tenda misteriosa aparece do nada com itens raros",
    "Um viajante misterioso oferece seus melhores itens",
    "Uma boutique interdimensional cheia de artefatos mágicos",
]


def gerar_sala_aleatoria(goblin=None):
    """
    Gera uma sala aleatória.
    Distribuição: 60% combate, 20% tesouro, 12% cura, 8% venda
    
    Args:
        goblin (Goblin): Goblin para sala de combate (se necessário)
        
    Returns:
        Sala: Uma sala gerada aleatoriamente
    """
    probabilidade = random.randint(1, 100)
    
    if probabilidade <= 60:  # 60% combate
        from goblin import criar_goblin_aleatorio
        if goblin is None:
            goblin = criar_goblin_aleatorio()
        descricao = random.choice(DESCRICOES_COMBATE)
        return SalaCombate(goblin, descricao)
    
    elif probabilidade <= 80:  # 20% tesouro
        descricao = random.choice(DESCRICOES_TESOURO)
        return SalaTesourou(descricao, quantidade_itens=random.randint(2, 4))
    
    elif probabilidade <= 92:  # 12% cura
        descricao = random.choice(DESCRICOES_CURA)
        return SalaCura(descricao, cura_total=random.randint(30, 60))
    
    else:  # 8% venda (RARA!)
        descricao = random.choice(DESCRICOES_VENDA)
        return SalaVenda(descricao)

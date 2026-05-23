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
    "Um corredor úmido onde a umidade cola na sua pele. O ar está pesado, fétido, carregado de podridão. Seus passos ecoam e então... silêncio absoluto. Você ouve um rosnado baixo, gutural. Uma forma se move nas sombras. Os olhos brilham em vermelho — uma criatura com dentes que são pura inteligência predatória.",
    "Uma câmara ossária. Crânios e ossos cobrem o chão em camadas compactadas. O cheiro é insuportável — morte antiga fermentando em eternidade. Uma vela fantasmagórica ilumina as paredes, e você vê marcas de garras recentes. Algo respirando pesadamente ecoado pelas órbitas vazias dos crânios ao seu redor.",
    "Um corredor inundado. Água preta como breu até seus joelhos. Algo toca sua perna — não é óbvio se é alga ou... dedos. A água emite um brilho fosforescente mórbido. Você vê uma silhueta anfíbia emergir, com pele escamosa que não deveria existir, pronta para arrancar sua garganta.",
    "Uma biblioteca maldita. Livros flutuam lentamente no ar, suas páginas virando sozinhas. A temperatura caiu 20 graus. Você respira vapor. As prateleiras rangem, e entre os corredores de livros, uma criatura grotesca com múltiplos olhos observa você, seu corpo se contorcendo de forma que desafia anatomia.",
    "Uma capela em ruínas. Velas vermelhas criam sombras dançantes nas paredes. Há um altar com símbolos sangrentos ainda frescos. Uma entidade de proporções humanoides emerge das sombras — seus olhos brilham com malevolência ancestral, e você sente a frieza de um milhão de mortes irradiando de seu corpo.",
    "Um túnel de correntes. O barulho metálico é ensurdecedor. As correntes seguram coisas — você vê entalhes de garras nas paredes, sangue escuro que não deveria estar tão fresco. A temperatura flutua erraticamente. Uma criatura se move ritmicamente, suas correntes tilintando enquanto se aproxima, seu rosto uma mistura de dor e fúria destrutiva.",
    "Uma sala de silêncio absoluto. Nem uma mosca. Nem ar. Você quase ouve seu coração explodindo. Então você vê olhos luminosos, dúzias deles, flutuando nas sombras. Um sussurro antigo ecoa diretamente em sua mente. A criatura não faz som quando se move, mas sente sua presença em cada nervo.",
    "Um corredor de símbolos primitivos. Eles cobrem as paredes em linhas de sangue. Você sente os símbolos pulsarem de forma sinistra. O ar zumbe com uma frequência que dói. Uma coisa com pele que não tem cores naturais emerge, com símbolos brilhando em seu corpo — uma encarnação do ritual antigo.",
    "Uma ponte quebrada sobre um vazio sem fundo. Você sente a gravidade se comportando estranho aqui. No meio da ponte, uma criatura aguarda — sua forma flutua entre dimensões, seus membros não têm ângulos normais, e sua respiração distorce o espaço ao redor.",
    "Uma caverna sem luz. Você está literalmente cego. Mas pode ouvir — respiração úmida, movimento lento, o som de algo que não deveria conseguir se locomover daquela forma. Seus olhos gradualmente se ajustam e vê uma silhueta impossível, seus órgãos vibrando com uma frequência que causa nauseia.",
]

DESCRICOES_TESOURO = [
    "Uma câmara dourada onde ouro e joias cobrem o chão. Mas há algo errado — o ouro não é quente, é gelado. As joias pulsam com uma luz que não deveria ser natural. Você sente que está sendo observado. Os itens parecem vibrar quando você toca, como se tivessem uma vontade própria. Alguém... algo... perdeu essa riqueza há muito tempo e ainda a guarda.",
    "Um cofre antigo com relíquias de civilizações esquecidas. Os itens estão dispostos cerimonialmente. Você encontra moedas de metal que não reconhece, artefatos com símbolos que queimam sua mente apenas por olhá-los. Uma neblina pairava sobre o tesouro. Você jura que viu algo se mover entre os objetos.",
    "Uma caverna cristalina onde itens mágicos pulsam com luz azulada. Os cristais refletem seu rosto em ângulos errados. O ar aqui hum com poder antigo. Os itens parecem estar presos em cristal parcialmente — como se foram preservados de propósito, ou aprisionados. Sua mão treme quando você se aproxima.",
    "Uma câmara subterrânea com riqueza de um reino perdido. Moedas, joias, armas forjadas de metal impossível. Mas cada item tem marcas de sangue velho. A riqueza está em uma pirâmide, e no topo há um trono vazio. Você sente o peso de milhões de miradas mortas nesta câmara, todas olhando para você, esperando.",
]

DESCRICOES_CURA = [
    "Uma gruta com uma fonte de água cristalina. A água brilha levemente, e a temperatura é perfeita. Mas quando você se aproxima, sente que a água não está vazando — está sendo contida por algo invisível. Você bebe, e por um momento pode sentir as feridas cicatrizarem. Porém, você também sente uma presença na água, como se algo antigo e sábio dormisse em suas profundezas.",
    "Um santuário antigo com uma aura de poder curativo. Símbolos sagrados cobrem as paredes. Você se sente seguro aqui... mas há um preço. Pela primeira vez desde entrar na masmorra, você sente que está sendo julgado. As lesões curam, mas você jura que pode ouvir sussurros de agradecimento de outras almas curadas neste lugar.",
    "Um oásis subterrâneo que emana paz. A água é morna e reconfortante. Flores iluminescem suavemente. Mas algo não é natural — as flores crescem em padrões geométricos perfeitos, como se cultivadas com propósito. Você é curado, mas quando você se afasta, vê seu reflexo na água por um instante — e não está sozinho no reflexo.",
]

DESCRICOES_VENDA = [
    "Uma tenda emerge da neblina — você tem certeza que não estava aqui segundos atrás. Dentro, um vendedor que você não consegue ver muito bem, seu rosto sempre na sombra mesmo com luz ao redor. Seus dedos são longos demais. Ele sorri, revelando dentes que não deveriam caber em uma boca humana. Seus itens emitem um brilho que causa incômodo. Você sente que está fazendo uma negociação com algo que não deveria estar neste reino.",
    "Um viajante em um beco lateral. Seu capuz oscila, e você não consegue ver seu rosto. Seus itens estão dispostos sobre um tecido negro que parece absorver luz. Quando você toca um item, o vendedor se mexe — rápido demais, sua postura errada. Você jura que ele pisca em três lugares simultâneos. Ele oferece seus melhores itens, mas você sente que o preço pode ser muito mais do que moeda.",
    "Uma loja impossível em uma parede da masmorra. Como ela está ali? As dimensões não fazem sentido. Dentro, artefatos brilham suspensos no ar. O vendedor é uma figura feita de luz e sombra, seu corpo nunca descansando em uma forma definida. Os itens aqui foram pertencer a pessoas que você jura reconhecer dos livros de história há séculos. Ele oferece preços baixos, mas pergunta questões que revelam seus medos mais profundos.",
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

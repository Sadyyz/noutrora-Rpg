# ============================================================================
# NOUTRORA RPG — SISTEMA DE SALAS
# ============================================================================

import random
import time
from items import gerar_loot_aleatorio, gerar_multiplos_itens


class Sala:
    def __init__(self, tipo, descricao):
        self.tipo      = tipo
        self.descricao = descricao

    def executar(self, player):
        raise NotImplementedError


class SalaCombate(Sala):
    def __init__(self, goblin, descricao):
        super().__init__("combate", descricao)
        self.goblin = goblin

    def executar(self, player):
        return self.goblin


class SalaTesourou(Sala):
    def __init__(self, descricao, quantidade_itens=3):
        super().__init__("tesouro", descricao)
        self.itens = gerar_multiplos_itens(quantidade_itens)

    def executar(self, player):
        print(f"\n{'='*60}")
        print("  BAU ENCONTRADO")
        print(f"{'='*60}")
        print(f"\n  {self.descricao}\n")

        print("  Itens:")
        for i, item in enumerate(self.itens):
            print(f"    [{i}] {item}")
        print(f"    [{len(self.itens)}] Pegar todos")
        print(f"    [{len(self.itens)+1}] Deixar para trás")

        while True:
            try:
                op = int(input("\n  >> ").strip())
                if 0 <= op < len(self.itens):
                    item = self.itens.pop(op)
                    player.adicionar_item(item)
                    print(f"\n  Pegou: {item}")
                    time.sleep(1)
                    return "continua"
                elif op == len(self.itens):
                    for item in self.itens:
                        player.adicionar_item(item)
                    print(f"\n  Pegou tudo.")
                    time.sleep(1)
                    return "continua"
                elif op == len(self.itens) + 1:
                    print("\n  Você deixa o baú para trás.")
                    time.sleep(1)
                    return "continua"
                else:
                    print("  Opção inválida.")
            except ValueError:
                print("  Número inválido.")


class SalaCura(Sala):
    def __init__(self, descricao, cura_total=50):
        super().__init__("cura", descricao)
        self.cura_total = cura_total

    def executar(self, player):
        print(f"\n{'='*60}")
        print("  FONTE MAGICA")
        print(f"{'='*60}")
        print(f"\n  {self.descricao}")
        print(f"\n  Vida atual: {player.vida}/{player.vida_maxima}")

        while True:
            print(f"\n  [1] Beber  (+{self.cura_total} HP)")
            print(f"  [2] Continuar")
            op = input("\n  >> ").strip()
            if op == "1":
                real = player.curar(self.cura_total)
                print(f"\n  +{real} HP.  Vida: {player.vida}/{player.vida_maxima}")
                time.sleep(1)
                return "continua"
            elif op == "2":
                print("\n  Você continua.")
                time.sleep(1)
                return "continua"
            else:
                print("  Opção inválida.")


class SalaVenda(Sala):
    def __init__(self, descricao):
        super().__init__("venda", descricao)
        self.itens_venda = gerar_multiplos_itens(5)

    def executar(self, player):
        print(f"\n{'='*60}")
        print("  VENDEDOR MISTERIOSO")
        print(f"{'='*60}")
        print(f"\n  {self.descricao}")

        while True:
            print(f"\n  Gold: {player.dinheiro}")
            print("  À venda:")
            for i, item in enumerate(self.itens_venda):
                print(f"    [{i}] {item}  (30 gold)")
            print(f"    [{len(self.itens_venda)}] Sair")

            try:
                op = int(input("\n  >> ").strip())
                if 0 <= op < len(self.itens_venda):
                    if player.remover_dinheiro(30):
                        item = self.itens_venda.pop(op)
                        player.adicionar_item(item)
                        print(f"\n  Comprou: {item}")
                        time.sleep(1)
                        if not self.itens_venda:
                            print("\n  Estoque esgotado.")
                            break
                    else:
                        print("\n  Gold insuficiente.")
                elif op == len(self.itens_venda):
                    print('\n  O vendedor some nas sombras.')
                    time.sleep(1)
                    return "continua"
                else:
                    print("  Opção inválida.")
            except ValueError:
                print("  Número inválido.")


# --------------------------------------------------------------------------
# DESCRIÇÕES ATMOSFÉRICAS
# --------------------------------------------------------------------------

DESCRICOES_COMBATE = [
    "Um corredor úmido onde a umidade cola na sua pele. O ar está pesado, fétido. Você ouve um rosnado baixo. Os olhos brilham em vermelho.",
    "Uma câmara ossária. Crânios cobrem o chão em camadas. O cheiro é insuportável. Uma vela ilumina as paredes — marcas de garras recentes.",
    "Um corredor inundado. Água preta como breu até os joelhos. Algo toca sua perna. A água emite brilho fosforescente. Uma silhueta emerge.",
    "Uma biblioteca maldita. Livros flutuam no ar. A temperatura caiu. Você respira vapor. Entre as prateleiras, algo com múltiplos olhos observa.",
    "Uma capela em ruínas. Velas vermelhas. Altar com símbolos sangrentos ainda frescos. Uma entidade emerge das sombras — olhos que pesam séculos.",
    "Um túnel de correntes. Barulho metálico ensurdecedor. Correntes seguram coisas. Sangue escuro fresco nas paredes. Algo se aproxima.",
    "Uma sala de silêncio absoluto. Nem uma mosca. Olhos luminosos flutuam nas sombras. Um sussurro ecoa diretamente em sua mente.",
    "Um corredor de símbolos primitivos em sangue. O ar zumbe em frequência dolorosa. Uma coisa com pele sem cores naturais emerge.",
    "Uma ponte quebrada sobre vazio sem fundo. A gravidade se comporta errado. Uma criatura aguarda no meio — sua forma flutua entre dimensões.",
    "Uma caverna sem luz. Você está cego. Mas pode ouvir — respiração úmida. Uma silhueta impossível. Órgãos vibrando em frequência nauseante.",
]

DESCRICOES_TESOURO = [
    "Uma câmara dourada onde ouro e joias cobrem o chão. Mas o ouro é gelado. As joias pulsam com luz antinatural.",
    "Um cofre antigo com relíquias de civilizações esquecidas. Moedas de metal que você não reconhece. Símbolos que queimam a vista.",
    "Uma caverna cristalina onde itens pulsam com luz azulada. O ar hum com poder antigo. Itens presos em cristal — preservados ou aprisionados.",
    "Uma câmara com riqueza de um reino perdido. Cada item tem marcas de sangue velho. Um trono vazio no centro.",
]

DESCRICOES_CURA = [
    "Uma gruta com fonte de água cristalina. A água brilha levemente. Você sente uma presença ancestral nas profundezas — sábia, antiga.",
    "Um santuário com aura de poder curativo. Símbolos sagrados nas paredes. Você se sente julgado. As lesões curam, mas algo observa.",
    "Um oásis subterrâneo de paz. Flores iluminescentes em padrões geométricos perfeitos. Seu reflexo na água não está sozinho.",
]

DESCRICOES_VENDA = [
    "Uma tenda que não estava aqui segundos atrás. Um vendedor com rosto sempre na sombra. Dedos longos demais. Dentes que não cabem numa boca normal.",
    "Um viajante em beco lateral. Capuz que não deixa ver o rosto. Itens sobre tecido negro que absorve luz. Ele pisca em três lugares ao mesmo tempo.",
    "Uma loja impossível na parede da masmorra. Dimensões erradas. Artefatos suspensos no ar. Vendedor feito de luz e sombra.",
]


def gerar_sala_aleatoria():
    from config import CHANCE_SALA_COMBATE, CHANCE_SALA_TESOURO, CHANCE_SALA_CURA
    p = random.randint(1, 100)

    if p <= CHANCE_SALA_COMBATE:
        from goblin import criar_goblin_aleatorio
        goblin   = criar_goblin_aleatorio()
        descricao = random.choice(DESCRICOES_COMBATE)
        return SalaCombate(goblin, descricao)

    elif p <= CHANCE_SALA_TESOURO:
        descricao = random.choice(DESCRICOES_TESOURO)
        return SalaTesourou(descricao, quantidade_itens=random.randint(2, 4))

    elif p <= CHANCE_SALA_CURA:
        descricao = random.choice(DESCRICOES_CURA)
        return SalaCura(descricao, cura_total=random.randint(30, 60))

    else:
        descricao = random.choice(DESCRICOES_VENDA)
        return SalaVenda(descricao)

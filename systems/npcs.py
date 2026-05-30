# ============================================================================
# NOUTRORA RPG — SISTEMA DE NPCs COM MEMÓRIA
# ============================================================================
# GDD: "NPCs lembram escolhas, ajuda, traições, mortes, ações passadas."
# GDD: "Isso cria conexão emocional, consequências persistentes."
#
# Cada NPC tem diálogos que mudam conforme o histórico registrado na Memória.
# ============================================================================

import time
from systems.memoria import memoria


def _digitar(texto, delay=0.03):
    """Efeito de digitação para imersão atmosférica."""
    import sys
    for char in texto:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()


# ============================================================================
# NPC: MERCADOR SOMBRIO
# ============================================================================

def encontro_mercador(jogador):
    """
    GDD: "Se o jogador ajudar um mercador no começo, ele pode ajudar em outra run."
    Reconhece o jogador se foi ajudado antes.
    """
    print("\n" + "=" * 60)
    print("  MERCADOR SOMBRIO")
    print("=" * 60)

    reconhece = memoria.mercador_reconhece()
    mortes    = memoria.obter("mortes_totais", 0)

    if reconhece:
        _digitar("\nUma figura encurvada emerge das sombras.")
        time.sleep(1)
        _digitar(f'  "...{jogador.nome}."')
        time.sleep(0.8)
        _digitar('  "Você voltou. Eu sabia que voltaria."')
        time.sleep(1)
        _digitar('  "Lembro do que fez por mim. Não esqueço."')
        time.sleep(1)
        _digitar('  "Pegue isto. Sem custo. Uma dívida paga."')
        time.sleep(1)

        from items import gerar_loot_aleatorio
        item = gerar_loot_aleatorio()
        jogador.adicionar_item(item)
        print(f"\n  Você recebeu: {item}")
        memoria.registrar_evento(f"Mercador presenteou {jogador.nome} — dívida honrada.")

    elif mortes > 3:
        _digitar("\nUma figura que você reconhece pelo peso dos olhos aparece.")
        time.sleep(0.8)
        _digitar('  "Você de novo. Quantas vezes mais preciso te ver antes que isso finde?"')
        time.sleep(0.8)
        _digitar(f'  "Morreu {mortes} vezes. {mortes} ressurreições sem explicação."')
        time.sleep(1)
        _digitar('  "Isto não é coragem, amigo. É maldição."')
        time.sleep(1)
        _digitar('  "Mas não importa. Eu ainda compro. E vendo."')
        time.sleep(0.8)

    else:
        _digitar("\nUma figura encapuzada surge da penumbra. Cheira a especiarias antigas e metal oxidado.")
        time.sleep(1)
        _digitar('  "Ah. Um rosto novo. Ou talvez não. Noutrora me embaça a memória."')
        time.sleep(0.8)
        _digitar('  "Mercadoria. Boa. Barata. Não faço perguntas sobre origem."')
        time.sleep(0.8)
        _digitar('  "E você não deveria fazer também. Algumas respostas matam."')
        time.sleep(1)

    # Loja
    _menu_mercador(jogador)


def _menu_mercador(jogador):
    from items import gerar_multiplos_itens
    from systems.equipment import obter_equipamentos_venda

    itens       = gerar_multiplos_itens(3)
    equipamentos = obter_equipamentos_venda(2)
    todos       = itens + equipamentos

    while True:
        print(f"\n  Sua bolsa: {jogador.dinheiro} gold")
        print("\n  À venda:")
        for i, item in enumerate(todos):
            preco = getattr(item, "preco", 30)
            print(f"    [{i}] {item}  — {preco} gold")
        print(f"    [{len(todos)}] Sair")

        try:
            op = int(input("\n  >> ").strip())
        except ValueError:
            continue

        if op == len(todos):
            print('\n  "Até a próxima... se houver próxima."')
            time.sleep(1)

            # GDD: Registrar se jogador ajudou / interagiu
            if not memoria.obter("ajudou_mercador"):
                _oferecer_ajuda_mercador(jogador)
            break

        if 0 <= op < len(todos):
            item  = todos[op]
            preco = getattr(item, "preco", 30)
            if jogador.remover_dinheiro(preco):
                if hasattr(item, "efeito_tipo"):
                    jogador.adicionar_item(item)
                else:
                    jogador.adicionar_equipamento(item)
                print(f"\n  Comprou: {item}")
            else:
                print(f"\n  Gold insuficiente. ({preco} necessário)")


def _oferecer_ajuda_mercador(jogador):
    """Escolha narrativa: ajudar ou não o mercador."""
    print("\n" + "=" * 60)
    _digitar('  "Espere."')
    time.sleep(0.6)
    _digitar('  "Preciso de um favor. Pequeno. Nada perigoso... provavelmente."')
    time.sleep(1)
    _digitar('  "Encontrou uma nota amassada no chão? Uma marca vermelha?"')
    time.sleep(1)

    print("\n  [1] Entregar a nota  — você não a viu, mas concorda")
    print("  [2] Recusar  — não é da sua conta")
    op = input("\n  >> ").strip()

    if op == "1":
        _digitar('\n  "Bom. Bom mesmo."')
        time.sleep(0.8)
        _digitar('  "Lembro de quem me ajuda."')
        memoria.definir("ajudou_mercador", True)
        memoria.registrar_evento(f"{jogador.nome} ajudou o Mercador Sombrio.")
        print("\n  [ O mercador guarda seu rosto na memória. ]")
    else:
        _digitar('\n  "...Entendido."')
        time.sleep(0.8)
        _digitar('  "Esqueça que perguntei."')
    time.sleep(1)


# ============================================================================
# NPC: ELFO FERIDO
# ============================================================================

def encontro_elfo_ferido(jogador):
    """
    GDD: "Se salvou o elfo em run anterior, ele pode ajudar futuramente."
    """
    print("\n" + "=" * 60)
    print("  ELFO FERIDO")
    print("=" * 60)

    deve_favor = memoria.elfo_deve_favor()

    if deve_favor:
        _digitar("\nEntre as pedras, uma figura élfica se levanta.")
        time.sleep(1)
        _digitar(f'  "...{jogador.nome}. Minha vida existe por você."')
        time.sleep(1)
        _digitar('  "Aceite isto. Não como pagamento — não há equivalência."')
        time.sleep(1)
        _digitar('  "Como gratidão que nunca caduca."')
        time.sleep(1)

        cura = jogador.curar(50)
        print(f"\n  O elfo cura você. +{cura} HP")
        jogador.adicionar_dinheiro(100)
        print(f"  Você recebe 100 gold.")
        memoria.registrar_evento(f"Elfo retribuiu favor a {jogador.nome}.")
        time.sleep(2)
        return

    # Primeiro encontro
    _digitar("\nVocê ouve um gemido abafado entre as rochas.")
    time.sleep(1)
    _digitar("Um elfo jaz ferido, respirando com dificuldade.")
    time.sleep(1)

    print("\n  [1] Ajudar o elfo  — usa um item de cura")
    print("  [2] Passar adiante — não é seu problema")
    op = input("\n  >> ").strip()

    if op == "1":
        if jogador.inventario:
            item = jogador.inventario.pop(0)
            _digitar(f'\n  Você usa {item.nome} no elfo.')
            time.sleep(1)
            _digitar('  "...Obrigado. Lembro de rostos."')
            memoria.definir("salvou_elfo", True)
            memoria.registrar_evento(f"{jogador.nome} salvou o Elfo Ferido.")
            print("\n  [ O elfo se levanta lentamente. Ele não esquecerá. ]")
        else:
            _digitar('\n  Você não tem itens. Você faz o que pode com as mãos.')
            time.sleep(1)
            _digitar('  O elfo sobrevive de qualquer forma.')
            memoria.definir("salvou_elfo", True)
            memoria.registrar_evento(f"{jogador.nome} tentou salvar o Elfo sem itens.")
    else:
        _digitar('\n  Você passa. O gemido some lentamente atrás de você.')
        time.sleep(1)
        _digitar('  Uma escolha feita. Uma consequência plantada.')
        memoria.registrar_evento(f"{jogador.nome} abandonou o Elfo Ferido.")
    time.sleep(2)


# ============================================================================
# NPC: REI GOBLIN
# ============================================================================

def encontro_goblin_rei(jogador):
    """
    GDD: "Rei Goblin oferece acordo. Se traído — desconfia nas próximas runs."
    """
    print("\n" + "=" * 60)
    print("  REI GOBLIN")
    print("=" * 60)

    desconfia = memoria.goblin_rei_desconfia()

    if desconfia:
        _digitar("\nO Rei Goblin emerge das sombras, mas para antes de se aproximar.")
        time.sleep(1)
        _digitar('  "Você. De novo."')
        time.sleep(0.8)
        _digitar('  "Não me engana duas vezes."')
        time.sleep(1)
        _digitar("  Ele chama seus guerreiros. Não há negociação.")
        time.sleep(1)
        print("\n  [ Combate forçado — memória tem consequências. ]")
        _combate_forzado_rei(jogador)
        return

    _digitar("\nUma figura massiva bloqueia o corredor. Ossos e pele, nada mais.")
    time.sleep(1)
    _digitar("O Rei Goblin. Uma coroa feita de ossos de seus inimigos. Olhos que pesam com séculos de morte.")
    time.sleep(1)
    _digitar('  "Você. Novo ou repetido, não importa. Meu olfato é certo."')
    time.sleep(1)
    _digitar('  "Ofereço: passagem sem sangue. Em troca: vinte moedas de ouro e UM item de seu tesouro."')
    time.sleep(1)
    _digitar('  "Recuse, e descubra por que meu trono é de ossos."')
    time.sleep(1)

    print("\n  [1] Aceitar o acordo — um negócio justo")
    print("  [2] Trair — fingir aceitar e atacar")
    print("  [3] Recusar — lutar de frente")
    op = input("\n  >> ").strip()

    if op == "1":
        if jogador.remover_dinheiro(20) and jogador.inventario:
            jogador.inventario.pop(0)
            _digitar('\n  O Rei Goblin inclina a cabeça — respeito entre predadores.')
            _digitar('  "Bem. Você honra seus juramentos. Isto é raro."')
            _digitar('  Os guardas se afastam em silêncio. Passagem livre pela masmorra.')
            memoria.registrar_evento(f"{jogador.nome} fez acordo com o Rei Goblin.")
            time.sleep(2)
        else:
            _digitar('\n  "Você não tem o que prometeu, mentiroso. Isto é insulto."')
            time.sleep(0.5)
            _combate_forzado_rei(jogador)

    elif op == "2":
        _digitar('\n  Você simula aceitar e ataca de surpresa.')
        time.sleep(1)
        _digitar('  O Rei Goblin uiva. "TRAIÇÃO!"')
        time.sleep(1)
        memoria.definir("traiu_goblin_rei", True)
        memoria.registrar_evento(f"{jogador.nome} traiu o Rei Goblin.")
        print("\n  [ Este ato será lembrado em todas as runs futuras. ]")
        _combate_forzado_rei(jogador)

    else:
        _digitar('\n  "Então seja. Sangue por sangue."')
        _combate_forzado_rei(jogador)


def _combate_forzado_rei(jogador):
    """Combate simplificado contra o Rei Goblin."""
    from inimigos import Goblin
    from batalhas import encontro_combate

    rei = Goblin(nivel=7, mutante=False)
    encontro_combate(jogador.nome, jogador, rei, "O Rei Goblin avança com força devastadora.")


# ============================================================================
# NPC: ENTIDADE DO ABISMO
# ============================================================================

def encontro_entidade(jogador):
    """
    Encontro raro. Oferece poder em troca de algo intangível.
    GDD: "Imersão psicológica, mistério, melancolia."
    """
    print("\n" + "=" * 60)
    print("  ENTIDADE DO ABISMO")
    print("=" * 60)
    time.sleep(1)

    tem_pacto = memoria.obter("pacto_demonio", False)
    mortes    = memoria.obter("mortes_totais", 0)

    if tem_pacto:
        _digitar("\nO ar esfria. Você já conhece essa presença.")
        time.sleep(1)
        _digitar('  "Voltou. Cumpriste tua parte inconscientemente."')
        time.sleep(1)
        _digitar('  "Cada morte tua foi alimento. Obrigado."')
        time.sleep(1)
        _digitar(f'  "{mortes} mortes. Bom rebanho."')
        time.sleep(2)
        print("\n  [ Você sente que cometeu um erro irreversível. ]")
        return

    _digitar("\nO corredor fica vazio demais. O silêncio é físico — asfixiante.")
    time.sleep(2)
    _digitar("Uma presença. Sem forma. Sem cheiro. Mas você SENTE. Cada célula do seu corpo grita.")
    time.sleep(1)
    _digitar('  "Vejo você. Vejo todas as suas mortes possíveis. Vejo também as vidas em que sobrevive."')
    time.sleep(1)
    _digitar('  "Ofereço força. Real. Não ilusória. Em troca... ainda nada agora."')
    time.sleep(1)
    _digitar('  "Apenas um contrato. As cláusulas? Virão quando menos esperar."')
    time.sleep(1)

    print("\n  [1] Aceitar o pacto — o poder merece o preço")
    print("  [2] Recusar — algo nisto cheira a morte")
    op = input("\n  >> ").strip()

    if op == "1":
        jogador.forca      += 8
        jogador.velocidade += 3
        _digitar('\n  "Bom. MUITO bom."')
        time.sleep(0.8)
        _digitar("  Você sente um poder sombrio inundar seus músculos — dói e exilara ao mesmo tempo.")
        time.sleep(0.8)
        _digitar("  Sua visão fica mais aguçada. Seus reflexos, sobrehumanos.")
        time.sleep(0.8)
        _digitar('  "Volte quando precisar. Sempre estarei aqui."')
        time.sleep(1)
        print(f"  ➜ Força +8 | Velocidade +3")
        memoria.definir("pacto_demonio", True)
        memoria.registrar_evento(f"{jogador.nome} fez pacto com a Entidade do Abismo.")
        print("\n  [ As cláusulas virão. Isto você SENTE. ]")
    else:
        _digitar('\n  "...Interessante. Uma recusa."')
        time.sleep(1)
        _digitar('  "Guardei seu rosto. Guardei seu cheiro. Sua essência me pertence."')
        time.sleep(0.8)
        _digitar('  A presença some. O ar fica morno. Mas você sabe: ela ainda está lá.')
        memoria.registrar_evento(f"{jogador.nome} recusou o pacto da Entidade.")
    time.sleep(2)

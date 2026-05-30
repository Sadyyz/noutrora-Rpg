# ============================================================================
# NOUTRORA RPG — SISTEMA DE COMBATE
# ============================================================================

import time
import random
from config import VARIACAO_DANO
import pygame


def calcular_dano(forca):
    return forca + random.randint(0, VARIACAO_DANO)


def determinar_iniciativa(vel_player, vel_goblin):
    return vel_player >= vel_goblin


def exibir_status_combate(player, goblin, turno):
    ft = player.obter_forca_total()
    vt = player.obter_velocidade_total()
    print(f"\n{'='*60}")
    print(f"  TURNO {turno}")
    print(f"{'='*60}")
    print(f"\n  {player.nome}:")
    print(f"    Vida      : {player.vida}/{player.vida_maxima}")
    print(f"    Forca     : {ft}  |  Velocidade: {vt}")
    if player.arma_equipada:
        print(f"    Arma      : {player.arma_equipada.nome}")
    print(f"\n  {goblin.obter_status()['tipo']}:")
    print(f"    Vida      : {goblin.vida}/{goblin.vida_maxima}")
    print(f"    Forca     : {goblin.forca}  |  Velocidade: {goblin.velocidade}")
    print(f"\n  {goblin.descrever_visualmente()}")


def obter_acao_jogador(player):
    while True:
        print(f"\n{'='*60}")
        print("  SUAS AÇÕES:")
        print("  [1] Atacar")
        print("  [2] Defender")
        if player.inventario:
            print(f"  [3] Usar Item  ({len(player.inventario)} disponíveis)")
        print("  [4] Fugir")
        print(f"{'='*60}")
        op = input("\n  >> ").strip()
        if op == "1":
            return "atacar"
        elif op == "2":
            return "defender"
        elif op == "3" and player.inventario:
            return "usar_item"
        elif op == "4":
            return "fugir"
        else:
            print("  Opção inválida.")


def processar_acao_jogador(player, goblin, acao):
    if acao == "atacar":
        dano = calcular_dano(player.obter_forca_total())
        goblin.tomar_dano(dano)
        frases = [
            "Você avança com tudo. Sua arma corta o ar.",
            "Um grito de batalha. Você se lança.",
            "Você vê uma abertura e ataca.",
            "Seus músculos ardem. O golpe sai.",
        ]
        print(f"\n  {random.choice(frases)}")
        print(f"  Dano causado: {dano}")
        if not goblin.esta_vivo():
            print(f"  A criatura cai.")
        time.sleep(1)
        return "atacou"

    elif acao == "defender":
        print("\n  Você eleva sua guarda.")
        print("  O próximo golpe terá impacto reduzido.")
        time.sleep(1)
        return "defendeu"

    elif acao == "usar_item":
        print(f"\n{player.listar_inventario()}")
        try:
            idx = int(input("\n  Qual item usar? >> ").strip())
            resultado = player.usar_item(idx)
            print(f"\n  {resultado}")
            time.sleep(1)
        except ValueError:
            print("  Número inválido.")
        return "usou_item"

    elif acao == "fugir":
        if random.randint(1, 100) > 50:
            print("\n  Você corre. A escuridão te engole.")
            time.sleep(1)
            return "fugiu"
        else:
            print("\n  Você tenta fugir — a criatura bloqueia o caminho.")
            time.sleep(1)
            return "falhou_fuga"


def executar_turno_interativo(player, goblin, turno):
    exibir_status_combate(player, goblin, turno)
    acao = obter_acao_jogador(player)
    resultado = processar_acao_jogador(player, goblin, acao)

    if resultado == "fugiu":
        return "fugiu", False

    if not goblin.esta_vivo():
        from config import XP_POR_VITORIA, RECOMPENSA_VITORIA_MIN, RECOMPENSA_VITORIA_MAX
        xp    = XP_POR_VITORIA
        gold  = random.randint(RECOMPENSA_VITORIA_MIN, RECOMPENSA_VITORIA_MAX)
        player.ganhar_experiencia(xp)
        player.adicionar_dinheiro(gold)
        print(f"\n  Vitória! +{xp} XP  +{gold} gold")
        time.sleep(2)
        return "vitoria", False

    # Reação do goblin
    print(f"\n{'='*60}")
    print("  REAÇÃO DO INIMIGO")
    print(f"{'='*60}")

    if random.randint(1, 2) == 1:
        dano = calcular_dano(goblin.forca)
        if resultado == "defendeu":
            dano = max(1, int(dano * 0.5))
            print("\n  Sua defesa amortece o golpe!")
        player.tomar_dano(dano)
        print(f"\n  O {goblin.obter_status()['tipo'].lower()} ataca!")
        print(f"  Você recebe {dano} de dano.  Vida: {player.vida}/{player.vida_maxima}")
    else:
        print(f"\n  O {goblin.obter_status()['tipo'].lower()} observa.")
        print("  Respiração pesada. Próximo turno.")

    time.sleep(1)

    if not player.esta_vivo():
        print("\n  Você foi derrotado.")
        time.sleep(2)
        return "derrota", False

    return "em_andamento", True


def encontro_combate(nome, player, goblin, cenario_texto):

    pygame.mixer.quit()  # Para garantir que o mixer seja reinicializado
    pygame.mixer.init()
    pygame.mixer.music.load("musicas/soundtracks/BATTLE.wav")
    pygame.mixer.music.play()
    """Controlador principal de um encontro de combate."""
    print(f"\n{cenario_texto}")
    time.sleep(1)
    print(f"\n  {goblin.obter_status()['tipo']} aparece!")
    print(f"  {goblin.descrever_visualmente()}")
    time.sleep(2)

    while True:
        print("\n" + "=" * 60)
        print("  [1] Combater")
        print("  [2] Tentar fugir agora")
        print("=" * 60)
        op = input(f"\n  {nome}, o que fará? >> ").strip()

        if op == "1":
            print("\n  O duelo começa.")
            time.sleep(1)
            turno = 1
            while player.esta_vivo() and goblin.esta_vivo():
                resultado, continua = executar_turno_interativo(player, goblin, turno)
                if not continua:
                    return resultado
                turno += 1
                input("\n  [ ENTER para continuar ]")

        elif op == "2":
            if random.randint(1, 100) > 40:
                print("\n  Você consegue fugir.")
                time.sleep(1)
                return "fugiu"
            else:
                print("\n  Não conseguiu fugir. Luta inevitável.")
                time.sleep(2)

        else:
            print("  Opção inválida.")

# ============================================================================
# NOUTRORA RPG — SISTEMA DE COMBATE (v2 — Habilidades + Inimigos Variados)
# ============================================================================

import time
import random
from config import VARIACAO_DANO
import pygame

try:
    from systems.audio import audio_manager
except ImportError:
    audio_manager = None


def calcular_dano(forca):
    return forca + random.randint(0, VARIACAO_DANO)


def _tem_habilidades(player):
    return hasattr(player, "habilidades") and player.habilidades


# ============================================================================
# DISPLAY
# ============================================================================

def exibir_status_combate(player, inimigo, turno):
    ft  = player.obter_forca_total()
    vt  = player.obter_velocidade_total()
    mana_str = ""
    if hasattr(player, "mana") and player.mana_maxima < 999:
        mana_str = f"  Mana      : {player.mana}/{player.mana_maxima}\n"

    print(f"\n{'='*60}")
    print(f"  TURNO {turno}")
    print(f"{'='*60}")
    print(f"\n  {player.nome}  [Nv{player.nivel}]:")
    print(f"    Vida      : {player.vida}/{player.vida_maxima}")
    print(f"{mana_str}    Forca     : {ft}  |  Velocidade: {vt}")
    if player.arma_equipada:
        print(f"    Arma      : {player.arma_equipada.nome}")

    efeitos = player.efeitos_ativos() if hasattr(player, "efeitos_ativos") else []
    if efeitos:
        print(f"    Efeitos   : {', '.join(efeitos)}")

    status = inimigo.obter_status()
    print(f"\n  {status['tipo']}  [Nv{inimigo.nivel}]:")
    print(f"    Vida      : {inimigo.vida}/{inimigo.vida_maxima}")
    print(f"    Forca     : {inimigo.forca}  |  Velocidade: {inimigo.velocidade}")

    efeitos_in = list(inimigo._efeitos.keys()) if inimigo._efeitos else []
    if efeitos_in:
        print(f"    Efeitos   : {', '.join(efeitos_in)}")

    print(f"\n  {inimigo.descrever_visualmente()}")


# ============================================================================
# MENU DE AÇÃO
# ============================================================================

def obter_acao_jogador(player):
    while True:
        print(f"\n{'='*60}")
        print("  SUAS ACOES:")
        print("  [1] Atacar")
        print("  [2] Defender")
        if player.inventario:
            print(f"  [3] Usar Item  ({len(player.inventario)} disponíveis)")
        if _tem_habilidades(player):
            print(f"  [5] Habilidades  ({len(player.habilidades)} disponíveis)")
        print("  [4] Fugir")
        print(f"{'='*60}")
        op = input("\n  >> ").strip()

        if op == "1":   return "atacar"
        elif op == "2": return "defender"
        elif op == "3" and player.inventario: return "usar_item"
        elif op == "4": return "fugir"
        elif op == "5" and _tem_habilidades(player): return "habilidade"
        else: print("  Opcao invalida.")


# ============================================================================
# PROCESSAR AÇÃO DO JOGADOR
# ============================================================================

def processar_acao_jogador(player, inimigo, acao):

    # ----------------------------------------------------------------
    if acao == "atacar":
        dano = calcular_dano(player.obter_forca_total())
        inimigo.tomar_dano(dano)
        inimigo.tocar_som("acerto")
        frases = [
            "Voce avanca com furia. Seus musculos se contraem — o golpe corta o ar com um som de morte.",
            "Um grito de batalha rouco sai de sua garganta. Voce se lanca com tudo que tem.",
            "Voce vê a fraqueza. Vê o ponto exato onde a dor sera maxima. Seu corpo age.",
            "Adrenalina pura. Seus sentidos afiam. O golpe sai com precisao mortal.",
            "Voce respira fundo. Cada movimento é calculo. Cada golpe, destino.",
        ]
        print(f"\n  {random.choice(frases)}")
        print(f"  ➜ Dano causado: {dano} HP")
        if not inimigo.esta_vivo():
            inimigo.tocar_som("morte")
            print(f"  A criatura desaba em silencio. Tudo o que ela era, agora e historia.")
        time.sleep(0.8)
        return "atacou"

    # ----------------------------------------------------------------
    elif acao == "defender":
        frases_defesa = [
            "Voce encolhe os ombros, elevando sua guarda. Espera, imóvel.",
            "Breath em. Todos os músculos se tendem. Voce se prepara para o impacto.",
            "Sua arma sobe como um escudo. Cada nervo do seu corpo pronto para absorver o golpe.",
        ]
        print(f"\n  {random.choice(frases_defesa)}")
        print("  O proximo golpe tera impacto MUITO reduzido.")
        time.sleep(0.8)
        return "defendeu"

    # ----------------------------------------------------------------
    elif acao == "usar_item":
        print(f"\n{player.listar_inventario()}")
        try:
            idx = int(input("\n  Qual item usar? >> ").strip())
            resultado = player.usar_item(idx)
            print(f"\n  {resultado}")
            time.sleep(0.8)
        except ValueError:
            print("  Numero invalido.")
        return "usou_item"

    # ----------------------------------------------------------------
    elif acao == "habilidade":
        print(f"\n{player.listar_habilidades()}")
        print(f"\n  Mana: {getattr(player, 'mana', '?')}/{getattr(player, 'mana_maxima', '?')}")
        try:
            idx = int(input("\n  Qual habilidade? >> ").strip())
            resultado = player.usar_habilidade(idx, inimigo)
            inimigo.tocar_som("acerto")
            print(f"\n{resultado}")
            time.sleep(1)
        except ValueError:
            print("  Numero invalido.")
        return "usou_habilidade"

    # ----------------------------------------------------------------
    elif acao == "fugir":
        if random.randint(1, 100) > 50:
            print("\n  Voce corre. A escuridao te engole.")
            time.sleep(0.8)
            return "fugiu"
        else:
            print("\n  Voce tenta fugir — o inimigo bloqueia o caminho!")
            time.sleep(0.8)
            return "falhou_fuga"


# ============================================================================
# TURNO COMPLETO
# ============================================================================

def executar_turno_interativo(player, inimigo, turno):

    # 1. Efeitos passivos do INIMIGO (veneno, sangramento que o player aplicou)
    msgs_inimigo = inimigo.turno_passivo()
    if msgs_inimigo:
        print()
        for m in msgs_inimigo: print(m)

    if not inimigo.esta_vivo():
        return _vitoria(player)

    # 2. Efeitos passivos do PLAYER (regen, veneno, etc)
    if hasattr(player, "turno_passivo"):
        msgs_player = player.turno_passivo()
        if msgs_player:
            print()
            for m in msgs_player: print(m)

    if not player.esta_vivo():
        print("\n  Voce foi derrotado pelos proprios efeitos.")
        time.sleep(2)
        return "derrota", False

    # 3. Status + escolha
    exibir_status_combate(player, inimigo, turno)

    acao     = obter_acao_jogador(player)
    resultado = processar_acao_jogador(player, inimigo, acao)

    if resultado == "fugiu":
        return "fugiu", False

    # 4. Checar morte do inimigo
    if not inimigo.esta_vivo():
        return _vitoria(player)

    # 5. Turno do inimigo
    print(f"\n{'='*60}")
    print(f"  TURNO DO INIMIGO")
    print(f"{'='*60}")

    # Atordoado?
    if inimigo.esta_atordoado():
        print(f"\n  {inimigo.TIPO} esta atordoado e perde o turno!")
        time.sleep(0.8)
    else:
        _turno_inimigo(player, inimigo, resultado)

    time.sleep(0.8)

    if not player.esta_vivo():
        print("\n  Voce foi derrotado.")
        time.sleep(2)
        return "derrota", False

    return "em_andamento", True


def _turno_inimigo(player, inimigo, resultado_player):
    """Executa a ação do inimigo neste turno."""

    # Tentativa de ação especial primeiro (25% chance)
    especial = inimigo.acao_especial(player)
    if especial:
        print(f"\n{especial}")
        # Aplica espinhos se player tiver
        _checar_espinhos(player, inimigo)
        return

    # Ataque normal (50% ataca, 50% observa)
    if random.randint(1, 2) == 1:
        dano = inimigo.calcular_dano_ataque()

        # Escudo arcano (Arcanista)
        if getattr(player, "_escudo_cargas", 0) > 0:
            player._escudo_cargas -= 1
            print(f"\n  O Escudo Arcano absorve o ataque! ({player._escudo_cargas} cargas restantes)")
            return

        # Intangível (Espectro)
        if getattr(player, "_intangivel", False):
            if getattr(player, "_turnos_intang", 0) > 0:
                player._turnos_intang -= 1
                print(f"\n  O ataque passa direto por voce! (Dissolucao ativa, {player._turnos_intang} turnos)")
                if player._turnos_intang <= 0:
                    player._intangivel = False
                return

        # Esquiva (Espectro)
        if hasattr(player, "tentar_esquiva") and player.tentar_esquiva():
            print(f"\n  Voce esquiva com velocidade sobrenatural!")
            return

        # Resistência (Portador)
        if getattr(player, "_resistencia_ativa", False):
            dano = max(1, int(dano * 0.2))
            player._resistencia_ativa = False
            print(f"\n  Resistencia da Maldicao! Dano reduzido em 80%!")

        # Defesa normal
        if resultado_player == "defendeu":
            dano = max(1, int(dano * 0.5))
            print(f"\n  Sua defesa amortece o golpe!")

        # Forma de Besta do Metamorfo (-30% defesa)
        from assets.classes.metamorfo import Metamorfo
        if isinstance(player, Metamorfo) and player.forma_ativa == "besta":
            dano = int(dano * 1.3)

        player.tomar_dano(dano)
        print(f"\n  {inimigo.TIPO} ataca!")
        print(f"  Voce recebe {dano} de dano.  Vida: {player.vida}/{player.vida_maxima}")

        # Espinhos (Metamorfo)
        _checar_espinhos(player, inimigo)
    else:
        print(f"\n  {inimigo.TIPO} observa seus movimentos.")
        print("  Respiracao pesada. Proximo turno.")


def _checar_espinhos(player, inimigo):
    """Se o Metamorfo tem espinhos, o inimigo toma dano ao atacar."""
    if getattr(player, "_espinhos_ativos", False):
        dano = getattr(player, "_dano_espinhos", 5)
        inimigo.tomar_dano(dano)
        print(f"  [Espinhos] Inimigo toma {dano} de dano de contato!")


def _vitoria(player):
    from config import XP_POR_VITORIA, RECOMPENSA_VITORIA_MIN, RECOMPENSA_VITORIA_MAX
    xp   = XP_POR_VITORIA
    gold = random.randint(RECOMPENSA_VITORIA_MIN, RECOMPENSA_VITORIA_MAX)
    player.ganhar_experiencia(xp)
    player.adicionar_dinheiro(gold)
    print(f"\n  Vitoria!  +{xp} XP  +{gold} gold")
    time.sleep(2)
    return "vitoria", False


# ============================================================================
# ENCONTRO PRINCIPAL
# ============================================================================

def encontro_combate(nome, player, inimigo, cenario_texto):
    pygame.quit()
    pygame.mixer.init()
    
    # Inicia música de batalha
    if audio_manager:
        audio_manager.tocar_musica_batalha()
    
    print(f"\n{cenario_texto}")
    time.sleep(1)
    print(f"\n  {inimigo.obter_status()['tipo']} aparece!")
    inimigo.tocar_som("aparecimento")
    print(f"\n  {inimigo.descrever_visualmente()}")
    time.sleep(2)

    while True:
        print("\n" + "=" * 60)
        print("  [1] Combater")
        print("  [2] Tentar fugir agora")
        print("=" * 60)
        op = input(f"\n  {nome}, o que fara? >> ").strip()

        if op == "1":
            print("\n  O duelo comeca.")
            time.sleep(1)
            turno = 1
            while player.esta_vivo() and inimigo.esta_vivo():
                resultado, continua = executar_turno_interativo(player, inimigo, turno)
                if not continua:
                    if audio_manager:
                        audio_manager.tocar_musica_principal()
                    return resultado
                turno += 1
                input("\n  [ ENTER para continuar ]")

        elif op == "2":
            if random.randint(1, 100) > 40:
                print("\n  Voce consegue fugir.")
                time.sleep(1)
                if audio_manager:
                    audio_manager.tocar_musica_principal()
                return "fugiu"
            else:
                print("\n  Nao conseguiu fugir. Luta inevitavel.")
                time.sleep(2)
        else:
            print("  Opcao invalida.")

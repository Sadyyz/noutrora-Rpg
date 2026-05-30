
import random
import sys
import time
import pygame
# Colorama (opcional — degrada graciosamente se não estiver instalado)
try:
    import colorama
    from colorama import Fore, Style
    colorama.init(autoreset=True)
    _COR_TITULO  = Fore.LIGHTGREEN_EX
    _COR_RESET   = Style.RESET_ALL
    _COR_AVISO   = Fore.YELLOW
    _COR_PERIGO  = Fore.RED
except ImportError:
    _COR_TITULO = _COR_RESET = _COR_AVISO = _COR_PERIGO = ""

from config import NOME_MINIMO, XP_POR_SALA_EXPLORADA
from player import Player
from batalhas import encontro_combate
from salas import gerar_sala_aleatoria, SalaCombate, SalaTesourou, SalaCura, SalaVenda
from assets.classes.metamorfo import Metamorfo
from assets.classes.druida import Druida
from assets.save.save_config import salvar_jogo, carregar_jogo, save_existe, deletar_save
from systems.memoria import memoria
from systems.run_procedural import GeraRun, processar_evento

# ============================================================================
# BANNER ASCII
# ============================================================================

BANNER = r"""
███╗   ██╗ ██████╗ ██╗   ██╗████████╗██████╗  ██████╗ ██████╗  █████╗
████╗  ██║██╔═══██╗██║   ██║╚══██╔══╝██╔══██╗██╔═══██╗██╔══██╗██╔══██╗
██╔██╗ ██║██║   ██║██║   ██║   ██║   ██████╔╝██║   ██║██████╔╝███████║
██║╚██╗██║██║   ██║██║   ██║   ██║   ██╔══██╗██║   ██║██╔══██╗██╔══██║
██║ ╚████║╚██████╔╝╚██████╔╝   ██║   ██║  ██║╚██████╔╝██║  ██║██║  ██║
╚═╝  ╚═══╝ ╚═════╝  ╚═════╝    ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝
           "Onde almas esquecidas vagam pela escuridão..."
"""


# ============================================================================
# UTILS DE EXIBIÇÃO
# ============================================================================

def _digitar(texto, delay=0.025):
    """Efeito de digitação lenta para atmosfera."""
    for char in texto:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()


def _pausa(segundos=1.5):
    time.sleep(segundos)


def _linha():
    print("=" * 60)


# ============================================================================
# MENU PRINCIPAL
# ============================================================================

def menu():
    pygame.mixer.init()
    pygame.mixer.music.load("musicas/soundtracks/MAIN.wav")
    pygame.mixer.music.play()

    print(_COR_TITULO + BANNER + _COR_RESET)

    # Exibe resumo do histórico se há memória acumulada
    if not memoria.primeira_vez():
        print("  [ Histórico detectado ]")
        print(memoria.resumo_runs())
        print()

    while True:
        _linha()
        print("  [1] Nova run")
        print("  [2] Carregar run salva")
        print("  [3] Memória do mundo")
        print("  [4] Sair")
        _linha()
        escolha = input("\n  >> ").strip()

        if escolha == "1":
            _iniciar_nova_run()
            break

        elif escolha == "2":
            jogador = carregar_jogo()
            if jogador:
                print(f"\n  Run carregada: {jogador.nome}  |  Sala {jogador.sala_atual}")
                _pausa(1)
                _explorar_masmorra(jogador.nome, jogador)
            else:
                print("\n  Nenhuma run salva encontrada.")
                _pausa(1)

        elif escolha == "3":
            _exibir_memoria()

        elif escolha == "4":
            print("\n  Até a próxima.")
            _pausa(1)
            sys.exit(0)

        else:
            print("\n  Opção inválida.")


# ============================================================================
# MEMÓRIA DO MUNDO (menu de lore/histórico)
# ============================================================================

def _exibir_memoria():
    _linha()
    print("  MEMORIA DO MUNDO")
    _linha()
    print("\n  Estatísticas:")
    print(memoria.resumo_runs())
    print("\n  Eventos recentes:")
    print(memoria.diario_recente())
    print("\n  Escolhas registradas:")

    flags = [
        ("ajudou_mercador",   "Ajudou o Mercador Sombrio"),
        ("traiu_goblin_rei",  "Traiu o Rei Goblin"),
        ("salvou_elfo",       "Salvou o Elfo Ferido"),
        ("destruiu_caverna",  "Destruiu um altar"),
        ("pacto_demonio",     "Fez pacto com a Entidade do Abismo"),
    ]
    for chave, descricao in flags:
        valor   = memoria.obter(chave, False)
        simbolo = "X" if valor else "."
        print(f"    [{simbolo}] {descricao}")

    print()
    input("  [ ENTER para voltar ]")


# ============================================================================
# INÍCIO DE NOVA RUN
# ============================================================================

def _iniciar_nova_run():
    """Fluxo completo de início: prólogo → nome → classe → jogo."""
    memoria.incrementar("runs_iniciadas")

    _exibir_prologo()

    nome     = _obter_nome_jogador()
    jogador  = _escolher_classe(nome)

    if jogador is None:
        return

    # GDD: Mensagem muda se é veterano (morreu antes)
    if memoria.e_veterano():
        mortes = memoria.obter("mortes_totais", 0)
        print(f"\n  Você voltou, {jogador.nome}.")
        _pausa(0.8)
        print(f"  {mortes} mortes registradas.")
        _pausa(0.8)
        print("  A masmorra lembra de você.")
    else:
        print(f"\n  Bem-vindo, {jogador.nome}.")
        _pausa(0.8)
        print("  Sua aventura começa agora.")

    print(f"\n  Vida: {jogador.vida}  |  Força: {jogador.forca}  |  Velocidade: {jogador.velocidade}")
    _pausa(2)

    _explorar_masmorra(nome, jogador)


# ============================================================================
# PRÓLOGO
# ============================================================================

def _exibir_prologo():
    while True:
        op = input("\n  Deseja ver o prólogo? (sim/nao): ").lower().strip()
        if op in ["nao", "não"]:
            print("\n  Prólogo pulado.")
            _pausa(1)
            return

        elif op == "sim":
            _narrar_prologo()
            return
        else:
            print("  Digite 'sim' ou 'nao'.")


def _narrar_prologo():
    print("\n" + "=" * 60)
    _digitar("\nA chuva caía como punhos sobre os telhados de Stormcloak.")
    _pausa(2)
    _digitar(
        "O pequeno vilarejo parecia ter sido abandonado há séculos. "
        "As poucas pessoas nas ruas evitavam olhar umas para as outras — "
        "e evitavam olhar para cima."
    )
    _pausa(4)
    _digitar(
        "\nVocê cresceu naquele lugar de desesperança. "
        "Filho de artesãos, passou a vida ouvindo histórias sobre Noutrora — "
        "uma masmorra que não deveria existir, construída por uma civilização "
        "apagada da história."
    )
    _pausa(4)

    # GDD: Se é veterano, prólogo muda
    if memoria.e_veterano():
        mortes = memoria.obter("mortes_totais", 0)
        _digitar(f"\nVocê já esteve aqui antes. {mortes} vezes.")
        _pausa(1)
        _digitar("E voltou todas elas.")
        _pausa(1)
        _digitar("Por quê? Você mesmo não sabe responder.")
        _pausa(2)
    else:
        _digitar(
            "\nUma manchete em um jornal amassado:\n"
            "\n  >>> A MASMORRA DE NOUTRORA VOLTA A EMITIR SINAIS APÓS 200 ANOS <<<\n"
        )
        _pausa(3)
        _digitar(
            "Naquela noite, algo mudou em você. "
            "Talvez curiosidade. Talvez ganância. "
            "Ou talvez algo mais antigo — uma chamada que não conseguia explicar."
        )
        _pausa(3)

    _digitar(
        "\nA entrada de Noutrora não é grande. "
        "É exatamente do tamanho certo para parecer feita especificamente para você. "
        "O ar que sai é quente e carregado de morte."
    )
    _pausa(3)
    _digitar("\nEste é o limiar.")
    _pausa(1)
    _digitar("Diga-me...")
    _digitar("qual")
    _digitar("é")
    _digitar("o") 
    _digitar("seu")
    _digitar("nome?")
    _pausa(2)


# ============================================================================
# NOME DO JOGADOR
# ============================================================================

def _obter_nome_jogador():
    while True:
        nome = input("\n  Seu nome: ").strip()
        if len(nome) <= NOME_MINIMO:
            print(f"  Nome muito curto. Mínimo {NOME_MINIMO + 1} letras.")
        else:
            return nome


# ============================================================================
# ESCOLHA DE CLASSE
# ============================================================================

def _escolher_classe(nome):
    while True:
        _linha()
        print("  ESCOLHA SUA CLASSE")
        _linha()
        print("  [1] Metamorfo")
        print("      Absorve essência de inimigos derrotados.")
        print("      +3 força  |  -1 velocidade")
        print()
        print("  [2] Druida")
        print("      Manipula toxinas e venenos da floresta.")
        print("      +2 velocidade  |  -2 força  |  3 cargas de veneno")
        _linha()

        op = input("\n  >> ").strip()

        if op == "1":
            jogador = Metamorfo(nome)
            print("\n  Metamorfo.")
            print("  Criaturas que abandonaram a própria humanidade em busca de poder.")
            _pausa(2)
            return jogador

        elif op == "2":
            jogador = Druida(nome)
            print("\n  Druida.")
            print("  Guardiões do equilíbrio. Enfraquecendo tudo que cruza seu caminho.")
            _pausa(2)
            return jogador

        else:
            print("  Opção inválida.")


# ============================================================================
# LOOP PRINCIPAL DE EXPLORAÇÃO
# ============================================================================

def _explorar_masmorra(nome, jogador):
    """
    GDD: "O jogador avança por eventos, escolhas e encontros."
    GDD: "Estrutura procedural — ordem muda a cada run."
    """
    salas_exploradas = 0
    gera_run         = GeraRun()   # GDD: procedural — embaralha eventos

    while jogador.esta_vivo():
        salas_exploradas   += 1
        jogador.sala_atual  = salas_exploradas

        # Atualizar recorde de profundidade na memória
        recorde = memoria.obter("maior_sala_alcancada", 0)
        if salas_exploradas > recorde:
            memoria.definir("maior_sala_alcancada", salas_exploradas)

        print(f"\n{'='*60}")
        print(f"  SALA {salas_exploradas}")
        print(f"  Vida: {jogador.vida}/{jogador.vida_maxima}  |"
              f"  Itens: {len(jogador.inventario)}  |"
              f"  Gold: {jogador.dinheiro}  |"
              f"  Nível: {jogador.nivel}")
        print(f"{'='*60}")

        # -------------------------------------------------------
        # GDD: "Evento especial" — a cada ~5 salas
        # -------------------------------------------------------
        evento = gera_run.proximo_evento_especial(salas_exploradas)
        if evento:
            processar_evento(evento, jogador)
            if not jogador.esta_vivo():
                _game_over(jogador, salas_exploradas)
                return

        # -------------------------------------------------------
        # Sala normal (combate / tesouro / cura / venda)
        # -------------------------------------------------------
        sala = gerar_sala_aleatoria()

        if isinstance(sala, SalaCombate):
            resultado = encontro_combate(nome, jogador, sala.goblin, sala.descricao)

            if resultado == "vitoria":
                memoria.incrementar("inimigos_derrotados")
                # GDD: Metamorfo absorve essência
                if isinstance(jogador, Metamorfo):
                    msg = jogador.absorver_essencia(sala.goblin)
                    print(f"\n  [Metamorfo] {msg}")
                jogador.ganhar_experiencia(XP_POR_SALA_EXPLORADA)
                print(f"\n  Vida restante: {jogador.vida}/{jogador.vida_maxima}")
                _pausa(1)

                # Oferecer save a cada 5 salas
                if salas_exploradas % 5 == 0:
                    _oferecer_save(jogador)

            elif resultado == "derrota":
                _game_over(jogador, salas_exploradas)
                return

            elif resultado == "fugiu":
                print(f"\n  Você fugiu após {salas_exploradas} salas.")
                _oferecer_save(jogador)
                return

        elif isinstance(sala, SalaTesourou):
            sala.executar(jogador)
            _pausa(1)

        elif isinstance(sala, SalaCura):
            sala.executar(jogador)
            # GDD: Druida regenera veneno em fontes
            if isinstance(jogador, Druida):
                jogador.regenerar_veneno()
                print("  [Druida] Carga de veneno regenerada.")
            _pausa(1)

        elif isinstance(sala, SalaVenda):
            print("\n  Uma figura emerge da escuridão. Tem algo para vender.")
            sala.executar(jogador)
            _pausa(1)

    _game_over(jogador, salas_exploradas)


# ============================================================================
# GAME OVER
# ============================================================================

def _game_over(jogador, salas):
    """
    GDD: "Memória persistente — cada morte alimenta o mundo."
    """
    memoria.incrementar("mortes_totais")
    memoria.registrar_evento(
        f"{jogador.nome} morreu na sala {salas}  "
        f"(nível {jogador.nivel}, {jogador.faccao})"
    )

    print(f"\n{'='*60}")
    print("  FIM DA RUN")
    print(f"{'='*60}")
    print(f"\n  {jogador.nome} caiu na sala {salas}.")
    _pausa(1)
    print(f"  Nível alcançado   : {jogador.nivel}")
    print(f"  Experiência total : {jogador.experiencia}")
    print(f"  Inimigos mortos   : {memoria.obter('inimigos_derrotados', 0)}")
    print(f"  Mortes totais     : {memoria.obter('mortes_totais', 0)}")
    _pausa(2)

    # GDD: Mundo comenta a morte
    mortes = memoria.obter("mortes_totais", 0)
    if mortes == 1:
        print("\n  A masmorra registrou sua primeira queda.")
        print("  Ela não esquece.")
    elif mortes <= 5:
        print(f"\n  Mais uma marca nas paredes de Noutrora.")
        print(f"  {mortes} ao total.")
    else:
        print(f"\n  {mortes} mortes.")
        print("  Você persiste. A masmorra também.")

    _pausa(2)

    # Apagar save da run (morte = reset da run atual)
    deletar_save()

    # Oferecer nova run
    print("\n  [1] Tentar novamente")
    print("  [2] Menu principal")
    op = input("\n  >> ").strip()
    if op == "1":
        _iniciar_nova_run()
    else:
        menu()


# ============================================================================
# SAVE DURANTE EXPLORAÇÃO
# ============================================================================

def _oferecer_save(jogador):
    print("\n  Deseja salvar? (s/n)")
    op = input("  >> ").strip().lower()
    if op == "s":
        salvar_jogo(jogador)


# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    menu()

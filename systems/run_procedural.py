# ============================================================================
# NOUTRORA RPG — SISTEMA PROCEDURAL DE RUNS
# ============================================================================
# GDD: "Todos os cenários podem aparecer em todas as runs."
# GDD: "Mas a ordem muda, o contexto muda, as consequências mudam."
#
# Pool de eventos: embaralhado a cada run.
# Certos eventos só aparecem com base na memória acumulada.
# ============================================================================

import random
from systems.memoria import memoria


# --------------------------------------------------------------------------
# POOL DE EVENTOS NARRATIVOS
# (além das salas normais — combat/tesouro/cura — esses são encontros únicos)
# --------------------------------------------------------------------------

EVENTOS_BASE = [
    "mercador",       # Encontro com Mercador Sombrio
    "elfo_ferido",    # Elfo ferido que pode ser salvo
    "goblin_rei",     # Negociação com o Rei Goblin
    "entidade",       # Entidade do Abismo (raro)
    "armadilha",      # Sala com armadilha
    "inscricoes",     # Sala de inscrições antigas
    "altar",          # Altar que pode curar ou maldizer
    "eco_passado",    # Visão de run anterior (atmosférico)
    "prisioneiro",    # Prisioneiro pedindo ajuda
]


class GeraRun:
    """
    Gera a sequência de eventos de uma run.
    Cada run tem uma ordem diferente dos mesmos elementos.
    GDD: "O jogador vive runs diferentes onde os mesmos eventos
          aparecem em ordens diferentes."
    """

    def __init__(self):
        self._pool_eventos = self._montar_pool()
        self._indice       = 0

    def _montar_pool(self):
        """
        Monta pool personalizado com base na memória.
        Eventos de memória têm chance de aparecer conforme histórico.
        """
        pool = EVENTOS_BASE.copy()

        # Evento de memória: eco do passado aparece mais vezes
        # se o jogador já morreu antes
        mortes = memoria.obter("mortes_totais", 0)
        if mortes > 0:
            pool.append("eco_passado")  # +1 ocorrência
        if mortes > 5:
            pool.append("eco_passado")  # +2 se veterano

        # Entidade aparece mais se o pacto foi feito
        if memoria.obter("pacto_demonio", False):
            pool.append("entidade")

        random.shuffle(pool)
        return pool

    def proximo_evento_especial(self, sala_numero):
        """
        A cada ~5 salas, um evento especial pode ocorrer.
        Retorna None se não for hora de evento especial.
        """
        # Eventos especiais nas salas 5, 10, 15, 20...
        if sala_numero % 5 != 0:
            return None

        # 40% de chance de aparecer
        if random.randint(1, 100) > 40:
            return None

        if self._indice >= len(self._pool_eventos):
            self._pool_eventos = self._montar_pool()
            self._indice       = 0

        evento = self._pool_eventos[self._indice]
        self._indice += 1
        return evento

    def log_ordem_run(self):
        """Retorna a sequência de eventos desta run (para debug/narrativa)."""
        return self._pool_eventos.copy()


# --------------------------------------------------------------------------
# PROCESSADOR DE EVENTOS ESPECIAIS
# --------------------------------------------------------------------------

def processar_evento(tipo_evento, jogador):
    """
    Executa o evento especial correto.
    Conecta GeraRun com os NPCs e lógicas de eventos.
    """
    import time

    if tipo_evento == "mercador":
        from systems.npcs import encontro_mercador
        encontro_mercador(jogador)

    elif tipo_evento == "elfo_ferido":
        from systems.npcs import encontro_elfo_ferido
        encontro_elfo_ferido(jogador)

    elif tipo_evento == "goblin_rei":
        from systems.npcs import encontro_goblin_rei
        encontro_goblin_rei(jogador)

    elif tipo_evento == "entidade":
        from systems.npcs import encontro_entidade
        encontro_entidade(jogador)

    elif tipo_evento == "armadilha":
        _evento_armadilha(jogador)

    elif tipo_evento == "inscricoes":
        _evento_inscricoes(jogador)

    elif tipo_evento == "altar":
        _evento_altar(jogador)

    elif tipo_evento == "eco_passado":
        _evento_eco_passado(jogador)

    elif tipo_evento == "prisioneiro":
        _evento_prisioneiro(jogador)


# --------------------------------------------------------------------------
# EVENTOS ATMOSFÉRICOS
# --------------------------------------------------------------------------

def _evento_armadilha(jogador):
    import time
    print("\n" + "=" * 60)
    print("  SALA DA ARMADILHA")
    print("=" * 60)
    time.sleep(1)
    print("\n  O chão range sob seus pés de forma estranha.")
    time.sleep(1)
    print("  Você para. Olha para baixo. Vê marcas de pressão.")
    time.sleep(1)

    print("\n  [1] Avançar com cuidado  — tenta desativar")
    print("  [2] Recuar e contornar   — perde tempo, ganha integridade")
    op = input("\n  >> ").strip()

    if op == "1":
        if random.randint(1, 2) == 1:
            print("\n  Você desativa a armadilha com precisão.")
            time.sleep(1)
            from items import gerar_loot_aleatorio
            recompensa = gerar_loot_aleatorio()
            jogador.adicionar_item(recompensa)
            print(f"  Encontrou: {recompensa}")
            memoria.registrar_evento(f"{jogador.nome} desativou armadilha.")
        else:
            dano = random.randint(15, 35)
            jogador.tomar_dano(dano)
            print(f"\n  A armadilha dispara. -{dano} HP")
            print(f"  Vida: {jogador.vida}/{jogador.vida_maxima}")
            memoria.registrar_evento(f"{jogador.nome} caiu em armadilha.")
    else:
        print("\n  Você contorna. A sala fica para trás.")
    time.sleep(2)


def _evento_inscricoes(jogador):
    import time
    print("\n" + "=" * 60)
    print("  SALA DAS INSCRIÇÕES")
    print("=" * 60)
    time.sleep(1)

    mortes = memoria.obter("mortes_totais", 0)
    runs   = memoria.obter("runs_iniciadas", 0)

    print("\n  Paredes cobertas de inscrições em uma língua que dói nos olhos para ler.")
    print("  Centenas delas. Milhares, talvez. Algumas tão antigas que a pedra se desgastou.")
    time.sleep(2)
    print("  Você olha com cuidado. Algumas parecem... impossível... FAMILIARES.")
    time.sleep(1)

    if runs > 1:
        print(f"\n  Uma das inscrições tem seu nome. Exatamente como você o escreve.")
        time.sleep(1)
        print(f"  Ao lado: datas. {mortes} datas de morte registradas em pedra.")
        time.sleep(1)
        print("  A masmorra não apenas lembra de você. Ela o documenta. Você é parte da história dela.")
        print("  Isto não é confortante.")
        memoria.registrar_evento(f"{jogador.nome} viu seu nome inscrito na parede.")
    else:
        print("\n  Uma inscrição em português antigo se destaca: 'O primeiro sempre esquece o caminho.'")
        time.sleep(1)
        print("  'Mas o segundo... o segundo LEMBRA.'")
        time.sleep(1)
        print("  Você não entende agora. Mas sente que vai entender, caro ou não.")

    time.sleep(2)
    jogador.ganhar_experiencia(25)
    print("\n  +25 XP (conhecimento da masmorra)")
    time.sleep(1)


def _evento_altar(jogador):
    import time
    print("\n" + "=" * 60)
    print("  ALTAR ANTIGO")
    print("=" * 60)
    time.sleep(1)

    print("\n  Um altar de pedra preta pulsa com luz violeta tênue.")
    time.sleep(1)
    print("  Você sente dois chamados: cura e maldição.")
    time.sleep(1)

    print("\n  [1] Fazer oferenda  — coloca um item")
    print("  [2] Beber da taça   — risco desconhecido")
    print("  [3] Destruir o altar")
    op = input("\n  >> ").strip()

    if op == "1" and jogador.inventario:
        jogador.inventario.pop(0)
        cura = random.randint(20, 60)
        jogador.curar(cura)
        print(f"\n  O altar aceita. Você é curado em {cura} HP.")
        memoria.registrar_evento(f"{jogador.nome} fez oferenda no altar.")

    elif op == "2":
        efeito = random.choice(["bom", "ruim", "neutro"])
        if efeito == "bom":
            jogador.forca += 3
            print("\n  Poder flui pelo seu corpo. Força +3")
        elif efeito == "ruim":
            dano = random.randint(20, 40)
            jogador.tomar_dano(dano)
            print(f"\n  Veneno. -{dano} HP")
        else:
            print("\n  Nada acontece. O altar observa.")

    elif op == "3":
        if memoria.obter("destruiu_caverna", False):
            print("\n  Você já destruiu antes. Sabe o que fazer.")
        print("\n  O altar racha. Uma onda de energia te empurra.")
        dano = random.randint(10, 25)
        jogador.tomar_dano(dano)
        print(f"  -{dano} HP mas o altar está destruído.")
        memoria.definir("destruiu_caverna", True)
        memoria.registrar_evento(f"{jogador.nome} destruiu um altar.")

    time.sleep(2)


def _evento_eco_passado(jogador):
    """
    GDD: "Memória persistente — sensação de mundo vivo."
    Evento atmosférico que mostra fragmentos de runs anteriores.
    """
    import time
    print("\n" + "=" * 60)
    print("  ECO DO PASSADO")
    print("=" * 60)
    time.sleep(1)

    mortes   = memoria.obter("mortes_totais", 0)
    diario   = memoria.diario_recente()

    print("\n  O corredor pisca.")
    time.sleep(1)
    print("  Por um instante, você vê uma sombra que reconhece.")
    time.sleep(1)
    print("  Você mesmo. Uma versão anterior. Morrendo.")
    time.sleep(2)

    if mortes == 1:
        print(f"\n  Você morreu uma vez aqui.")
    elif mortes > 1:
        print(f"\n  Você morreu {mortes} vezes aqui.")
        time.sleep(1)
        print("  E voltou todas elas.")

    time.sleep(1)
    print("\n  Fragmentos do que aconteceu antes:")
    print(diario)
    time.sleep(3)

    print("\n  A visão some. Você continua.")
    time.sleep(1)


def _evento_prisioneiro(jogador):
    import time
    print("\n" + "=" * 60)
    print("  PRISIONEIRO")
    print("=" * 60)
    time.sleep(1)

    print("\n  Correntes. Uma figura humana acorrentada à parede.")
    time.sleep(1)
    print("  Ela levanta a cabeça. Olhos vermelhos de tanto chorar.")
    time.sleep(1)
    print('  "Por favor... tire essas correntes."')
    time.sleep(1)

    print("\n  [1] Libertar o prisioneiro")
    print("  [2] Questionar antes de agir")
    print("  [3] Continuar andando")
    op = input("\n  >> ").strip()

    if op == "1":
        print("\n  Você força as correntes. Elas cedem.")
        time.sleep(1)
        r = random.choice(["grato", "armadilha"])
        if r == "grato":
            recompensa = random.randint(30, 80)
            jogador.adicionar_dinheiro(recompensa)
            print(f'  "Obrigado. Tenho isto." +{recompensa} gold')
            memoria.registrar_evento(f"{jogador.nome} libertou prisioneiro grato.")
        else:
            dano = random.randint(20, 40)
            jogador.tomar_dano(dano)
            print("  O prisioneiro sorri de forma errada. E ataca.")
            print(f"  -{dano} HP. Uma lição aprendida.")
            memoria.registrar_evento(f"{jogador.nome} caiu em armadilha do prisioneiro falso.")

    elif op == "2":
        print('\n  "Quem te prendeu?"')
        time.sleep(0.8)
        print('  "...Os mesmos que te perseguem."')
        time.sleep(1)
        print("  Você decide por conta própria.")

    else:
        print("\n  Você continua. O choro fica para trás.")
        time.sleep(1)
        print("  Uma escolha. Como todas as outras aqui.")
        memoria.registrar_evento(f"{jogador.nome} ignorou o prisioneiro.")

    time.sleep(2)

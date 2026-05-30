# ============================================================================
# NOUTRORA RPG — CLASSE PLAYER
# ============================================================================

from config import PLAYER_INICIAL, DINHEIRO_INICIAL, XP_LEVEL_BASE, XP_MULTIPLICADOR


class Player:
    """Representa o jogador em uma run de Noutrora."""

    def __init__(self, nome):
        self.nome          = nome
        self.vida          = PLAYER_INICIAL["vida"]
        self.vida_maxima   = PLAYER_INICIAL["vida"]
        self.forca         = PLAYER_INICIAL["forca"]
        self.velocidade    = PLAYER_INICIAL["velocidade"]
        self.experiencia   = 0
        self.nivel         = 1
        self.dinheiro      = DINHEIRO_INICIAL
        self.sala_atual    = 1          # Profundidade atual na run
        self.faccao        = "Sem Facção"

        # Inventário
        self.inventario    = []         # Itens consumíveis
        self.equipamentos  = []         # Equipamentos no inventário

        # Slots de equipamento
        self.arma_equipada       = None
        self.armadura_equipada   = None
        self.acessorio_equipado  = None

    # ------------------------------------------------------------------
    # VIDA
    # ------------------------------------------------------------------

    def tomar_dano(self, dano):
        self.vida = max(0, self.vida - dano)

    def curar(self, quantidade):
        anterior    = self.vida
        self.vida   = min(self.vida + quantidade, self.vida_maxima)
        return self.vida - anterior

    def esta_vivo(self):
        return self.vida > 0

    # ------------------------------------------------------------------
    # ITENS CONSUMÍVEIS
    # ------------------------------------------------------------------

    def adicionar_item(self, item):
        self.inventario.append(item)

    def usar_item(self, indice):
        if 0 <= indice < len(self.inventario):
            item = self.inventario.pop(indice)
            return item.aplicar_efeito(self)
        return "Item inválido!"

    def listar_inventario(self):
        if not self.inventario:
            return "  Inventário de itens: vazio"
        linhas = ["  Itens:"]
        for i, item in enumerate(self.inventario):
            linhas.append(f"    [{i}] {item}")
        return "\n".join(linhas)

    # ------------------------------------------------------------------
    # EQUIPAMENTOS
    # ------------------------------------------------------------------

    def adicionar_equipamento(self, equip):
        self.equipamentos.append(equip)

    def equipar(self, indice):
        if not (0 <= indice < len(self.equipamentos)):
            return "Equipamento inválido!"
        equip = self.equipamentos[indice]
        slot  = equip.tipo

        if slot == "arma":
            if self.arma_equipada:
                self.equipamentos.append(self.arma_equipada)
            self.arma_equipada = equip
        elif slot == "armadura":
            if self.armadura_equipada:
                self.equipamentos.append(self.armadura_equipada)
            self.armadura_equipada = equip
        elif slot == "acessorio":
            if self.acessorio_equipado:
                self.equipamentos.append(self.acessorio_equipado)
            self.acessorio_equipado = equip

        self.equipamentos.pop(indice)
        return f"Equipou {equip.nome}!"

    def calcular_bonus_equipamentos(self):
        f_bonus = 0
        v_bonus = 0
        for slot in [self.arma_equipada, self.armadura_equipada, self.acessorio_equipado]:
            if slot:
                b = slot.obter_bonus_total()
                f_bonus += b["forca"]
                v_bonus += b["velocidade"]
        return f_bonus, v_bonus

    def obter_forca_total(self):
        b, _ = self.calcular_bonus_equipamentos()
        return self.forca + b

    def obter_velocidade_total(self):
        _, b = self.calcular_bonus_equipamentos()
        return max(0, self.velocidade + b)

    def listar_equipamentos(self):
        linhas = ["  Equipamentos:"]
        if self.arma_equipada:
            linhas.append(f"    [arma]     {self.arma_equipada.nome}")
        if self.armadura_equipada:
            linhas.append(f"    [armadura] {self.armadura_equipada.nome}")
        if self.acessorio_equipado:
            linhas.append(f"    [acesso.]  {self.acessorio_equipado.nome}")
        if self.equipamentos:
            linhas.append("  Disponíveis:")
            for i, e in enumerate(self.equipamentos):
                linhas.append(f"    [{i}] {e}")
        return "\n".join(linhas)

    # ------------------------------------------------------------------
    # DINHEIRO
    # ------------------------------------------------------------------

    def adicionar_dinheiro(self, qtd):
        self.dinheiro += qtd

    def remover_dinheiro(self, qtd):
        if self.dinheiro >= qtd:
            self.dinheiro -= qtd
            return True
        return False

    # ------------------------------------------------------------------
    # PROGRESSÃO
    # ------------------------------------------------------------------

    def ganhar_experiencia(self, qtd):
        self.experiencia += qtd
        self._checar_level_up()

    def _checar_level_up(self):
        xp_necessario = int(XP_LEVEL_BASE * (XP_MULTIPLICADOR ** (self.nivel - 1)))
        if self.experiencia >= xp_necessario:
            self.nivel       += 1
            self.experiencia -= xp_necessario
            self.forca       += 2
            self.velocidade  += 1
            self.vida_maxima += 15
            self.vida         = min(self.vida + 15, self.vida_maxima)
            print(f"\n  *** LEVEL UP! Nível {self.nivel} ***")
            print(f"  Força +2 | Velocidade +1 | Vida máxima +15")

    # ------------------------------------------------------------------
    # STATUS
    # ------------------------------------------------------------------

    def obter_status(self):
        ft, vt = self.calcular_bonus_equipamentos()
        return {
            "nome":              self.nome,
            "vida":              self.vida,
            "vida_maxima":       self.vida_maxima,
            "forca":             self.forca,
            "forca_total":       self.obter_forca_total(),
            "velocidade":        self.velocidade,
            "velocidade_total":  self.obter_velocidade_total(),
            "nivel":             self.nivel,
            "experiencia":       self.experiencia,
            "dinheiro":          self.dinheiro,
            "faccao":            self.faccao,
            "sala_atual":        self.sala_atual,
        }

    def __str__(self):
        return (
            f"{self.nome} | Nível {self.nivel} | "
            f"Vida {self.vida}/{self.vida_maxima} | "
            f"Força {self.obter_forca_total()} | "
            f"Vel {self.obter_velocidade_total()} | "
            f"Gold {self.dinheiro}"
        )

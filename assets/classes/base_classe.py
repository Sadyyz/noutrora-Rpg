# ============================================================================
# NOUTRORA RPG — CLASSE BASE DE TODAS AS CLASSES JOGÁVEIS
# ============================================================================
# Toda classe herda de Player E desta base.
# Define a interface de habilidades que o sistema de combate usa.
# ============================================================================

import time
import random


class BaseClasse:
    """
    Mixin de habilidades. Toda classe jogável herda daqui além de Player.
    Define:
      - self.habilidades : lista de Habilidade
      - self.mana / self.mana_maxima  (recurso de habilidades)
      - usar_habilidade(indice, alvo)
      - listar_habilidades()
      - turno_passivo()  — efeitos que rodam no fim de cada turno
    """

    def _init_habilidades(self, mana_max=50):
        self.mana         = mana_max
        self.mana_maxima  = mana_max
        self.habilidades  = []           # Populado por cada subclasse
        # Efeitos ativos (duração em turnos)
        self._efeitos     = {}           # {"nome": {"dano": x, "turnos": n, ...}}

    # ------------------------------------------------------------------
    # MANA
    # ------------------------------------------------------------------

    def recuperar_mana(self, qtd):
        self.mana = min(self.mana + qtd, self.mana_maxima)

    def gastar_mana(self, custo):
        if self.mana >= custo:
            self.mana -= custo
            return True
        return False

    # ------------------------------------------------------------------
    # HABILIDADES
    # ------------------------------------------------------------------

    def listar_habilidades(self):
        if not self.habilidades:
            return "  Nenhuma habilidade disponível."
        linhas = ["  Habilidades:"]
        for i, h in enumerate(self.habilidades):
            disponivel = "OK" if self.mana >= h.custo else "--"
            linhas.append(
                f"    [{i}] [{disponivel}] {h.nome}  "
                f"(custo: {h.custo} mana)  — {h.descricao}"
            )
        return "\n".join(linhas)

    def usar_habilidade(self, indice, alvo):
        """
        Executa a habilidade no índice dado contra 'alvo' (inimigo).
        Retorna string com resultado narrativo.
        """
        if not (0 <= indice < len(self.habilidades)):
            return "Habilidade inválida."
        hab = self.habilidades[indice]
        if not self.gastar_mana(hab.custo):
            return f"Mana insuficiente. ({self.mana}/{hab.custo} necessário)"
        return hab.executar(self, alvo)

    # ------------------------------------------------------------------
    # EFEITOS POR TURNO (veneno, sangramento, regeneração...)
    # ------------------------------------------------------------------

    def aplicar_efeito(self, nome, dados):
        """
        Registra um efeito de duração.
        dados = {"tipo": "dano"/"cura", "valor": int, "turnos": int, "descricao": str}
        """
        self._efeitos[nome] = dados.copy()

    def turno_passivo(self):
        """
        Chamado no início de cada turno de combate.
        Processa efeitos ativos e retorna lista de mensagens.
        """
        msgs  = []
        vazar = []
        for nome, ef in self._efeitos.items():
            if ef["tipo"] == "dano":
                self.tomar_dano(ef["valor"])
                msgs.append(f"  [{nome}] -{ef['valor']} HP  ({ef['turnos']-1} turnos restantes)")
            elif ef["tipo"] == "cura":
                real = self.curar(ef["valor"])
                msgs.append(f"  [{nome}] +{real} HP  ({ef['turnos']-1} turnos restantes)")
            ef["turnos"] -= 1
            if ef["turnos"] <= 0:
                vazar.append(nome)
        for nome in vazar:
            del self._efeitos[nome]
            msgs.append(f"  [{nome}] efeito encerrado.")
        return msgs

    def efeitos_ativos(self):
        return list(self._efeitos.keys())


# ============================================================================
# CLASSE HABILIDADE — representa uma habilidade individual
# ============================================================================

class Habilidade:
    """
    Uma habilidade usável em combate.
    executar(usuario, alvo) → str com resultado narrativo.
    """

    def __init__(self, nome, descricao, custo, fn_executar):
        """
        Args:
            nome       : str
            descricao  : str curta para o menu
            custo      : int (mana)
            fn_executar: callable(usuario, alvo) → str
        """
        self.nome      = nome
        self.descricao = descricao
        self.custo     = custo
        self._fn       = fn_executar

    def executar(self, usuario, alvo):
        return self._fn(usuario, alvo)

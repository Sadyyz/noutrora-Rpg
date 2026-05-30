# ============================================================================
# NOUTRORA RPG — SISTEMA DE MEMÓRIA PERSISTENTE
# ============================================================================
# GDD: "NPCs lembram escolhas, ajuda, traições, mortes, ações passadas."
# GDD: "Isso cria conexão emocional, consequências persistentes, mundo vivo."
#
# A Memória é separada do Save normal — ela persiste ENTRE runs diferentes.
# O jogador morre → salva → começa nova run → NPCs ainda se lembram.
# ============================================================================

import json
import os
from config import MEMORIA_KEYS

MEMORIA_PATH = os.path.join(os.path.dirname(__file__), "data", "memoria.json")


class Memoria:
    """
    Gerencia a memória persistente do mundo entre todas as runs.
    Instância única que existe além da morte do jogador.
    """

    def __init__(self):
        self._dados = self._carregar()

    # ------------------------------------------------------------------
    # PERSISTÊNCIA
    # ------------------------------------------------------------------

    def _carregar(self):
        """Carrega memória do arquivo ou cria uma vazia."""
        os.makedirs(os.path.dirname(MEMORIA_PATH), exist_ok=True)
        if os.path.exists(MEMORIA_PATH):
            try:
                with open(MEMORIA_PATH, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                pass
        return self._padrao()

    def _padrao(self):
        """Retorna estrutura de memória vazia (primeira run de todos os tempos)."""
        return {
            # Booleanos de escolha
            "ajudou_mercador":      False,
            "traiu_goblin_rei":     False,
            "salvou_elfo":          False,
            "destruiu_caverna":     False,
            "pacto_demonio":        False,
            # Contadores históricos
            "mortes_totais":        0,
            "runs_completadas":     0,
            "runs_iniciadas":       0,
            "maior_sala_alcancada": 0,
            "inimigos_derrotados":  0,
            # Facção e identidade
            "faccao_escolhida":     "Sem Facção",
            # Log narrativo (últimas 5 ações memoráveis)
            "diario": [],
        }

    def salvar(self):
        """Persiste a memória no disco."""
        os.makedirs(os.path.dirname(MEMORIA_PATH), exist_ok=True)
        with open(MEMORIA_PATH, "w", encoding="utf-8") as f:
            json.dump(self._dados, f, ensure_ascii=False, indent=2)

    # ------------------------------------------------------------------
    # INTERFACE PÚBLICA
    # ------------------------------------------------------------------

    def obter(self, chave, padrao=None):
        return self._dados.get(chave, padrao)

    def definir(self, chave, valor):
        self._dados[chave] = valor
        self.salvar()

    def incrementar(self, chave, quantidade=1):
        atual = self._dados.get(chave, 0)
        self._dados[chave] = atual + quantidade
        self.salvar()

    def registrar_evento(self, texto):
        """
        Adiciona ao diário narrativo (mantém só os últimos 10 eventos).
        GDD: "Sensação de mundo vivo."
        """
        diario = self._dados.get("diario", [])
        diario.append(texto)
        if len(diario) > 10:
            diario = diario[-10:]
        self._dados["diario"] = diario
        self.salvar()

    # ------------------------------------------------------------------
    # QUERIES NARRATIVAS — usadas pelos NPCs para modificar diálogos
    # ------------------------------------------------------------------

    def primeira_vez(self):
        """True se esta é a primeira run de todos os tempos."""
        return self._dados.get("runs_iniciadas", 0) == 0

    def e_veterano(self):
        """True se o jogador já morreu ao menos uma vez."""
        return self._dados.get("mortes_totais", 0) > 0

    def mercador_reconhece(self):
        """Mercador reconhece e ajuda se foi ajudado antes."""
        return self._dados.get("ajudou_mercador", False)

    def elfo_deve_favor(self):
        """Elfo deve favor se foi salvo em run anterior."""
        return self._dados.get("salvou_elfo", False)

    def goblin_rei_desconfia(self):
        """Rei Goblin desconfia se foi traído antes."""
        return self._dados.get("traiu_goblin_rei", False)

    def resumo_runs(self):
        """Retorna texto narrativo sobre histórico do jogador."""
        mortes    = self._dados.get("mortes_totais", 0)
        runs      = self._dados.get("runs_iniciadas", 0)
        profund   = self._dados.get("maior_sala_alcancada", 0)
        inimigos  = self._dados.get("inimigos_derrotados", 0)
        faccao    = self._dados.get("faccao_escolhida", "Sem Facção")

        if runs == 0:
            return "Primeira vez aqui. O mundo não te conhece ainda."

        linhas = [
            f"  Runs iniciadas  : {runs}",
            f"  Mortes          : {mortes}",
            f"  Profundidade rec: Sala {profund}",
            f"  Inimigos mortos : {inimigos}",
            f"  Última facção   : {faccao}",
        ]
        return "\n".join(linhas)

    def diario_recente(self):
        """Retorna os últimos eventos do diário."""
        diario = self._dados.get("diario", [])
        if not diario:
            return "Nenhum evento registrado."
        return "\n".join(f"  • {e}" for e in diario[-5:])

    # ------------------------------------------------------------------
    # LIMPEZA (reset de memória — ação narrativa importante)
    # ------------------------------------------------------------------

    def resetar_tudo(self):
        """
        Apaga toda a memória. Ação narrativa de peso:
        o mundo esquece quem você foi.
        """
        self._dados = self._padrao()
        self.salvar()


# Instância global — importada por todos os módulos
memoria = Memoria()

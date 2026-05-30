# ============================================================================
# NOUTRORA RPG — SISTEMA DE SAVE/LOAD
# ============================================================================
# Save guarda o estado da RUN ATUAL.
# Memória (systems/memoria.py) guarda o estado HISTÓRICO entre todas as runs.
# ============================================================================

import json
import os

SAVE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "save.json")


def salvar_jogo(jogador):
    """
    Persiste o estado atual do jogador no disco.

    Args:
        jogador (Player): instância do jogador
    """
    os.makedirs(os.path.dirname(SAVE_PATH), exist_ok=True)

    dados = {
        "nome":           jogador.nome,
        "vida":           jogador.vida,
        "vida_maxima":    jogador.vida_maxima,
        "forca":          jogador.forca,
        "velocidade":     jogador.velocidade,
        "experiencia":    jogador.experiencia,
        "nivel":          jogador.nivel,
        "dinheiro":       jogador.dinheiro,
        "sala_atual":     getattr(jogador, "sala_atual", 1),
        "faccao":         getattr(jogador, "faccao", "Sem Facção"),
        "inventario":     _serializar_inventario(jogador.inventario),
        "equipamentos":   _serializar_equipamentos(jogador),
    }

    with open(SAVE_PATH, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

    print("\n  [ save registrado ]")


def carregar_jogo():
    """
    Carrega save do disco e reconstrói o jogador.

    Returns:
        Player | None: jogador reconstituído ou None se não há save
    """
    if not os.path.exists(SAVE_PATH):
        print("\n  Nenhum save encontrado.")
        return None

    try:
        with open(SAVE_PATH, "r", encoding="utf-8") as f:
            dados = json.load(f)
    except (json.JSONDecodeError, IOError):
        print("\n  Save corrompido.")
        return None

    # Importação local para evitar ciclo
    from player import Player

    jogador = Player(dados["nome"])
    jogador.vida          = dados.get("vida", 100)
    jogador.vida_maxima   = dados.get("vida_maxima", 100)
    jogador.forca         = dados.get("forca", 10)
    jogador.velocidade    = dados.get("velocidade", 5)
    jogador.experiencia   = dados.get("experiencia", 0)
    jogador.nivel         = dados.get("nivel", 1)
    jogador.dinheiro      = dados.get("dinheiro", 500)
    jogador.sala_atual    = dados.get("sala_atual", 1)
    jogador.faccao        = dados.get("faccao", "Sem Facção")

    return jogador


def deletar_save():
    """Remove o save atual (morte permanente)."""
    if os.path.exists(SAVE_PATH):
        os.remove(SAVE_PATH)


def save_existe():
    """Verifica se existe um save."""
    return os.path.exists(SAVE_PATH)


# ------------------------------------------------------------------
# HELPERS DE SERIALIZAÇÃO
# ------------------------------------------------------------------

def _serializar_inventario(inventario):
    itens = []
    for item in inventario:
        itens.append({
            "nome":         item.nome,
            "raridade":     item.raridade,
            "efeito_tipo":  item.efeito_tipo,
            "valor_efeito": item.valor_efeito,
        })
    return itens


def _serializar_equipamentos(jogador):
    equipados = {}
    if jogador.arma_equipada:
        equipados["arma"] = jogador.arma_equipada.nome
    if jogador.armadura_equipada:
        equipados["armadura"] = jogador.armadura_equipada.nome
    if jogador.acessorio_equipado:
        equipados["acessorio"] = jogador.acessorio_equipado.nome
    return equipados

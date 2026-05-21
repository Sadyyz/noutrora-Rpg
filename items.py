# ============================================================================
# SISTEMA DE ITENS
# ============================================================================
# Define todos os itens do jogo, seus efeitos e raridades.

import random


class Item:
    """Classe base para itens do jogo."""
    
    def __init__(self, nome, descricao, raridade, efeito_tipo, valor_efeito):
        """
        Args:
            nome (str): Nome do item
            descricao (str): Descrição do que faz
            raridade (str): "comum", "raro", "épico", "lendário"
            efeito_tipo (str): "cura", "forca", "velocidade"
            valor_efeito (int): Quantidade de efeito
        """
        self.nome = nome
        self.descricao = descricao
        self.raridade = raridade
        self.efeito_tipo = efeito_tipo
        self.valor_efeito = valor_efeito
    
    def __repr__(self):
        cores = {
            "comum": "⚪",
            "raro": "🔵",
            "épico": "🟣",
            "lendário": "🟡"
        }
        return f"{cores.get(self.raridade, '')} {self.nome} ({self.raridade})"
    
    def aplicar_efeito(self, jogador):
        """Aplica o efeito do item ao jogador."""
        if self.efeito_tipo == "cura":
            vida_anterior = jogador.vida
            jogador.vida = min(jogador.vida + self.valor_efeito, jogador.vida_maxima)
            cura_real = jogador.vida - vida_anterior
            return f"Você foi curado em {cura_real} pontos de vida!"
        
        elif self.efeito_tipo == "forca":
            jogador.forca += self.valor_efeito
            return f"Sua força aumentou em {self.valor_efeito}!"
        
        elif self.efeito_tipo == "velocidade":
            jogador.velocidade += self.valor_efeito
            return f"Sua velocidade aumentou em {self.valor_efeito}!"
        
        return "Item aplicado."


# ============================================================================
# CATÁLOGO DE ITENS POR RARIDADE
# ============================================================================

ITENS_COMUNS = [
    Item("Pão", "Cura básica", "comum", "cura", 20),
    Item("Maçã", "Uma maçã fresca", "comum", "cura", 15),
    Item("Erva Medicinal", "Cura simples", "comum", "cura", 25),
]

ITENS_RAROS = [
    Item("Frasco de Elixir", "Cura potente", "raro", "cura", 50),
    Item("Espada de Ferro", "Aumenta força", "raro", "forca", 3),
    Item("Botas Mágicas", "Aumenta velocidade", "raro", "velocidade", 2),
]

ITENS_EPICOS = [
    Item("Poção Divina", "Cura completa", "épico", "cura", 100),
    Item("Espada Flamejante", "Força massiva", "épico", "forca", 6),
    Item("Capa da Velocidade", "Velocidade extrema", "épico", "velocidade", 4),
]

ITENS_LENDARIOS = [
    Item("Elixir da Eternidade", "Cura suprema", "lendário", "cura", 150),
    Item("Excalibur", "Força lendária", "lendário", "forca", 10),
    Item("Bota de Hermes", "Velocidade divina", "lendário", "velocidade", 6),
]

# Dicionário centralizado de todos os itens
TODOS_ITENS = {
    "comum": ITENS_COMUNS,
    "raro": ITENS_RAROS,
    "épico": ITENS_EPICOS,
    "lendário": ITENS_LENDARIOS,
}


def gerar_loot_aleatorio():
    """
    Gera um item aleatório do loot.
    Maior chance de comum, menor de lendário (segue distribuição realista).
    
    Returns:
        Item: Item gerado aleatoriamente
    """
    probabilidades = random.randint(1, 100)
    
    if probabilidades <= 60:  # 60% comum
        return random.choice(ITENS_COMUNS)
    elif probabilidades <= 85:  # 25% raro
        return random.choice(ITENS_RAROS)
    elif probabilidades <= 98:  # 13% épico
        return random.choice(ITENS_EPICOS)
    else:  # 2% lendário
        return random.choice(ITENS_LENDARIOS)


def gerar_multiplos_itens(quantidade=3):
    """
    Gera múltiplos itens (para baús).
    
    Args:
        quantidade (int): Quantos itens gerar
        
    Returns:
        list: Lista de itens
    """
    return [gerar_loot_aleatorio() for _ in range(quantidade)]

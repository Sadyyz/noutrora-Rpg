# ============================================================================
# SISTEMA DE EQUIPAMENTOS
# ============================================================================
# Define equipamentos (armas, armaduras) e seu sistema de upgrade

class Equipamento:
    """Representa um equipamento (arma, armadura, etc)."""
    
    def __init__(self, nome, tipo, descricao, bonus_forca=0, bonus_velocidade=0, preco=0, raridade="comum"):
        """
        Args:
            nome (str): Nome do equipamento
            tipo (str): "arma", "armadura", "acessorio"
            descricao (str): Descrição
            bonus_forca (int): Bônus de força
            bonus_velocidade (int): Bônus de velocidade
            preco (int): Preço em moeda
            raridade (str): "comum", "raro", "épico", "lendário"
        """
        self.nome = nome
        self.tipo = tipo
        self.descricao = descricao
        self.bonus_forca = bonus_forca
        self.bonus_velocidade = bonus_velocidade
        self.preco = preco
        self.raridade = raridade
        self.nivel_upgrade = 1  # Nível de upgrade (1-10)
    
    def fazer_upgrade(self):
        """Melhora o equipamento em um nível."""
        if self.nivel_upgrade < 10:
            self.nivel_upgrade += 1
            self.bonus_forca += 1
            self.bonus_velocidade += 1
            return True
        return False
    
    def obter_bonus_total(self):
        """Retorna bonus total considerando nível de upgrade."""
        return {
            "forca": self.bonus_forca + (self.nivel_upgrade - 1) // 2,
            "velocidade": self.bonus_velocidade + (self.nivel_upgrade - 1) // 3,
        }
    
    def __repr__(self):
        cores = {
            "comum": "⚪",
            "raro": "🔵",
            "épico": "🟣",
            "lendário": "🟡"
        }
        icon = cores.get(self.raridade, '')
        nivel = f" +{self.nivel_upgrade}" if self.nivel_upgrade > 1 else ""
        return f"{icon} {self.nome}{nivel} ({self.tipo})"
    
    def obter_status(self):
        """Retorna dicionário com informações do equipamento."""
        bonus = self.obter_bonus_total()
        return {
            "nome": self.nome,
            "tipo": self.tipo,
            "raridade": self.raridade,
            "nivel": self.nivel_upgrade,
            "bonus_forca": bonus["forca"],
            "bonus_velocidade": bonus["velocidade"],
            "preco": self.preco,
        }


# ============================================================================
# CATÁLOGO DE EQUIPAMENTOS
# ============================================================================

# ARMAS
ARMAS_COMUNS = [
    Equipamento("Espada Ferrugenta", "arma", "Espada antiga e desgastada", bonus_forca=2, bonus_velocidade=0, preco=50, raridade="comum"),
    Equipamento("Adaga Simples", "arma", "Uma adaga de ferro", bonus_forca=1, bonus_velocidade=2, preco=40, raridade="comum"),
]

ARMAS_RARAS = [
    Equipamento("Espada de Ferro", "arma", "Uma bela espada de ferro", bonus_forca=4, bonus_velocidade=1, preco=150, raridade="raro"),
    Equipamento("Machado de Batalha", "arma", "Pesado mas devastador", bonus_forca=6, bonus_velocidade=-1, preco=180, raridade="raro"),
]

ARMAS_EPICAS = [
    Equipamento("Espada Flamejante", "arma", "Chamas envolvem a lâmina", bonus_forca=8, bonus_velocidade=2, preco=400, raridade="épico"),
    Equipamento("Lança Divina", "arma", "Uma arma dos deuses", bonus_forca=7, bonus_velocidade=3, preco=420, raridade="épico"),
]

ARMAS_LENDARIAS = [
    Equipamento("Excalibur", "arma", "A lendária espada suprema", bonus_forca=12, bonus_velocidade=3, preco=1000, raridade="lendário"),
    Equipamento("Mjolnir", "arma", "O martelo do trovão", bonus_forca=14, bonus_velocidade=0, preco=1200, raridade="lendário"),
]

# ARMADURAS
ARMADURAS_COMUNS = [
    Equipamento("Armadura de Couro", "armadura", "Proteção básica", bonus_forca=0, bonus_velocidade=-1, preco=60, raridade="comum"),
]

ARMADURAS_RARAS = [
    Equipamento("Armadura de Ferro", "armadura", "Proteção sólida", bonus_forca=1, bonus_velocidade=-2, preco=200, raridade="raro"),
    Equipamento("Armadura de Aço", "armadura", "Bem forjada e durável", bonus_forca=2, bonus_velocidade=-1, preco=220, raridade="raro"),
]

ARMADURAS_EPICAS = [
    Equipamento("Armadura de Mithril", "armadura", "Metal mágico leve", bonus_forca=3, bonus_velocidade=1, preco=500, raridade="épico"),
]

ARMADURAS_LENDARIAS = [
    Equipamento("Armadura Celestial", "armadura", "Proteção divina", bonus_forca=5, bonus_velocidade=2, preco=1500, raridade="lendário"),
]

# ACESSÓRIOS
ACESSORIOS_COMUNS = [
    Equipamento("Anel de Ferro", "acessorio", "Um anel simples", bonus_forca=1, bonus_velocidade=0, preco=40, raridade="comum"),
]

ACESSORIOS_RAROS = [
    Equipamento("Anel de Poder", "acessorio", "Um anel poderoso", bonus_forca=3, bonus_velocidade=1, preco=150, raridade="raro"),
]

ACESSORIOS_EPICOS = [
    Equipamento("Anel da Sabedoria", "acessorio", "Conhecimento infinito", bonus_forca=2, bonus_velocidade=4, preco=400, raridade="épico"),
]

ACESSORIOS_LENDARIOS = [
    Equipamento("Anel do Infinito", "acessorio", "Poder absoluto", bonus_forca=6, bonus_velocidade=6, preco=2000, raridade="lendário"),
]

# Dicionário centralizado
CATALOGO_EQUIPAMENTOS = {
    "arma": {
        "comum": ARMAS_COMUNS,
        "raro": ARMAS_RARAS,
        "épico": ARMAS_EPICAS,
        "lendário": ARMAS_LENDARIAS,
    },
    "armadura": {
        "comum": ARMADURAS_COMUNS,
        "raro": ARMADURAS_RARAS,
        "épico": ARMADURAS_EPICAS,
        "lendário": ARMADURAS_LENDARIAS,
    },
    "acessorio": {
        "comum": ACESSORIOS_COMUNS,
        "raro": ACESSORIOS_RAROS,
        "épico": ACESSORIOS_EPICOS,
        "lendário": ACESSORIOS_LENDARIOS,
    }
}


def obter_equipamento_aleatorio():
    """Gera um equipamento aleatório para venda."""
    import random
    probabilidade = random.randint(1, 100)
    
    # 60% comum, 25% raro, 13% épico, 2% lendário
    if probabilidade <= 60:
        raridade = "comum"
    elif probabilidade <= 85:
        raridade = "raro"
    elif probabilidade <= 98:
        raridade = "épico"
    else:
        raridade = "lendário"
    
    tipo = random.choice(["arma", "armadura", "acessorio"])
    return random.choice(CATALOGO_EQUIPAMENTOS[tipo][raridade])


def obter_equipamentos_venda(quantidade=5):
    """Gera múltiplos equipamentos para venda na loja."""
    return [obter_equipamento_aleatorio() for _ in range(quantidade)]

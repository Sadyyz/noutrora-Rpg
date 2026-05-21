# ============================================================================
# CLASSE PLAYER - Encapsula toda a lógica do jogador
# ============================================================================
# Por que usar classe? Dados + comportamento juntos, fácil adicionar métodos
# novas propriedades (experiência, itens, etc.) sem quebrar o resto do código.

from config import PLAYER_INICIAL


class Player:
    """Representa o jogador na masmorra."""

    def __init__(self, nome):
        """
        Inicializa o jogador com nome e atributos.
        
        Args:
            nome (str): Nome do jogador
        """
        self.nome = nome
        self.vida = PLAYER_INICIAL["vida"]
        self.vida_maxima = PLAYER_INICIAL["vida"]
        self.forca = PLAYER_INICIAL["forca"]
        self.velocidade = PLAYER_INICIAL["velocidade"]
        self.inventario = []  # Lista de itens (consumíveis)
        self.experiencia = 0
        self.nivel = 1
        
        # NOVO: Sistema de equipamento
        self.dinheiro = 500  # Moeda inicial
        self.arma_equipada = None  # Equipamento de arma
        self.armadura_equipada = None  # Equipamento de armadura
        self.acessorio_equipado = None  # Equipamento de acessório
        self.equipamentos = []  # Equipamentos no inventário

    def tomar_dano(self, dano):
        """
        Jogador recebe dano. Não pode ficar com vida negativa.
        
        Args:
            dano (int): Quantidade de dano recebido
        """
        self.vida -= dano
        if self.vida < 0:
            self.vida = 0

    def curar(self, quantidade):
        """
        Cura o jogador até o máximo.
        
        Args:
            quantidade (int): Quantidade de cura
        """
        vida_anterior = self.vida
        self.vida = min(self.vida + quantidade, self.vida_maxima)
        return self.vida - vida_anterior

    def esta_vivo(self):
        """Verifica se o jogador está vivo."""
        return self.vida > 0

    # ========== SISTEMA DE ITENS CONSUMÍVEIS ==========
    
    def adicionar_item(self, item):
        """
        Adiciona um item consumível ao inventário.
        
        Args:
            item (Item): O item a adicionar
        """
        self.inventario.append(item)

    def usar_item(self, indice):
        """
        Usa um item consumível do inventário.
        
        Args:
            indice (int): Índice do item no inventário
            
        Returns:
            str: Mensagem de efeito do item
        """
        if 0 <= indice < len(self.inventario):
            item = self.inventario.pop(indice)
            return item.aplicar_efeito(self)
        return "Item inválido!"

    def listar_inventario(self):
        """Retorna string com a lista de itens consumíveis do inventário."""
        if not self.inventario:
            return "Inventário de itens: vazio"
        
        lista = "Seu Inventário (Itens):\n"
        for i, item in enumerate(self.inventario):
            lista += f"  [{i}] {item}\n"
        return lista

    # ========== SISTEMA DE EQUIPAMENTOS ==========
    
    def adicionar_equipamento(self, equip):
        """
        Adiciona um equipamento ao inventário de equipamentos.
        
        Args:
            equip (Equipamento): O equipamento a adicionar
        """
        self.equipamentos.append(equip)
    
    def equipar(self, indice):
        """
        Equipa um equipamento do inventário.
        
        Args:
            indice (int): Índice do equipamento
            
        Returns:
            str: Mensagem de equipamento
        """
        if 0 <= indice < len(self.equipamentos):
            equip = self.equipamentos[indice]
            tipo = equip.tipo
            
            if tipo == "arma":
                antigo = self.arma_equipada
                self.arma_equipada = equip
                self.equipamentos.pop(indice)
                if antigo:
                    self.equipamentos.append(antigo)
                return f"✅ Equipou {equip.nome}!"
            
            elif tipo == "armadura":
                antigo = self.armadura_equipada
                self.armadura_equipada = equip
                self.equipamentos.pop(indice)
                if antigo:
                    self.equipamentos.append(antigo)
                return f"✅ Equipou {equip.nome}!"
            
            elif tipo == "acessorio":
                antigo = self.acessorio_equipado
                self.acessorio_equipado = equip
                self.equipamentos.pop(indice)
                if antigo:
                    self.equipamentos.append(antigo)
                return f"✅ Equipou {equip.nome}!"
        
        return "Equipamento inválido!"
    
    def fazer_upgrade_equipamento(self, indice_equip, quantidade_itens=1):
        """
        Melhora um equipamento usando itens consumíveis.
        
        Args:
            indice_equip (int): Índice do equipamento
            quantidade_itens (int): Quantos itens usar para upgrade
            
        Returns:
            str: Mensagem de resultado
        """
        if len(self.inventario) < quantidade_itens:
            return "❌ Você não tem itens suficientes para upgrade!"
        
        if 0 <= indice_equip < len(self.equipamentos):
            equip = self.equipamentos[indice_equip]
            
            # Remover itens consumidos
            for _ in range(quantidade_itens):
                self.inventario.pop(0)
            
            # Fazer upgrade
            if equip.fazer_upgrade():
                return f"⬆️  {equip.nome} melhorou para nível {equip.nivel_upgrade}!"
            else:
                return f"❌ {equip.nome} já está no nível máximo!"
        
        return "Equipamento inválido!"
    
    def listar_equipamentos(self):
        """Retorna string com lista de equipamentos."""
        lista = "Seu Inventário (Equipamentos):\n"
        
        if self.arma_equipada:
            lista += f"  🗡️  EQUIPADA: {self.arma_equipada}\n"
        if self.armadura_equipada:
            lista += f"  🛡️  EQUIPADA: {self.armadura_equipada}\n"
        if self.acessorio_equipado:
            lista += f"  💍 EQUIPADA: {self.acessorio_equipado}\n"
        
        if self.equipamentos:
            lista += "\n  Disponíveis:\n"
            for i, equip in enumerate(self.equipamentos):
                lista += f"    [{i}] {equip}\n"
        else:
            lista += "\n  (Nenhum equipamento disponível)\n"
        
        return lista
    
    def calcular_bonus_equipamentos(self):
        """Calcula bônus totais de todos os equipamentos equipados."""
        forca_bonus = 0
        velocidade_bonus = 0
        
        if self.arma_equipada:
            bonus = self.arma_equipada.obter_bonus_total()
            forca_bonus += bonus["forca"]
            velocidade_bonus += bonus["velocidade"]
        
        if self.armadura_equipada:
            bonus = self.armadura_equipada.obter_bonus_total()
            forca_bonus += bonus["forca"]
            velocidade_bonus += bonus["velocidade"]
        
        if self.acessorio_equipado:
            bonus = self.acessorio_equipado.obter_bonus_total()
            forca_bonus += bonus["forca"]
            velocidade_bonus += bonus["velocidade"]
        
        return forca_bonus, velocidade_bonus
    
    def obter_forca_total(self):
        """Retorna força total com bônus de equipamento."""
        bonus_f, _ = self.calcular_bonus_equipamentos()
        return self.forca + bonus_f
    
    def obter_velocidade_total(self):
        """Retorna velocidade total com bônus de equipamento."""
        _, bonus_v = self.calcular_bonus_equipamentos()
        return max(0, self.velocidade + bonus_v)  # Nunca negativa
    
    # ========== SISTEMA DE DINHEIRO ==========
    
    def adicionar_dinheiro(self, quantidade):
        """
        Adiciona dinheiro (moeda).
        
        Args:
            quantidade (int): Quantidade a adicionar
        """
        self.dinheiro += quantidade
    
    def remover_dinheiro(self, quantidade):
        """
        Remove dinheiro.
        
        Args:
            quantidade (int): Quantidade a remover
            
        Returns:
            bool: True se tinha dinheiro suficiente
        """
        if self.dinheiro >= quantidade:
            self.dinheiro -= quantidade
            return True
        return False
    
    # ========== EXPERIÊNCIA ==========

    def ganhar_experiencia(self, quantidade):
        """
        Ganha experiência.
        
        Args:
            quantidade (int): Experiência ganha
        """
        self.experiencia += quantidade

    def obter_status(self):
        """Retorna dicionário com status atual (para exibição)."""
        forca_total = self.obter_forca_total()
        velocidade_total = self.obter_velocidade_total()
        
        return {
            "nome": self.nome,
            "vida": self.vida,
            "vida_maxima": self.vida_maxima,
            "forca": self.forca,
            "forca_total": forca_total,
            "velocidade": self.velocidade,
            "velocidade_total": velocidade_total,
            "nivel": self.nivel,
            "experiencia": self.experiencia,
            "dinheiro": self.dinheiro,
        }

    def __str__(self):
        """Representação em string do jogador."""
        return (
            f"{self.nome} - Vida: {self.vida}/{self.vida_maxima} | "
            f"Força: {self.obter_forca_total()} | Velocidade: {self.obter_velocidade_total()}"
        )

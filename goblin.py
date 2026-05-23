# ============================================================================
# CLASSE GOBLIN - Encapsula toda a lógica do inimigo
# ============================================================================

import random
from config import GOBLINS_STATS, GOBLINS_MUTANTES_STATS, TIPOS_INIMIGOS


class Goblin:
    """Representa um goblin na masmorra."""

    def __init__(self, nivel, mutante=False):
        """
        Inicializa um goblin com nível de dificuldade.
        
        Args:
            nivel (int): Nível de dificuldade (1-10)
            mutante (bool): Se True, é um goblin mutante (mais poderoso)
        """
        stats_table = GOBLINS_MUTANTES_STATS if mutante else GOBLINS_STATS

        # Garante que o nível está no intervalo válido
        if nivel < 1 or nivel > 10:
            nivel = random.randint(1, 10)

        stats = stats_table[nivel]
        self.vida = stats["vida"]
        self.vida_maxima = stats["vida"]
        self.forca = stats["forca"]
        self.velocidade = stats["velocidade"]
        self.mutante = mutante

    def tomar_dano(self, dano):
        """
        Goblin recebe dano. Não pode ficar com vida negativa.
        
        Args:
            dano (int): Quantidade de dano recebido
        """
        self.vida = max(0, self.vida - dano)

    def esta_vivo(self):
        """Verifica se o goblin está vivo."""
        return self.vida > 0

    def obter_status(self):
        """Retorna dicionário com status atual."""
        tipo = "Goblin Mutante" if self.mutante else "Goblin"
        return {
            "tipo": tipo,
            "vida": self.vida,
            "vida_maxima": self.vida_maxima,
            "forca": self.forca,
            "velocidade": self.velocidade,
        }

    def descrever_visualmente(self):
        """Retorna descrição cinematográfica e perturbadora do goblin baseada no nível."""
        if self.mutante:
            # Descrições de goblins mutantes por nível
            descricoes_mutantes = {
                1: "Uma criatura de pele vermelha com veias luminosas pulsando. Seus olhos brilham em amarelo. Três garras em cada mão, úmidas de baba. Um rugido ocasional revela dentes que parecem osso. Sua presença é dolorosa, como se o ar ao redor fizesse ferimentos.",
                2: "Um mutante maior, com musculatura retorcida que não segue anatomia normal. Sua pele tem textura de couro queimado. Possui espículas ósseas saindo da coluna. Seus olhos rastreiam cada movimento seu com inteligência predatória. Rosnados guturais ecoam conforme se aproxima.",
                3: "Uma abominação com múltiplos braços atrofiados saindo de seu corpo. Sua cabeça é desproporcional, mandíbula aberta demais. Sangue goteja de feridas que nunca cicatrizam. Você sente uma aura de maldição irradiando. Seus passos fazem o chão vibrar com malevolvência.",
                4: "Um colosso deformado com pele que muda de cor conforme move. Seu corpo exuda uma substância viscosa fosforescente. Você conta mais de quatro olhos brilhando em diferentes pontos de sua cabeça. Ele emite um zumbido que dói nos dentes. Sua força é visível em cada movimento.",
                5: "Uma criatura primordial que mal parece goblin. Seu corpo é uma mistura de carne, osso e algo que não tem nome. Ácido goteja de sua boca. Você pode sentir a idade - séculos talvez - irradiando dessa coisa. Ele o observa como quem observa um inseto.",
                6: "Um titã de pesadelo com tamanho anormalmente grande. Sua pele é translúcida e você vê órgãos que não deveriam existir se movimentando dentro. Chifres nodosos saem de sua cabeça. Você sente fraqueza apenas por estar perto. Seu rosnado é primitivo e puro.",
                7: "Uma entidade quase demoníaca. Seu corpo está envolvido em um brilho negro que absorve luz. Você consegue ver símbolos antigos escritos em sua pele em letras que o ferem apenas olhando. Ele se move de forma que desafia gravidade. Sua inteligência é inumana e focada em você.",
                8: "Um terror antropomórfico. Múltiplas camadas de pele transparente revelam camadas de músculos e ossos que não combinam. Seus olhos brilham com conhecimento ancestral. Quando ele respira, o ar ao redor congela. Você sente como se estivesse diante de algo que deveria estar morto há eras.",
                9: "Uma criatura que desafia descrição. Seu corpo flutua levemente do chão, sua forma instável e pulsante. Você vê fracturas na realidade ao seu redor. Sangue preto goteja de feridas invisíveis. Seus murmúrios ecoam como se viessem de múltiplas dimensões. Você começa a questionar se realmente pode vencê-lo.",
                10: "Um deus abominável em forma quase-goblin. Sua presença distorce a masmorra ao seu redor. Você sente anos de sua vida sendo sugados apenas por estar próximo. Seus olhos contêm constelações impossíveis. Quando ele se move, o espaço-tempo se comporta erraticamente. Você nunca sentiu tanto medo primordial na vida."
            }
            nivel = min(self.forca // 5 + 1, 10)  # Aproxima nível por força
            return descricoes_mutantes.get(nivel, descricoes_mutantes[10])
        else:
            # Descrições de goblins normais por nível
            descricoes_normais = {
                1: "Um pequeno goblin com pele pálida e enrugada. Seus olhos são pequenos mas malignos. Ele rosna ocasionalmente, revelando dentes afiados mas soltos. Fedorento. Você pode derrotá-lo... provavelmente.",
                2: "Um goblin mais musculoso com cicatrizes pelo corpo. Seus olhos brilham com animal inteligência. Ele empunha um pedaço de osso afiado como arma. Seu rosnado é mais profundo. Você sente que ele já matou antes.",
                3: "Um guerreiro goblin de aparência quase humanóide. Sua pele é verde escuro com marcas de batalha. Você vê inteligência tática em seus olhos. Ele se move com propósito, já avaliando os melhores ângulos para te atacar.",
                4: "Um campeão goblin com armadura caseira feita de ossos. Sua musculatura é impressionante. Ele emite um aura de agressividade contida. Você sente que este é um guerreiro veterano. Seus olhos te prometem dor.",
                5: "Um goblin líder, maior e mais forte que seus pares. Ele carrega uma arma que parece ter sido forjada com propósito maligno. Sua pele é quase negra. Você pode sentir sua inteligência superior. Ele o avalia como um predador avalia presas.",
                6: "Uma criatura que é mais monstro que goblin. Sua pele é dura como couro endurecido em fogo. Músculos corroem por sua forma. Você pode ver que ele já enfrentou muitos heróis antes. Sua presença é opressiva.",
                7: "Uma abominação goblin que transcende a biologia normal. Sua pele brilha com veias vermelhas de sangue corrompido. Você pode sentir a maldade concentrada em seu corpo. Ele emite um zumbido que faz suas feridas doerem. Sua força é quase sobrenatural.",
                8: "Um campeão antigo que deveria estar morto há séculos. Sua pele é quase metálica, marcada com símbolos de poder. Seus olhos brilham com ódio puro. Você sente como se estivesse diante de um guerreiro de eras passadas. Sua habilidade é além do normal.",
                9: "Uma criatura que perdeu quase sua humanidade goblin. Seu corpo é uma máquina de morte aperfeiçoada. Você vê conhecimento ancestral em seus olhos. Cada movimento é calculado para máxima eficiência. Você sente que ele está acima de você.",
                10: "O goblin ultimate - uma perfeição em morte e destruição. Seu corpo é esculpido pela violência de milênios. Você pode sentir séculos de experiência em combate. Seus olhos contêm o vazio de um assassino que nunca falhou. Você está diante de um predador de topo."
            }
            nivel = self.forca // 4 + 1
            return descricoes_normais.get(min(nivel, 10), descricoes_normais[10])

    def __str__(self):
        """Representação em string do goblin."""
        tipo = "Goblin Mutante" if self.mutante else "Goblin"
        return (
            f"{tipo} - Vida: {self.vida}/{self.vida_maxima} | "
            f"Força: {self.forca} | Velocidade: {self.velocidade}"
        )


def criar_goblin_aleatorio():
    """
    Cria um goblin com nível aleatório.
    
    Returns:
        Goblin: Um novo goblin com nível 1-10
    """
    nivel = random.randint(1, 10)
    return Goblin(nivel)


def obter_tipo_inimigo_aleatorio():
    """
    Retorna uma descrição aleatória de inimigos para narrativa.
    
    Returns:
        str: Descrição do tipo de inimigo (ex: "1 goblin", "3 goblins")
    """
    indice = random.randint(1, len(TIPOS_INIMIGOS))
    return TIPOS_INIMIGOS[indice]

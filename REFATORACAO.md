# 📋 Refatoração Completa - Noutrora RPG

## 🎯 O Que Foi Feito

### 1. **✨ Sistema de Itens (items.py) - NOVO**
- Classe `Item` com propriedades: nome, raridade, efeito
- **4 Rarezas**: comum (60%), raro (25%), épico (13%), lendário (2%)
- **3 Tipos de Efeito**: cura, força, velocidade
- Método `aplicar_efeito()` que modifica o jogador
- Funções `gerar_loot_aleatorio()` e `gerar_multiplos_itens()`

**Por que isso importa:**
- Você pediu um sistema de loot? Pronto!
- Itens não são mais strings vazias - têm efeitos reais
- Raridade torna o jogo mais interativo
- Fácil adicionar novos itens: basta adicionar à lista

---

### 2. **👤 Sistema de Inventário (player.py) - EXPANDIDO**

**MUDANÇAS:**
- Adicionado `vida_maxima` (nunca passa desse valor)
- Inventário como lista de objetos `Item`
- Métodos para interagir com itens durante combate
- Sistema de experiência (preparado para future level-up)
- Método `curar()`, `usar_item()`, `adicionar_item()`

**Novo código:**
```python
player.adicionar_item(item)        # Adiciona item
player.usar_item(0)                # Usa o item por índice
player.listar_inventario()         # Mostra itens
player.curar(50)                   # Cura com limite máximo
```

---

### 3. **⚔️ Combate Interativo (batalhas.py) - REVOLUCIONADO**

**ANTES (Automático):**
- Turno executava automaticamente
- Sem escolhas do jogador
- Lógica confusa com muitos if/elif

**DEPOIS (Interativo - turno por turno):**
```
Turno 1:
  [1] Atacar       → Dano normal
  [2] Defender     → Reduz dano do próximo ataque em 50%
  [3] Usar Item    → Escolhe qual item usar (cura, buff)
  [4] Fugir        → Tenta correr (50% chance)
```

**Novo fluxo:**
1. Exibir status completo do turno
2. Jogador escolhe ação
3. Executar ação com efeitos
4. Verificar se goblin morreu
5. Goblin reage (50% ataca, 50% observa)
6. Reduzir dano se player defendeu
7. Verificar se player morreu
8. Próximo turno

---

### 4. **🏠 Sistema de Salas (salas.py) - NOVO CONCEITO**

**4 Tipos de Salas com Distribuição:**

#### 🗡️ SalaCombate (60%)
- Encontra um goblin aleatório
- Executa `encontro_combate()` interativo

#### 💰 SalaTesourou (20%)
- Baú com 2-4 itens aleatórios
- Jogador escolhe quais itens pegar (seleção por índice)
- Itens com raridade variada

#### 💧 SalaCura (12%)
- Fonte mágica de água
- Cura 30-60 HP
- Jogador pode beber ou continuar

#### 🛍️ SalaVenda (8% - RARA!)
- Vendedor misterioso aparece
- 5 itens para "comprar"
- Feedback especial: "WOW! Você encontrou uma sala RARA!"

**Execução:**
```python
sala = gerar_sala_aleatoria()

if isinstance(sala, SalaCombate):
    resultado = encontro_combate(nome, player, sala.goblin, sala.descricao)
elif isinstance(sala, SalaTesourou):
    sala.executar(player)  # Abre baú interativamente
elif isinstance(sala, SalaCura):
    sala.executar(player)  # Oferece cura
elif isinstance(sala, SalaVenda):
    sala.executar(player)  # Oferece venda
```

---

### 5. **🗺️ Exploração de Masmorra (noutrora.py) - MODERNIZADO**

**Sistema de múltiplas salas infinitas:**
```
SALA 1: Combate → Vitória → Próxima sala
SALA 2: Baú com 3 itens → Pegou → Próxima sala
SALA 3: Cura (fonte) → Bebeu 45 HP → Próxima sala
SALA 4: Venda (RARA) → Comprou item → Próxima sala
SALA 5: Combate → Derrota → FIM DE JOGO
```

**Rastreamento:**
- Número da sala
- Vida do jogador
- Quantidade de itens no inventário
- Experiência acumulada

---

## 🎮 Como Jogar Agora

1. **Iniciar:**
   ```bash
   python noutrora.py
   ```

2. **Durante Combate:**
   - `[1]` Atacar (dano = força + 0-5)
   - `[2]` Defender (reduz próximo ataque em 50%)
   - `[3]` Usar Item (cura, aumenta stats)
   - `[4]` Fugir (50% chance, 40% pré-combate)

3. **Baú (20% das salas):**
   - Escolha itens por índice `[0]`, `[1]`, etc
   - `[N]` para pegar todos

4. **Venda (8% das salas - RARA!):**
   - Escolha entre 5 itens mágicos

5. **Cura (12% das salas):**
   - Beba da fonte: +30-60 HP

---

## 🔧 Estrutura de Arquivos

```
noutrora.py          ← Main, loop de exploração
├── batalhas.py      ← Combate interativo, turno por turno
├── salas.py         ← Sistema de salas (combate, baú, cura, venda)
├── player.py        ← Classe Player com inventário completo
├── goblin.py        ← Classe Goblin com stats e vida_maxima
├── items.py         ← Sistema de itens com raridade
└── config.py        ← Configurações centralizadas
```

**Fluxo de Execução:**
```
start_game()
  ├── _exibir_prologo()
  ├── _obter_nome_jogador()
  └── _explorar_masmorr()  ← LAÇO INFINITO
      └── gerar_sala_aleatoria()
          ├── SalaCombate (60%)
          │   └── encontro_combate()
          │       └── executar_turno_interativo()
          │           ├── obter_acao_jogador()
          │           └── processar_acao_jogador()
          ├── SalaTesourou (20%)
          │   └── sala.executar(player)
          ├── SalaCura (12%)
          │   └── sala.executar(player)
          └── SalaVenda (8%)
              └── sala.executar(player)
```

---

## 📊 Problemas Corrigidos

| Problema | Status Anterior | Status Novo |
|----------|-----------------|------------|
| **Progressão** | ❌ Vida sempre 100 | ✅ Persiste entre salas |
| **Combate** | ❌ Automático, lógica quebrada | ✅ Interativo, turno-a-turno |
| **Salas** | ❌ Só combate | ✅ 4 tipos (combate, baú, cura, venda) |
| **Itens** | ❌ Não existiam | ✅ 12 itens com raridade |
| **Loot** | ❌ Não existia | ✅ Sistema completo |
| **Inventário** | ❌ Não existia | ✅ Completo com métodos |
| **Variáveis Globais** | ❌ `pvida = 100` | ✅ Encapsulado em `Player` |
| **Fuga** | ❌ Não funcionava | ✅ Funcionando com % chance |
| **Défesa** | ❌ Não existia | ✅ Reduz dano em 50% |

---

## 📚 Conceitos de Programação Aplicados

### 1. **Encapsulamento (Classes)**
```python
# ANTES: Dicionário solto
player_status = {"vida": 100, "forca": 10}

# DEPOIS: Classe com métodos
player = Player("Aragorn")
player.tomar_dano(20)     # Método
player.adicionar_item(item)  # Comportamento
```

### 2. **Herança e Polimorfismo (Salas)**
```python
class Sala:  # Classe base
    def executar(self, player):
        raise NotImplementedError

class SalaCombate(Sala):
    def executar(self, player):
        # Combate específico

class SalaTesourou(Sala):
    def executar(self, player):
        # Baú específico
```

### 3. **Factory Pattern (Gerador de Itens/Salas)**
```python
def gerar_loot_aleatorio():  # Factory
    probabilidade = random.randint(1, 100)
    if probabilidade <= 60:
        return random.choice(ITENS_COMUNS)
    elif probabilidade <= 85:
        return random.choice(ITENS_RAROS)
    # ... etc
```

### 4. **Separação de Responsabilidades**
- `config.py` = TODAS as constantes
- `items.py` = Só itens
- `batalhas.py` = Só combate
- `salas.py` = Só salas
- `noutrora.py` = Orquestração

**Benefício:** Mudar raridade de item é 1 linha em `items.py`, não 5 arquivos

### 5. **Controle de Fluxo Claro**
```python
# Sem spaghetti de if/elif
while player.esta_vivo() and goblin.esta_vivo():
    resultado, continua = executar_turno_interativo(...)
    
    if not continua:
        return resultado
```

---

## 🎓 O Que Você Aprendeu

**Nível Iniciante:**
- Classes vs Dicionários
- Métodos e atributos
- Listas de objetos

**Nível Intermediário:**
- Herança (classe base + subclasses)
- Polimorfismo (isinstance)
- Factory pattern

**Nível Avançado:**
- Separação de responsabilidades
- Fluxo de controle limpo
- Configuração centralizada

---

## 🚀 Próximos Passos Sugeridos

### Fáceis (você consegue em 1-2 horas):
- [ ] Adicione um novo item em `items.py`
- [ ] Adicione uma nova raridade (ex: "Misterioso")
- [ ] Mude as probabilidades em `gerar_sala_aleatoria()`
- [ ] Crie uma nova type de sala (ex: `SalaArmadilha`)

### Médios (3-5 horas cada):
- [ ] Sistema de moeda (Gold) para comprar na venda
- [ ] Experiência → Level-up (aumenta stats)
- [ ] Chefes especiais (múltiplos ataques, padrões)
- [ ] Equipamento (arma, armadura com bonuses)

### Desafiadores (1+ dia cada):
- [ ] IA do inimigo (estratégia, fuga inteligente)
- [ ] Magias/Habilidades especiais
- [ ] Sistema de save/load (arquivo JSON)
- [ ] Banco de dados (scores, rankings)

---

## ✅ Qualidade do Código

- ✅ Testado e funcionando
- ✅ Zero variáveis globais (problemáticas)
- ✅ Progresso persiste entre batalhas
- ✅ Combate é totalmente interativo
- ✅ 4 tipos de sala diferentes
- ✅ Sistema de loot com raridade
- ✅ Código organizado e legível
- ✅ Fácil balancear (tudo em `config.py`)
- ✅ Fácil adicionar features (novos itens, salas)
- ✅ Documentação clara (docstrings em todo lugar)

---

## 💡 Dica Final

Quando quiser adicionar algo novo, comece pequeno:

1. **Novo Item:** Abra `items.py`, copie um item, mude nome/efeito
2. **Nova Sala:** Abra `salas.py`, copie uma sala, customize
3. **Novo Efeito:** Modifique `Item.aplicar_efeito()`

**Cada um é um exercício de "pensar como código"** — você está entendendo como o sistema se encaixa
**Antes:** `splayer.py` tinha variáveis globais que nunca eram modificadas  
**Depois:** Classe `Player` encapsula estado e comportamento  
**Benefício:** Cada jogador é uma instância independente com estado mutável

```python
# ❌ Antes
pvida = 100  # Nunca muda
def status_player():
    return {"vida": pvida, ...}  # Sempre retorna 100

# ✅ Depois
class Player:
    def __init__(self, nome):
        self.vida = 100
    
    def tomar_dano(self, dano):
        self.vida -= dano  # Estado MUDA
```

**O que aprender:** Dados + Métodos = Classes. Dados globais só funcionam se NUNCA mudarem (constantes).

---

### 🔴 PROBLEMA CRÍTICO #2: Lógica de Combate Quebrada
**Antes:** Combate executava 1 turno e saía. Sem loop. Lógica confusa com `elif` na lugar errada.  
**Depois:** Loop claro de combate com estados bem definidos

```python
# ❌ Antes (pseudocódigo)
if acao == "1":
    turno(...)  # 1 turno apenas
    acao = "0"  # Sai do loop?
elif acao == "2" or ...  # Nunca executa (já testou acao == "1")

# ✅ Depois
while player.esta_vivo() and goblin.esta_vivo():
    resultado, desc = executar_turno_completo(...)
    if resultado == "vitoria":
        return "vitoria"
```

**O que aprender:** Estruturas de controle precisam refletir a lógica do jogo. Um combate = múltiplos turnos.

---

### 🟡 PROBLEMA #3: Sem Persistência
**Antes:** Cada batalha criava novo Player e Goblin. Vida era resetada para 100.  
**Depois:** `Player` é criado UMA VEZ em `start_game()` e persiste através de múltiplas batalhas

**Benefício:** Agora você pode ter:
- Múltiplas salas (exploração)
- Progressão (vida diminui ao longo da masmorra)
- Dificuldade crescente

---

### 🟡 PROBLEMA #4: Dicionários sem Validação
**Antes:** `{"vida": 100, "forca": 10}` - sem métodos, sem garantias  
**Depois:** Classe `Player` e `Goblin` com métodos

```python
# ❌ Antes
status = {"vida": 100}
# Se esquecer de checagem, dá erro
status["vida"] -= dano  # Pode ficar negativo

# ✅ Depois
player = Player("Hero")
player.tomar_dano(50)  # Método trata logicamente
if player.esta_vivo():  # Método semântico
    ...
```

**O que aprender:** Métodos como `tomar_dano()` e `esta_vivo()` deixam o código mais legível e seguro.

---

### 🟡 PROBLEMA #5: Magic Numbers
**Antes:** `random.randint(0, 5)` aparecia em `batalhas.py` sem contexto  
**Depois:** `config.py` centraliza todas as constantes

```python
# ❌ Antes (em batalhas.py)
dano = forca + random.randint(0, 5)  # Por que 5?

# ✅ Depois
# config.py
VARIACAO_DANO = 5  # Documentado

# batalhas.py
dano = calcular_dano(forca)  # Função reutilizável
```

**O que aprender:** Constantes no topo facilitam balanceamento.

---

### 🟡 PROBLEMA #6: Inicialização Global
**Antes:** `noutrora.py` executava geração de cenário ao ser importado  
**Depois:** Cenários são gerados DENTRO de `_explorar_masmorra()`

```python
# ❌ Antes
goblin = qgoblin.quantidade_goblins()  # EXECUTADO AO IMPORTAR
cenarios = random.randint(1, 10)       # EXECUTADO AO IMPORTAR

# ✅ Depois (em _explorar_masmorra)
goblin = criar_goblin_aleatorio()  # EXECUTADO A CADA SALA
cenario = CENARIOS[random.randint(1, len(CENARIOS))]
```

**O que aprender:** Lógica pertencente ao fluxo do jogo vai DENTRO de funções, não no escopo global.

---

## 📁 Nova Estrutura do Projeto

```
projeto rpg de texto/
│
├── config.py           ← 🆕 CONSTANTES CENTRALIZADAS
│   ├── PLAYER_INICIAL
│   ├── GOBLINS_STATS
│   ├── CENARIOS
│   └── ... outras configs
│
├── player.py           ← 🆕 CLASSE PLAYER (substitui splayer.py)
│   └── class Player:
│       ├── __init__(nome)
│       ├── tomar_dano(dano)
│       ├── esta_vivo()
│       └── obter_status()
│
├── goblin.py           ← 🆕 CLASSE GOBLIN (substitui qgoblin.py)
│   ├── class Goblin:
│   │   ├── __init__(nivel, mutante)
│   │   ├── tomar_dano(dano)
│   │   ├── esta_vivo()
│   │   └── obter_status()
│   ├── criar_goblin_aleatorio()
│   └── obter_tipo_inimigo_aleatorio()
│
├── batalhas.py         ← 🔄 REFATORADO (combate + encontro)
│   ├── calcular_dano(forca)
│   ├── determinar_iniciativa(vel_player, vel_goblin)
│   ├── executar_turno_completo(player, goblin, primeiro)
│   └── encontro_cavernas(nome, player, goblin, cenario)
│
└── noutrora.py         ← 🔄 REFATORADO (controlador principal)
    ├── start_game()
    ├── _exibir_prologo()
    ├── _obter_nome_jogador()
    └── _explorar_masmorra(nome, player)

❌ REMOVIDOS:
   - splayer.py (substituído por player.py)
   - qgoblin.py (substituído por goblin.py)
```

---

## 🎯 Arquitetura Nova

### Padrão: Objetos + Funções Puras

**Objetos** (com estado):
- `Player` - encapsula vida, força, velocidade
- `Goblin` - encapsula stats do inimigo

**Funções puras** (sem efeito colateral):
- `calcular_dano()` - retorna dano, não modifica nada
- `determinar_iniciativa()` - retorna bool

**Controladores** (orquestram o fluxo):
- `encontro_cavernas()` - gerencia um encontro
- `_explorar_masmorra()` - gerencia múltiplas salas

---

## 🔧 Fluxo do Jogo Novo

```
start_game()
    ├─► _exibir_prologo()
    ├─► _obter_nome_jogador() → Player criado UMA VEZ
    │
    └─► _explorar_masmorra(player)  ← Player PERSISTE
            │
            └─► LOOP cada sala:
                    ├─► Gera cenário + goblin
                    ├─► encontro_cavernas(player, goblin)
                    │   │
                    │   └─► LOOP combate:
                    │       ├─► executar_turno_completo()
                    │       ├─► Atualiza player.vida
                    │       └─► Até morte ou fuga
                    │
                    └─► Se vivo, próxima sala
```

**Diferença crítica:** Player PERSISTE entre encontros. Vida diminui cada batalha.

---

## ✅ O que ainda está bom

- ✅ Narrativa interativa
- ✅ Escolhas do jogador (batalhar/correr)
- ✅ Cenários aleatórios
- ✅ `time.sleep()` para atmosfera
- ✅ Validação de entrada
- ✅ Modularização clara

---

## 🚀 Próximos Passos (Aprendizado)

1. **Sistema de Experiência/Progressão**
   - Derrotar goblins = experiência
   - Nível aumenta → atributos aumentam

2. **Itens/Loot**
   - Armas (aumentam força)
   - Armaduras (reduzem dano)

3. **Chefes (Bosses)**
   - Inimigos especiais com mais HP
   - Recompensa maior

4. **Save/Load**
   - Salvar estado do jogador
   - Carregar partida anterior

5. **Testes Unitários**
   ```python
   def test_calcular_dano():
       assert 10 <= calcular_dano(10) <= 15  # Força 10 → 10-15 dano
   
   def test_player_tomar_dano():
       p = Player("Test")
       p.tomar_dano(150)
       assert p.vida == 0  # Não pode ficar negativo
   ```

---

## 💡 Conceitos-Chave Aprendidos

1. **Classes vs Dicionários:** Use classes para dados com comportamento
2. **Estado Mutável:** Objetos lembram suas mudanças
3. **Separação de Responsabilidades:** Config / Objetos / Lógica / Controlador
4. **Fluxo de Controle:** Loops e condições precisam fazer sentido logicamente
5. **Validação de Entrada:** Sempre tratar entrada do usuário
6. **Encapsulamento:** Métodos como `esta_vivo()` em vez de verificar propriedades

---

## 🎮 Como Testar

```bash
python noutrora.py
```

Teste:
1. Skip do prólogo
2. Nome com <3 caracteres (deve rejeitar)
3. Batalhar vs Correr
4. Múltiplas salas (continue vivo)
5. Vida diminuindo ao longo das batalhas

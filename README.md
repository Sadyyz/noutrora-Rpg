# 🎮 Noutrora RPG - Jogo de Texto Interativo

## ⚡ Quick Start

```bash
python noutrora.py
```

## 📖 Como Jogar

### 1️⃣ **Prólogo**
- Leia ou pule a história de introdução
- Digite `sim` ou `nao`

### 2️⃣ **Nome do Personagem**
- Digite um nome com mais de 3 letras
- Ex: `Aragorn`, `Gandalf`, `Legolas`

### 3️⃣ **Exploração da Masmorra**
Você encontrará **4 tipos de salas aleatórias:**

#### 🗡️ **Sala de Combate (60%)**
Encontra um goblin! Você pode:
- `[1]` **Atacar** → Causa dano (força + 0-5)
- `[2]` **Defender** → Reduz o próximo ataque em 50%
- `[3]` **Usar Item** → Cura ou aumenta stats
- `[4]` **Fugir** → 50% de chance de escapar

**Combate é turno-a-turno:**
1. Você escolhe ação
2. Executada com efeito
3. Goblin contra-ataca (ou observa)
4. Próximo turno

#### 💰 **Sala com Baú (20%)**
Encontra um baú com itens! Você pode:
- `[0]`, `[1]`, `[2]` → Pegar item específico
- `[3]` → Pegar TODOS os itens
- `[4]` → Deixar para trás

**Itens têm raridade:**
- ⚪ Comum (restaura pouca vida)
- 🔵 Raro (restaura bastante vida ou +1 força)
- 🟣 Épico (restaura muita vida ou +2 força)
- 🟡 Lendário (restaura completo ou +3 força)

#### 💧 **Sala de Cura (12%)**
Uma fonte mágica aparece! Você pode:
- `[1]` → Beber (cura 30-60 HP)
- `[2]` → Continuar sem beber

#### 🛍️ **Sala de Venda (8% - MUITO RARA!)**
Um vendedor misterioso oferece itens! Você pode:
- `[0]` até `[4]` → Escolher item para "comprar"
- `[5]` → Sair sem comprar

---

## 📊 Sistema de Progressão

```
Sala 1: Combate
  → Vitória
  → Próxima sala
  
Sala 2: Baú com itens
  → Pegou 2 itens
  → Vida: 90/100
  → Próxima sala
  
Sala 3: Cura
  → Bebeu da fonte
  → Vida: 100/100
  → Próxima sala
  
Sala 4: Combate DIFÍCIL
  → Derrota
  → FIM DE JOGO
  → Você explorou 4 salas
  → Acumulou 100 XP
```

**Você morre = FIM**. Jogo continua infinito até morrer.

---

## 🎯 Estratégia

1. **Coletar itens** → Use em combates difíceis
2. **Usar defesa** → Quando goblin for muito forte
3. **Fugir inteligentemente** → Antes de combate se HP baixo
4. **Beber em fontes** → Recuperar vida para próximo combate

---

## 📈 Seu Status

A cada sala você vê:
```
Vida: 80/100 | Inventário: 2 itens
```

- **Vida** = HP atual / HP máximo (100)
- **Inventário** = Quantos itens você tem

---

## 🎓 O Que Aprender

Este jogo foi refatorado de forma **didática**. Explore:

1. **Arquivo `items.py`** 
   - Veja como itens são criados com raridade
   - Entenda probabilidades

2. **Arquivo `salas.py`**
   - Veja como 4 tipos diferentes de salas funcionam
   - Polimorfismo em ação (herança de classes)

3. **Arquivo `batalhas.py`**
   - Combate turno-a-turno interativo
   - Como usar `while` para turnos

4. **Arquivo `config.py`**
   - TODAS as constantes do jogo (stats, valores)
   - Mudando aqui = balanceia o jogo todo

---

## 🐛 Bugs ou Sugestões?

Se encontrar algo estranho:
1. Verifique `config.py` (talvez valores desequilibrados)
2. Leia a documentação em `REFATORACAO.md`
3. O código está comentado para você entender

---

## 🎨 Personalizando o Jogo

### Mudar raridade de itens?
Abra `items.py`, procure `gerar_loot_aleatorio()`:
```python
if probabilidade <= 70:  # 70% comum (era 60%)
    return random.choice(ITENS_COMUNS)
```

### Mais salas de combate?
Abra `salas.py`, procure `gerar_sala_aleatoria()`:
```python
if probabilidade <= 70:  # 70% combate (era 60%)
    from goblin import criar_goblin_aleatorio
```

### Mudar vida inicial?
Abra `config.py`:
```python
PLAYER_INICIAL = {
    "vida": 150,  # Era 100
    "forca": 10,
    "velocidade": 5,
}
```

---

## 📝 Arquivos do Projeto

```
noutrora.py         ← RODAR ISTO
batalhas.py         ← Combate turno-a-turno
salas.py            ← Salas da masmorra
player.py           ← Jogador com inventário
goblin.py           ← Inimigos
items.py            ← Sistema de itens
config.py           ← Valores centralizados
REFATORACAO.md      ← Documentação técnica
README.md           ← Este arquivo
```

---

## 🚀 Divirta-se!

O jogo é roguelike: cada partida é diferente!

- Salas aleatórias
- Inimigos com força aleatória
- Itens com raridade aleatória
- Desafio aumenta conforme você vai mais fundo

**Quantas salas você consegue explorar?**

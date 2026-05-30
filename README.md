# NOUTRORA RPG

```
python noutrora.py
```

---

## O que é

RPG narrativo de terminal. Você avança por salas geradas de forma procedural,
toma decisões, enfrenta inimigos, e carrega as consequências de cada escolha
através de múltiplas runs.

O jogo **lembra de você**. NPCs reagem ao seu histórico. O mundo muda.

---

## Como jogar

**1. Prólogo** — leia ou pule.

**2. Nome** — mínimo 4 letras.

**3. Classe:**
- `Metamorfo` — absorve essência dos inimigos derrotados, ficando mais forte
- `Druida` — usa veneno para enfraquecer inimigos gradualmente

**4. Explorar** — salas aleatórias em ordem diferente a cada run.

**Durante combate:**
```
[1] Atacar    — dano = força + variação
[2] Defender  — reduz próximo golpe em 50%
[3] Usar Item — item do inventário
[4] Fugir     — 50% de chance
```

**Tipos de sala:**
```
60%  Combate   — inimigo aleatório
20%  Tesouro   — baú com itens
12%  Cura      — fonte que restaura HP
 8%  Venda     — vendedor misterioso (RARA)
```

**A cada ~5 salas**, um evento especial pode ocorrer:
- Encontro com o Mercador Sombrio
- Elfo Ferido (salvar ou não)
- Rei Goblin (negociar, trair, lutar)
- Entidade do Abismo (pacto de poder)
- Armadilhas, altares, inscrições, ecos do passado

---

## Sistema de Memória

O jogo salva um histórico **permanente** entre todas as runs em `data/memoria.json`.

```
Ajudou o Mercador  → ele te presenteia na próxima run
Salvou o Elfo      → elfo cura você e dá gold depois
Traiu o Rei Goblin → ele ataca na vista na próxima run
Fez pacto          → entidade aparece mais vezes
```

Acessível via menu: `[3] Memória do mundo`

---

## Estrutura

```
noutrora.py                  ← MAIN (nunca renomear)
config.py                    ← Todas as constantes
player.py                    ← Classe Player
goblin.py                    ← Classe Goblin
batalhas.py                  ← Sistema de combate
salas.py                     ← Salas da masmorra
items.py                     ← Itens consumíveis
equipment.py                 ← Equipamentos
assets/
  classes/
    metamorfo.py             ← Classe Metamorfo
    druida.py                ← Classe Druida
  save/
    save_config.py           ← Save/load de run
systems/
  memoria.py                 ← Memória persistente entre runs
  npcs.py                    ← NPCs com memória
  run_procedural.py          ← Geração procedural de eventos
data/
  save.json                  ← Save da run atual (criado em jogo)
  memoria.json               ← Histórico permanente (criado em jogo)
```

---

## Dependências

```
python 3.8+
colorama  (opcional — o jogo funciona sem ela)
```

Instalar colorama:
```
pip install colorama
```

---

## Filosofia

> O objetivo não é explorar um mapa.
> O objetivo é viver narrativas, criar consequências,
> e descobrir que o mundo se lembra de quem você foi.

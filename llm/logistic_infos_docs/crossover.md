# Módulo de Cruzamento (Crossover) - Algoritmo Genético para Otimização Logística

## Visão Geral

O módulo `d_crossover.py` implementa operadores de cruzamento (crossover) para o algoritmo genético, responsáveis por combinar características de duas soluções parentais para gerar uma nova solução (offspring). Este módulo oferece duas estratégias distintas de cruzamento: **RBX (Route-Based Crossover)** e **BCRC (Best Cost Route Crossover)**, permitindo exploração diversificada do espaço de soluções.

## Objetivo

Criar novas soluções candidatas combinando informações genéticas de duas soluções parentais de alta qualidade, preservando características promissoras e potencialmente gerando soluções superiores. O crossover é o principal mecanismo de exploração no algoritmo genético.

## Fundamento em Algoritmos Genéticos

### Papel do Crossover

O crossover simula a **reprodução sexual** na evolução biológica:

```
Pai 1: [A, B, C, D, E]  ──┐
                          ├──> Crossover ──> Filho: [A, B, X, Y, E]
Pai 2: [X, Y, Z, W, V]  ──┘
```

**Princípios:**
- **Herança:** Filho herda características de ambos os pais
- **Recombinação:** Combina blocos genéticos (rotas) de diferentes soluções
- **Diversidade:** Gera variabilidade na população
- **Exploração:** Descobre novas regiões do espaço de busca

### Pressão Seletiva

```
População → Seleção → Crossover → Mutação → Nova Geração
    ↑                    ↓                        ↓
    └────────────── Avaliação Fitness ←──────────┘
```

Pais de alta qualidade (baixo fitness) produzem filhos com maior probabilidade de qualidade.

## Estratégias Implementadas

### 1. RBX (Route-Based Crossover) - Cruzamento Baseado em Rota

#### Conceito

Herda uma **rota completa** de um veículo específico do Pai 1 e preenche o restante com genes do Pai 2, preservando a estrutura e ordem de uma rota de alta qualidade.

#### Algoritmo Passo a Passo

**Entrada:**
- `parent1`: Cromossomo do primeiro pai (lista de genes/entregas)
- `parent2`: Cromossomo do segundo pai
- `deliveries`: Informações das entregas
- `vehicles`: Informações dos veículos
- `center`: Coordenadas do centro de distribuição

**Processo:**

```
1. Decodificar parent1 em estrutura de rotas por veículo
   parent1_decoded = {
       "V1": [1, 5, 8, 12, 20],
       "V2": [2, 7, 15, 18, 23],
       "V3": [3, 6, 9, 14, 22],
       ...
   }

2. Selecionar aleatoriamente um veículo
   selected_vehicle = "V2"  (aleatório)

3. Herdar rota completa deste veículo
   inherited_route = [2, 7, 15, 18, 23]

4. Criar filho iniciando com a rota herdada
   child = [2, 7, 15, 18, 23]

5. Adicionar genes do parent2 que ainda não estão no filho
   for gene in parent2:
       if gene not in child:
           child.append(gene)
   
   child = [2, 7, 15, 18, 23, 1, 3, 4, 6, 8, 9, 10, ...]
```

**Saída:**
- `child`: Novo cromossomo (lista completa de entregas)

#### Exemplo Detalhado

**Configuração:**
```python
# Pai 1 (decodificado)
routes_p1 = {
    "V1": [1, 5, 8, 12, 20],
    "V2": [2, 7, 15, 18, 23],  # <- Selecionado
    "V3": [3, 6, 9, 14, 22],
    "V4": [4, 10, 13, 17, 21],
    "V5": [11, 16, 19, 24, 25]
}

# Pai 2 (codificado)
parent2 = [11, 3, 7, 19, 5, 14, 1, 22, 10, 16, 4, 8, 
           24, 12, 6, 21, 9, 25, 13, 20, 17, 2, 15, 18, 23]
```

**Execução:**
```python
# 1. Veículo selecionado: V2
selected_vehicle = "V2"

# 2. Rota herdada do V2
inherited_route = [2, 7, 15, 18, 23]

# 3. Inicializar filho
child = [2, 7, 15, 18, 23]

# 4. Adicionar genes do parent2 não presentes
# parent2 = [11, 3, 7, 19, 5, 14, 1, 22, 10, 16, ...]
#              ↓   ↓  X    ↓   ↓   ↓   ↓   ↓   ↓   ↓
#            novo novo já  novo novo novo novo novo novo
#                     está

# 5. Filho final
child = [2, 7, 15, 18, 23, 11, 3, 19, 5, 14, 1, 22, 
         10, 16, 4, 8, 24, 12, 6, 21, 9, 25, 13, 20, 17]
```

**Análise:**
- **Preservado:** Sequência exata do V2: [2, 7, 15, 18, 23]
- **Herdado de P2:** Ordem dos demais genes conforme aparecem no Pai 2
- **Característica:** Mantém boa subsequência de rota do Pai 1

#### Vantagens e Desvantagens

**Vantagens:**
- ✅ Preserva rotas completas de alta qualidade
- ✅ Mantém ordem relativa entre entregas de uma rota
- ✅ Simples e computacionalmente eficiente O(n)
- ✅ Garante diversidade através de seleção aleatória de veículo

**Desvantagens:**
- ❌ Não considera otimização de custo durante construção
- ❌ Ordem do restante pode não ser ideal
- ❌ Pode gerar rotas ineficientes se pais forem muito diferentes

**Complexidade:**
- **Tempo:** O(n) onde n é número total de entregas
- **Espaço:** O(n) para estruturas auxiliares

### 2. BCRC (Best Cost Route Crossover) - Cruzamento com Melhor Custo

#### Conceito

Extrai uma **sub-rota** (segmento) do Pai 1 e insere no Pai 2 na **posição que minimiza o custo total** da rota resultante, utilizando busca exaustiva para encontrar a inserção ótima.

#### Algoritmo Passo a Passo

**Entrada:**
- `parent1`: Cromossomo do primeiro pai
- `parent2`: Cromossomo do segundo pai
- `deliveries`: Informações das entregas (com coordenadas)

**Processo:**

```
1. Selecionar aleatoriamente dois índices i, j (i < j) no parent1
   i, j = sorted(random.sample(range(len(parent1)), 2))
   
   Exemplo: i=5, j=10

2. Extrair sub-rota do parent1
   subroute = parent1[i:j]
   
   parent1 = [1, 2, 3, 4, 5, |6, 7, 8, 9, 10|, 11, 12, ...]
                              └─ subroute ──┘

3. Criar base removendo genes da subroute do parent2
   base = [g for g in parent2 if g not in subroute]
   
   parent2 = [15, 6, 3, 9, 1, 12, 8, 4, 7, ...]
              |   X     X     |   X     X
              └─── mantém ────┘
   
   base = [15, 3, 1, 12, 4, ...]

4. Testar todas as posições de inserção possíveis
   for pos in range(len(base) + 1):
       candidate = base[:pos] + subroute + base[pos:]
       cost = calcular_custo_manhattan(candidate)
       
       if cost < best_cost:
           best_cost = cost
           best_pos = pos

5. Retornar melhor configuração
   child = base[:best_pos] + subroute + base[best_pos:]
```

**Saída:**
- `child`: Novo cromossomo com subroute inserida otimamente

#### Exemplo Detalhado

**Configuração:**
```python
# Pai 1
parent1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

# Pai 2
parent2 = [15, 6, 3, 9, 1, 12, 8, 4, 7, 2, 5, 11, 10, 13, 14]

# Coordenadas (exemplo simplificado)
deliveries = {
    1: {"lat": 0, "lon": 0},
    2: {"lat": 1, "lon": 1},
    3: {"lat": 2, "lon": 0},
    ...
}
```

**Execução:**

```python
# 1. Índices aleatórios
i, j = 5, 10
# i=5, j=10

# 2. Extrair subroute
subroute = parent1[5:10] = [6, 7, 8, 9, 10]

# 3. Criar base (parent2 sem genes da subroute)
parent2 = [15, 6, 3, 9, 1, 12, 8, 4, 7, 2, 5, 11, 10, 13, 14]
           |   X     X     |   X     X     |   |   X      |
base = [15, 3, 1, 12, 4, 2, 5, 11, 13, 14]

# 4. Testar posições (len(base) + 1 = 11 posições)

## Posição 0: [6,7,8,9,10] + [15,3,1,12,4,2,5,11,13,14]
candidate = [6, 7, 8, 9, 10, 15, 3, 1, 12, 4, 2, 5, 11, 13, 14]
cost_pos0 = manhattan(6,7) + manhattan(7,8) + ... + manhattan(13,14)
         = 2 + 2 + 2 + 2 + 10 + 25 + ... = 150 (exemplo)

## Posição 1: [15] + [6,7,8,9,10] + [3,1,12,4,2,5,11,13,14]
candidate = [15, 6, 7, 8, 9, 10, 3, 1, 12, 4, 2, 5, 11, 13, 14]
cost_pos1 = manhattan(15,6) + manhattan(6,7) + ... + manhattan(13,14)
         = 18 + 2 + 2 + ... = 145 (exemplo)

## Posição 2: [15,3] + [6,7,8,9,10] + [1,12,4,2,5,11,13,14]
candidate = [15, 3, 6, 7, 8, 9, 10, 1, 12, 4, 2, 5, 11, 13, 14]
cost_pos2 = manhattan(15,3) + manhattan(3,6) + ... + manhattan(13,14)
         = 25 + 8 + 2 + ... = 135 (exemplo) ← MELHOR

## ... continua testando até posição 10

# 5. Melhor posição encontrada: pos = 2
best_pos = 2
best_cost = 135

# 6. Construir filho
child = base[:2] + subroute + base[2:]
child = [15, 3, 6, 7, 8, 9, 10, 1, 12, 4, 2, 5, 11, 13, 14]
```

#### Cálculo de Custo Manhattan

Para cada candidato, o custo é calculado como:

$$C_{total} = \sum_{i=1}^{n-1} d_{Manhattan}(P_i, P_{i+1})$$

Onde:
- $P_i$: Entrega na posição $i$ do candidato
- $d_{Manhattan}(A, B) = |lat_A - lat_B| + |lon_A - lon_B|$

**Código:**
```python
cost = 0
for k in range(len(candidate) - 1):
    a = candidate[k]
    b = candidate[k + 1]
    cost += manhattan(
        (deliveries[a]["lat"], deliveries[a]["lon"]),
        (deliveries[b]["lat"], deliveries[b]["lon"])
    )
```

#### Vantagens e Desvantagens

**Vantagens:**
- ✅ Otimização local: encontra melhor inserção
- ✅ Considera distância Manhattan real entre entregas
- ✅ Preserva blocos promissores (subroute)
- ✅ Gera soluções de maior qualidade em média

**Desvantagens:**
- ❌ Computacionalmente mais custoso: O(n²) vs O(n) do RBX
- ❌ Testa todas as posições (força bruta)
- ❌ Não considera estrutura global de veículos
- ❌ Pode ser lento para muitas entregas

**Complexidade:**
- **Tempo:** O(n²) onde n é número de entregas
  - O(n) posições testadas
  - O(n) cálculo de custo para cada posição
- **Espaço:** O(n) para estruturas candidatas

### Comparação Entre RBX e BCRC

| Aspecto | RBX | BCRC |
|---------|-----|------|
| **Estratégia** | Herdar rota completa | Inserir sub-rota otimamente |
| **Complexidade** | O(n) | O(n²) |
| **Qualidade** | Moderada | Alta |
| **Velocidade** | Rápida | Lenta |
| **Exploração** | Alta (aleatória) | Moderada (gulosa local) |
| **Preservação** | Rota de veículo intacta | Bloco contíguo |
| **Uso ideal** | Populações grandes | Refinamento de soluções |

## Função de Seleção: `crossover()`

### Interface Principal

```python
def crossover(parent1, parent2, deliveries, vehicles, center, p_rbx=0.5):
```

**Parâmetros:**
- `parent1`: Primeiro cromossomo parental
- `parent2`: Segundo cromossomo parental
- `deliveries`: Dicionário com informações de entregas
- `vehicles`: Dicionário com informações de veículos
- `center`: Coordenadas do centro de distribuição
- `p_rbx`: Probabilidade de usar RBX (padrão: 0.5)

**Retorno:**
- Cromossomo filho gerado por RBX ou BCRC

### Lógica de Decisão

```python
if random.random() < p_rbx:
    return RBX(parent1, parent2, deliveries, vehicles, center)
else:
    return BCRC(parent1, parent2, deliveries)
```

**Estratégia Probabilística:**

$$P(RBX) = p_{rbx} = 0.5$$
$$P(BCRC) = 1 - p_{rbx} = 0.5$$

**Distribuição 50/50 (padrão):**
- 50% das vezes: RBX (rápido, exploratório)
- 50% das vezes: BCRC (lento, otimizador)

### Ajustes de Probabilidade

**Cenários de Uso:**

```python
# Fase inicial: priorizar exploração
crossover(..., p_rbx=0.7)  # 70% RBX, 30% BCRC

# Fase intermediária: balanceado
crossover(..., p_rbx=0.5)  # 50% RBX, 50% BCRC (padrão)

# Fase final: priorizar refinamento
crossover(..., p_rbx=0.3)  # 30% RBX, 70% BCRC

# Apenas exploração
crossover(..., p_rbx=1.0)  # 100% RBX

# Apenas otimização
crossover(..., p_rbx=0.0)  # 100% BCRC
```

**Impacto no Algoritmo:**

| p_rbx | Comportamento | Velocidade | Qualidade |
|-------|---------------|------------|-----------|
| 1.0 | Exploração máxima | Muito rápida | Moderada |
| 0.7 | Alta exploração | Rápida | Boa |
| 0.5 | Balanceado | Média | Muito boa |
| 0.3 | Alta otimização | Lenta | Alta |
| 0.0 | Otimização máxima | Muito lenta | Máxima |

## Dependências e Integração

### Módulos Importados

```python
from b_manhattan_distance import cartesian_to_manhattan as manhattan
from _encode_decode import decode_chromosome
import random
```

**Funções Utilizadas:**

1. **`cartesian_to_manhattan(coord1, coord2)`**
   - Calcula distância Manhattan entre dois pontos
   - Usado no BCRC para avaliar custo de rotas
   - Ver: [manhattan_distance.md](manhattan_distance.md)

2. **`decode_chromosome(chromosome, deliveries, vehicles)`**
   - Converte cromossomo linear em estrutura de rotas por veículo
   - Usado no RBX para acessar rotas individuais
   - Ver: `_encode_decode.py`

3. **`random.choice()` e `random.sample()`**
   - Seleção aleatória de veículos (RBX)
   - Seleção de índices para subroute (BCRC)

### Fluxo no Algoritmo Genético

```
┌─────────────────────────┐
│  População Geração N    │
└───────────┬─────────────┘
            │
            ↓
┌─────────────────────────┐
│  f_selection.py         │  ← Seleciona pais
│  (Torneio, Roleta, etc.)│
└───────────┬─────────────┘
            │
            ↓
┌─────────────────────────┐
│  d_crossover.py         │  ← Gera filhos (aqui)
│  RBX ou BCRC            │
└───────────┬─────────────┘
            │
            ↓
┌─────────────────────────┐
│  e_mutation.py          │  ← Aplica mutação
└───────────┬─────────────┘
            │
            ↓
┌─────────────────────────┐
│  c_fitness.py           │  ← Avalia filhos
└───────────┬─────────────┘
            │
            ↓
┌─────────────────────────┐
│  População Geração N+1  │
└─────────────────────────┘
```

### Estruturas de Dados

**Cromossomo (representação linear):**
```python
chromosome = [3, 15, 7, 22, 11, 18, 4, 25, 9, 13, 1, 19, 6, 14, 21, ...]
# Lista de IDs de entregas em ordem
```

**Cromossomo decodificado (estrutura por veículos):**
```python
decoded = {
    "V1": [3, 15, 7, 22, 11],
    "V2": [18, 4, 25, 9, 13],
    "V3": [1, 19, 6, 14, 21],
    ...
}
# Dicionário: veículo → lista de entregas
```

## Exemplo Completo de Uso

### Cenário Prático

```python
from d_crossover import crossover
from delivery_setup.deliveries import load_deliveries_info
from delivery_setup.vehicles import load_vehicles_info
from address_routes.distribute_center import get_center_coordinates

# Carregar dados
city = "SP"
deliveries = load_deliveries_info(city)
vehicles = load_vehicles_info(city)
center = get_center_coordinates(city)

# Pais selecionados (cromossomos lineares)
parent1 = [1, 5, 8, 12, 20, 2, 7, 15, 18, 23, 3, 6, 9, 14, 22, 
           4, 10, 13, 17, 21, 11, 16, 19, 24, 25]

parent2 = [11, 3, 7, 19, 5, 14, 1, 22, 10, 16, 4, 8, 24, 12, 6, 
           21, 9, 25, 13, 20, 17, 2, 15, 18, 23]

# Executar crossover com probabilidade padrão (50% RBX, 50% BCRC)
child = crossover(parent1, parent2, deliveries, vehicles, center)

print(f"Pai 1: {parent1}")
print(f"Pai 2: {parent2}")
print(f"Filho: {child}")

# Executar múltiplos crossovers
children = []
for i in range(10):
    child = crossover(parent1, parent2, deliveries, vehicles, center, p_rbx=0.6)
    children.append(child)
    print(f"Filho {i+1}: {child}")
```

### Saída Esperada

```
Pai 1: [1, 5, 8, 12, 20, 2, 7, 15, 18, 23, ...]
Pai 2: [11, 3, 7, 19, 5, 14, 1, 22, 10, 16, ...]

# Exemplo com RBX (rota V2 herdada)
Filho: [2, 7, 15, 18, 23, 11, 3, 19, 5, 14, 1, 22, ...]
        └──── V2 ─────┘ └──── do Pai 2 ──────────────┘

# Exemplo com BCRC (subroute [8, 12, 20] inserida)
Filho: [11, 3, 8, 12, 20, 7, 19, 5, 14, 1, 22, ...]
        └───┘ └─ sub ─┘ └──── do Pai 2 ─────────┘
```

## Boas Práticas e Recomendações

### 1. Balanceamento de Estratégias

**Evolução Adaptativa:**
```python
# Ajustar p_rbx conforme progresso
def adaptive_p_rbx(generation, max_generations):
    # Começa com exploração, termina com otimização
    return 0.8 - (0.6 * generation / max_generations)

# Geração 0: p_rbx = 0.8 (80% RBX)
# Geração 100: p_rbx = 0.2 (20% RBX)
```

### 2. Validação de Filhos

Sempre verificar integridade do filho:
```python
def validate_child(child, expected_size):
    # Todos os genes presentes?
    assert len(child) == expected_size
    
    # Sem duplicatas?
    assert len(set(child)) == expected_size
    
    # Todos os genes válidos?
    assert all(1 <= gene <= expected_size for gene in child)
```

### 3. Taxa de Crossover

Em algoritmos genéticos, nem todos os indivíduos sofrem crossover:

```python
def apply_crossover_selectively(population, crossover_rate=0.8):
    new_population = []
    
    for i in range(0, len(population), 2):
        parent1 = population[i]
        parent2 = population[i+1]
        
        if random.random() < crossover_rate:
            # 80% de chance: fazer crossover
            child = crossover(parent1, parent2, ...)
            new_population.append(child)
        else:
            # 20% de chance: copiar pai diretamente
            new_population.append(parent1.copy())
    
    return new_population
```

### 4. Elitismo

Preservar melhores soluções:
```python
def genetic_step_with_elitism(population, elite_size=2):
    # Ordenar por fitness
    sorted_pop = sorted(population, key=lambda x: fitness(x))
    
    # Preservar elite
    elite = sorted_pop[:elite_size]
    
    # Crossover no restante
    offspring = []
    for _ in range(len(population) - elite_size):
        p1, p2 = select_parents(sorted_pop)
        child = crossover(p1, p2, ...)
        offspring.append(child)
    
    # Combinar elite + offspring
    return elite + offspring
```

## Análise de Desempenho

### Métricas de Qualidade

**Taxa de Melhoria:**
```python
def improvement_rate(parent1_fitness, parent2_fitness, child_fitness):
    avg_parent_fitness = (parent1_fitness + parent2_fitness) / 2
    improvement = (avg_parent_fitness - child_fitness) / avg_parent_fitness
    return improvement * 100  # Percentual
```

**Diversidade Gerada:**
```python
def diversity_score(child, parent1, parent2):
    # Hamming distance (posições diferentes)
    diff_p1 = sum(1 for i in range(len(child)) if child[i] != parent1[i])
    diff_p2 = sum(1 for i in range(len(child)) if child[i] != parent2[i])
    return (diff_p1 + diff_p2) / (2 * len(child))
```

### Benchmarking

```python
import time

def benchmark_crossover_methods(n_tests=1000):
    rbx_times = []
    bcrc_times = []
    
    for _ in range(n_tests):
        # RBX
        start = time.time()
        child = RBX(parent1, parent2, deliveries, vehicles, center)
        rbx_times.append(time.time() - start)
        
        # BCRC
        start = time.time()
        child = BCRC(parent1, parent2, deliveries)
        bcrc_times.append(time.time() - start)
    
    print(f"RBX médio: {sum(rbx_times)/n_tests*1000:.2f} ms")
    print(f"BCRC médio: {sum(bcrc_times)/n_tests*1000:.2f} ms")
    print(f"BCRC é {sum(bcrc_times)/sum(rbx_times):.1f}x mais lento")
```

**Resultados Típicos:**
```
RBX médio: 0.15 ms
BCRC médio: 2.30 ms
BCRC é 15.3x mais lento
```

## Limitações e Melhorias Possíveis

### Limitações Atuais

1. **BCRC busca local:** Não considera estrutura global de veículos
2. **RBX sem otimização:** Não avalia qualidade durante construção
3. **Sem cache:** Recalcula distâncias repetidamente
4. **Posições fixas:** Não adapta estratégia baseada em convergência

### Melhorias Propostas

#### 1. Crossover Multi-Ponto (MPX)

```python
def MPX(parent1, parent2, n_points=2):
    points = sorted(random.sample(range(len(parent1)), n_points))
    child = []
    use_p1 = True
    
    for i in range(len(points) + 1):
        start = 0 if i == 0 else points[i-1]
        end = len(parent1) if i == len(points) else points[i]
        
        segment = parent1[start:end] if use_p1 else parent2[start:end]
        child.extend([g for g in segment if g not in child])
        use_p1 = not use_p1
    
    return child
```

#### 2. Order Crossover (OX)

```python
def OX(parent1, parent2):
    i, j = sorted(random.sample(range(len(parent1)), 2))
    child = [None] * len(parent1)
    child[i:j] = parent1[i:j]
    
    pos = j
    for gene in parent2[j:] + parent2[:j]:
        if gene not in child:
            if pos >= len(child):
                pos = 0
            child[pos] = gene
            pos += 1
    
    return child
```

#### 3. Cache de Distâncias

```python
_distance_cache = {}

def cached_manhattan(coord1, coord2):
    key = (coord1, coord2)
    if key not in _distance_cache:
        _distance_cache[key] = manhattan(coord1, coord2)
    return _distance_cache[key]
```

#### 4. BCRC com Heurística

```python
def BCRC_heuristic(parent1, parent2, deliveries, k=5):
    # Testar apenas k posições mais promissoras
    # baseado em proximidade geográfica
    i, j = sorted(random.sample(range(len(parent1)), 2))
    subroute = parent1[i:j]
    base = [g for g in parent2 if g not in subroute]
    
    # Avaliar apenas k posições centrais
    candidates = []
    step = len(base) // k
    for pos in range(0, len(base), step):
        candidate = base[:pos] + subroute + base[pos:]
        cost = calculate_cost(candidate, deliveries)
        candidates.append((cost, pos))
    
    best_pos = min(candidates, key=lambda x: x[0])[1]
    return base[:best_pos] + subroute + base[best_pos:]
```

## Palavras-chave para Busca

- Crossover genético
- Operador de cruzamento
- RBX Route-Based Crossover
- BCRC Best Cost Route Crossover
- Recombinação de cromossomos
- Herança genética
- Exploração vs otimização
- Inserção ótima
- Distância Manhattan crossover
- Sub-rota preservação
- Algoritmo genético VRP
- Operadores reprodutivos
- Probabilidade de crossover
- Diversidade populacional
- Busca exaustiva inserção
- Order Crossover OX
- Multi-point crossover
- Elitismo GA

## Referências Técnicas

### Complexidade Computacional
- **RBX:** $O(n)$ - Linear no número de entregas
- **BCRC:** $O(n^2)$ - Quadrático (n posições × n custo)
- **crossover():** $O(n)$ ou $O(n^2)$ dependendo da escolha

### Notação
- $n$: Número total de entregas
- $m$: Número de veículos
- $p_{rbx}$: Probabilidade de usar RBX
- $P_1, P_2$: Cromossomos parentais
- $C$: Cromossomo filho (offspring)
- $SR$: Sub-rota (subroute)
- $d(A,B)$: Distância Manhattan entre A e B

### Bibliografia Recomendada
- Goldberg, D. E. (1989). *Genetic Algorithms in Search, Optimization, and Machine Learning*
- Mitchell, M. (1998). *An Introduction to Genetic Algorithms*
- Potvin, J. Y. (1996). *Genetic algorithms for the traveling salesman problem*
- Davis, L. (1991). *Handbook of Genetic Algorithms*

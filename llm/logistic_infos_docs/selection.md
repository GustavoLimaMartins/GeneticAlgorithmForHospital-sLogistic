# Módulo de Seleção - Algoritmo Genético para Otimização Logística

## Visão Geral

O módulo `f_selection.py` implementa mecanismos de seleção para o algoritmo genético, responsáveis por escolher quais indivíduos da população atual terão a oportunidade de gerar descendentes para a próxima geração. Este módulo combina duas estratégias fundamentais: **Elitismo** (preservação dos melhores) e **Seleção por Torneio** (competição justa), garantindo convergência sem perda de diversidade.

## Objetivo

Aplicar **pressão seletiva** à população, favorecendo indivíduos com melhor fitness (menor custo) para reprodução, enquanto mantém diversidade genética suficiente para evitar convergência prematura. O módulo implementa o princípio darwiniano de "sobrevivência do mais apto" no contexto de otimização logística.

## Fundamento em Algoritmos Genéticos

### Princípio da Seleção Natural

A seleção é a força motriz da evolução artificial:

```
População Geração N (100 indivíduos)
    ↓
Avaliação de Fitness
    ↓
┌─────────────────────────────────────────┐
│ Fitness: [1250, 1180, 1420, 980, ...]   │
│          ▼ menor = melhor                │
└─────────────────────────────────────────┘
    ↓
Seleção (pressão seletiva)
    ↓
┌─────────────────────────────────────────┐
│ Selecionados (melhores + torneio)       │
│ Maior probabilidade para baixo fitness  │
└─────────────────────────────────────────┘
    ↓
Crossover + Mutação
    ↓
População Geração N+1
```

**Analogia Biológica:**
- **Ambiente hostil:** Função de fitness (custos, restrições)
- **Adaptação:** Soluções com menor custo "sobrevivem"
- **Reprodução:** Selecionados geram descendentes
- **Herança:** Crossover transmite características

### Pressão Seletiva

$$P_{seleção}(i) = f(\text{fitness}_i, \text{população})$$

Onde:
- Indivíduos com **melhor fitness** têm **maior probabilidade** de seleção
- Mas não é determinístico (permite alguma aleatoriedade)
- Balanceia exploração (diversidade) e explotação (convergência)

### Problema de Minimização

**Importante:** No nosso problema, **fitness menor = solução melhor**

$$\text{Objetivo: } \min F(x)$$

Portanto:
- Fitness = 1000 é **melhor** que Fitness = 1500
- Elite: Menores valores de fitness
- Torneio: Vence o de menor fitness

## Estratégias de Seleção Implementadas

### 1. Tournament Selection (Seleção por Torneio)

#### Conceito

Realiza "torneios" entre $k$ indivíduos escolhidos aleatoriamente, selecionando o **melhor** (menor fitness) como vencedor. Este vencedor é escolhido para reprodução.

#### Algoritmo Detalhado

**Assinatura:**
```python
def tournament_selection(population: list[dict], k: int = 2) -> dict
```

**Parâmetros:**
- `population`: Lista de indivíduos com seus cromossomos e fitness
- `k`: Tamanho do torneio (número de competidores, padrão: 2)

**Retorno:**
- Indivíduo vencedor (menor fitness entre os k selecionados)

**Processo:**

```
1. Escolher k indivíduos aleatoriamente da população
   contenders = random.sample(population, k)
   
   Exemplo com k=3:
   População = [Ind1(fit=1200), Ind2(fit=980), Ind3(fit=1450), 
                Ind4(fit=1100), Ind5(fit=1350), ...]
   
   Sorteados: [Ind2(fit=980), Ind4(fit=1100), Ind5(fit=1350)]

2. Comparar fitness de todos os competidores
   Competidores: 980, 1100, 1350

3. Selecionar o MELHOR (menor fitness)
   winner = min(contenders, key=lambda ind: ind["fitness"])
   
   Vencedor: Ind2 com fitness=980

4. Retornar vencedor
   return Ind2
```

#### Exemplo Prático

**População de 10 indivíduos:**
```python
population = [
    {"chromosome": [1,2,3,...], "fitness": 1250},  # Ind 0
    {"chromosome": [5,1,8,...], "fitness": 1180},  # Ind 1 ✓
    {"chromosome": [3,7,2,...], "fitness": 1420},  # Ind 2
    {"chromosome": [9,4,1,...], "fitness": 980},   # Ind 3 ★ ELITE
    {"chromosome": [2,6,5,...], "fitness": 1350},  # Ind 4
    {"chromosome": [7,3,9,...], "fitness": 1090},  # Ind 5 ✓
    {"chromosome": [4,8,6,...], "fitness": 1280},  # Ind 6
    {"chromosome": [6,9,7,...], "fitness": 1150},  # Ind 7 ✓
    {"chromosome": [8,5,4,...], "fitness": 1390},  # Ind 8
    {"chromosome": [10,2,11,..],"fitness": 1220},  # Ind 9
]
```

**Torneio 1 (k=3):**
```python
# Sorteio
contenders = [Ind2(1420), Ind5(1090), Ind9(1220)]

# Comparação
fitness_values = [1420, 1090, 1220]

# Vencedor
winner = Ind5 (fitness=1090)  # Menor fitness
```

**Torneio 2 (k=2):**
```python
# Sorteio
contenders = [Ind0(1250), Ind7(1150)]

# Vencedor
winner = Ind7 (fitness=1150)  # Menor fitness
```

#### Características Matemáticas

**Probabilidade de Seleção:**

Para um indivíduo com rank $r$ (1 = melhor, N = pior) em população de tamanho $N$:

$$P(\text{seleção}) = \frac{1}{N} \left[1 - \left(\frac{r-1}{N}\right)^k\right]$$

**Efeito do tamanho do torneio (k):**

| k | Pressão Seletiva | Diversidade | Características |
|---|------------------|-------------|-----------------|
| 2 | Baixa-Média | Alta | Mais aleatório, explora mais |
| 3 | Média | Média | Balanceado (recomendado) |
| 4 | Média-Alta | Média-Baixa | Favorece elite moderadamente |
| 5+ | Alta | Baixa | Quase determinístico |

**Vantagens do k=2 (padrão):**
- Boa diversidade mantida
- Implementação eficiente
- Pressão seletiva suficiente
- Amplamente validado na literatura

#### Propriedades Importantes

**1. Aleatoriedade Controlada**
```python
# Mesmo o pior pode ser selecionado
# se competir apenas com outros ruins
worst_individual = population[-1]  # Pior fitness

# Torneio: [pior, segundo_pior]
# Pior pode vencer se competir apenas com segundo pior
```

**2. Não Requer Normalização**
```python
# Funciona com qualquer escala de fitness
# Não precisa converter para probabilidades
# Apenas comparação ordinal
```

**3. Independência de Escala**
```python
# Fitness: [100, 200, 300] ou [1000000, 2000000, 3000000]
# Resultado é o mesmo (comparação relativa)
```

#### Vantagens e Desvantagens

**Vantagens:**
- ✅ Simples de implementar
- ✅ Computacionalmente eficiente: O(k)
- ✅ Não requer cálculo de probabilidades
- ✅ Mantém diversidade (todos podem ser selecionados)
- ✅ Pressão seletiva ajustável via k
- ✅ Funciona bem com fitness negativos
- ✅ Paralelizável

**Desvantagens:**
- ❌ Aleatoriedade pode selecionar indivíduos ruins
- ❌ Sem garantia de convergência rápida
- ❌ Pode perder melhor solução (sem elitismo)

**Complexidade:**
- **Tempo:** O(k) por seleção, O(k × pop_size) total
- **Espaço:** O(k) para armazenar competidores

### 2. Elitist Selection (Seleção Elitista)

#### Conceito

Preserva os **melhores indivíduos** da população atual, garantindo que passem diretamente para a próxima geração **sem alterações**. Implementa o princípio: "não destrua o que já é bom".

#### Algoritmo Detalhado

**Assinatura:**
```python
def get_elite(population: list[dict], elite_ratio: float = 0.035) -> list[dict]
```

**Parâmetros:**
- `population`: Lista completa de indivíduos
- `elite_ratio`: Proporção da população considerada elite (padrão: 3.5%)

**Retorno:**
- Lista dos melhores indivíduos (ordenados por fitness crescente)

**Processo:**

```
1. Calcular tamanho da elite
   elite_size = max(1, int(len(population) * elite_ratio))
   
   Exemplo: population_size = 100
   elite_size = max(1, int(100 × 0.035))
   elite_size = max(1, 3) = 3

2. Ordenar população por fitness (crescente = melhor primeiro)
   sorted_population = sorted(population, key=lambda ind: ind["fitness"])
   
   Resultado:
   [Ind3(980), Ind5(1090), Ind7(1150), Ind1(1180), ...]
    └─ melhor                                pior ─┘

3. Extrair os elite_size primeiros
   elite = sorted_population[:elite_size]
   
   elite = [Ind3(980), Ind5(1090), Ind7(1150)]

4. Retornar elite
   return elite
```

#### Exemplo Prático

**População de 100 indivíduos:**
```python
# Fitness variando de 980 (melhor) a 2500 (pior)
population_size = 100
elite_ratio = 0.035

# Cálculo
elite_size = max(1, int(100 * 0.035))
elite_size = max(1, 3) = 3

# Após ordenação por fitness
sorted_pop = [
    {"chromosome": [...], "fitness": 980},   # Rank 1 ← ELITE
    {"chromosome": [...], "fitness": 1020},  # Rank 2 ← ELITE
    {"chromosome": [...], "fitness": 1050},  # Rank 3 ← ELITE
    {"chromosome": [...], "fitness": 1180},  # Rank 4
    {"chromosome": [...], "fitness": 1220},  # Rank 5
    ...
    {"chromosome": [...], "fitness": 2500},  # Rank 100 (pior)
]

# Elite selecionada
elite = sorted_pop[:3]  # Top 3 indivíduos
```

#### Taxa de Elitismo (elite_ratio)

**Configuração Padrão: 3.5%**

$$\text{elite\_size} = \max\left(1, \lfloor N \times 0.035 \rfloor\right)$$

**Exemplos para diferentes tamanhos de população:**

| Pop. Size | elite_ratio | Cálculo | Elite Size |
|-----------|-------------|---------|------------|
| 50 | 3.5% | max(1, 1.75) | 2 |
| 100 | 3.5% | max(1, 3.5) | 3 |
| 200 | 3.5% | max(1, 7.0) | 7 |
| 500 | 3.5% | max(1, 17.5) | 17 |
| 20 | 3.5% | max(1, 0.7) | 1 |

**Garantia:** `max(1, ...)` assegura que **sempre** haja pelo menos 1 elite.

#### Escolha do Valor 3.5%

**Justificativa:**

1. **Literatura:** Valores comuns variam de 1-10%
2. **Balanceamento:** 
   - < 1%: Elite muito pequena, pode perder melhor solução
   - 3-5%: Ideal (compromisso entre preservação e renovação)
   - > 10%: Estagnação, pouca renovação

3. **Impacto Computacional:**
   ```
   Elite 3.5% em pop=100: 3 indivíduos preservados
   - 3% da população sem custo de crossover/mutação
   - 97% passa por operadores genéticos
   ```

4. **Convergência vs Diversidade:**
   ```
   3.5% garante:
   ✓ Melhor solução nunca se perde
   ✓ Top 3-5 soluções preservadas
   ✓ 96.5% da população evolui normalmente
   ✓ Pressão seletiva moderada
   ```

#### Variações de Elite Ratio

```python
# Muito conservador (convergência lenta, alta diversidade)
elite_ratio = 0.01  # 1%

# Padrão balanceado
elite_ratio = 0.035  # 3.5%

# Agressivo (convergência rápida, menor diversidade)
elite_ratio = 0.10  # 10%

# Adaptativo
def adaptive_elite_ratio(generation, max_gen):
    # Começa com 1%, termina com 10%
    progress = generation / max_gen
    return 0.01 + (0.09 * progress)
```

#### Propriedades Importantes

**1. Monotonicidade de Convergência**
$$F_{best}(t+1) \leq F_{best}(t)$$

Com elitismo, o melhor fitness **nunca piora** entre gerações.

**2. Garantia de Preservação**
```python
# Melhor solução da geração N
best_gen_n = min(population, key=lambda x: x["fitness"])

# Sempre estará na geração N+1 (via elite)
assert best_gen_n in next_generation
```

**3. Convergência Garantida**
- Teorema: Com elitismo, AG converge para ótimo global (sob certas condições)
- Prática: Converge para ótimo local de alta qualidade

#### Vantagens e Desvantagens

**Vantagens:**
- ✅ **Garante** que melhor solução não se perca
- ✅ Acelera convergência
- ✅ Monotonia: fitness nunca piora
- ✅ Simples de implementar
- ✅ Computacionalmente barato (apenas sort)

**Desvantagens:**
- ❌ Pode causar convergência prematura se elite_ratio muito alto
- ❌ Reduz diversidade genética se excessivo
- ❌ Elite pode dominar população (se ratio alto)

**Complexidade:**
- **Tempo:** O(N log N) para ordenação
- **Espaço:** O(elite_size) para armazenar elite

### 3. Hybrid Selection (Seleção Híbrida): Elitismo + Torneio

#### Conceito

Combina as vantagens de ambas estratégias: **elitismo** garante preservação dos melhores, enquanto **torneio** preenche o restante com seleção baseada em competição, mantendo diversidade.

#### Algoritmo Completo

**Assinatura:**
```python
def select_next_generation(
    population: list[dict],
    pop_size: int,
    elite_ratio: float = 0.035,
    tournament_k: int = 2
) -> list[dict]
```

**Parâmetros:**
- `population`: População atual (geração N)
- `pop_size`: Tamanho desejado da próxima população
- `elite_ratio`: Proporção de elite (padrão: 3.5%)
- `tournament_k`: Tamanho do torneio (padrão: 2)

**Retorno:**
- Nova população selecionada (geração N+1, antes de crossover/mutação)

**Processo Detalhado:**

```
1. FASE ELITISTA
   ──────────────
   elite = get_elite(population, elite_ratio)
   selected = elite[:]  # Cópia da elite
   
   Exemplo (pop_size=100):
   elite_size = 3
   selected = [Ind3(980), Ind5(1090), Ind7(1150)]
   len(selected) = 3

2. FASE TORNEIO
   ─────────────
   while len(selected) < pop_size:
       parent = tournament_selection(population, k=tournament_k)
       selected.append(parent)
   
   Iterações:
   - Iteração 1: Torneio → Ind1(1180) → selected = [elite..., Ind1]
   - Iteração 2: Torneio → Ind5(1090) → selected = [elite..., Ind1, Ind5]
   - Iteração 3: Torneio → Ind7(1150) → selected = [elite..., Ind1, Ind5, Ind7]
   - ...continua...
   - Iteração 97: Torneio → IndX → selected = [100 indivíduos]

3. RETORNO
   ────────
   return selected  # Exatamente pop_size indivíduos
```

#### Exemplo Completo Passo a Passo

**Configuração Inicial:**
```python
# População atual (geração N)
population_size = 50
population = [
    {"chromosome": [1,5,8,...], "fitness": 980},    # Melhor
    {"chromosome": [3,7,2,...], "fitness": 1020},   # 2º melhor
    {"chromosome": [9,4,1,...], "fitness": 1050},   # 3º melhor
    {"chromosome": [2,6,5,...], "fitness": 1180},
    {"chromosome": [7,3,9,...], "fitness": 1220},
    ...  # 45 indivíduos restantes
    {"chromosome": [8,5,4,...], "fitness": 2450},   # Pior
]

# Parâmetros
elite_ratio = 0.035  # 3.5%
tournament_k = 2
target_pop_size = 50
```

**Execução:**

```python
# ETAPA 1: Selecionar Elite
elite_size = max(1, int(50 * 0.035))  # = 1 (só o melhor)
elite = [
    {"chromosome": [1,5,8,...], "fitness": 980}
]
selected = elite[:]
print(f"Elite: {len(selected)} indivíduos")  # 1

# ETAPA 2: Preencher com Torneios
# Faltam: 50 - 1 = 49 indivíduos

# Torneio 1
contenders_1 = [population[10], population[23]]  # Aleatório
winner_1 = min(contenders_1, key=lambda x: x["fitness"])
selected.append(winner_1)  # len=2

# Torneio 2
contenders_2 = [population[5], population[37]]
winner_2 = min(contenders_2, key=lambda x: x["fitness"])
selected.append(winner_2)  # len=3

# ... continua por 47 torneios ...

# Torneio 49
contenders_49 = [population[42], population[18]]
winner_49 = min(contenders_49, key=lambda x: x["fitness"])
selected.append(winner_49)  # len=50

# ETAPA 3: Verificação
assert len(selected) == 50
print(f"População selecionada: {len(selected)} indivíduos")
```

#### Distribuição da Seleção

**Composição da População Selecionada:**

```
┌──────────────────────────────────────────────┐
│ Geração N+1 (antes de crossover/mutação)    │
├──────────────────────────────────────────────┤
│                                              │
│ Elite (3.5%): [■■]                          │
│   - Copiados identicamente                   │
│   - Melhor fitness garantido                 │
│                                              │
│ Torneio (96.5%): [■■■■■■■■■■■■■■■■■■■■]    │
│   - Seleção competitiva                      │
│   - Bias para melhores fitness               │
│   - Mantém diversidade                       │
│                                              │
└──────────────────────────────────────────────┘
```

**Probabilidade de Seleção por Quartil:**

| Quartil | Fitness | P(Elite) | P(Torneio k=2) | P(Total) |
|---------|---------|----------|----------------|----------|
| Top 25% | Melhor | ~14% | ~44% | ~50% |
| 25-50% | Bom | 0% | ~31% | ~28% |
| 50-75% | Médio | 0% | ~19% | ~17% |
| Bottom 25% | Ruim | 0% | ~6% | ~5% |

**Interpretação:**
- Elite: Garantia absoluta para top 3.5%
- Melhores têm alta probabilidade via torneio
- Piores ainda têm chance (diversidade)

#### Fluxo Evolutivo Completo

```
┌─────────────────────────────────────────────────┐
│ GERAÇÃO N (100 indivíduos avaliados)           │
│ Fitness: [980, 1020, 1050, ..., 2450]          │
└───────────────────┬─────────────────────────────┘
                    ↓
        ┌───────────────────────┐
        │ f_selection.py        │
        │ select_next_generation│
        └───────────┬───────────┘
                    ↓
        ┌──────────────────────┐
        │ 1. Elite (3%)        │
        │    [980, 1020, 1050] │
        └──────────┬───────────┘
                   ↓
        ┌──────────────────────┐
        │ 2. Torneio (97%)     │
        │    97 seleções       │
        └──────────┬───────────┘
                   ↓
┌───────────────────────────────────────────────────┐
│ PAIS SELECIONADOS (100 indivíduos)               │
│ - Elite preservada                                │
│ - Restante via competição                         │
└────────────────────┬──────────────────────────────┘
                     ↓
        ┌────────────────────────┐
        │ d_crossover.py         │
        │ (pares de pais → filhos│
        └────────────┬───────────┘
                     ↓
        ┌────────────────────────┐
        │ e_mutation.py          │
        │ (mutação nos filhos)   │
        └────────────┬───────────┘
                     ↓
        ┌────────────────────────┐
        │ c_fitness.py           │
        │ (avaliar nova geração) │
        └────────────┬───────────┘
                     ↓
┌───────────────────────────────────────────────────┐
│ GERAÇÃO N+1 (100 indivíduos avaliados)           │
│ Fitness médio melhorado                           │
└───────────────────────────────────────────────────┘
```

#### Propriedades da Seleção Híbrida

**1. Convergência Garantida**
$$\min_{i \in \text{Gen}_{N+1}} F_i \leq \min_{i \in \text{Gen}_N} F_i$$

Elitismo garante que melhor fitness nunca piora.

**2. Diversidade Mantida**
```python
# Torneio permite seleção de indivíduos médios/ruins
# Diversidade = probabilidade de exploração
diversity_factor = (pop_size - elite_size) / pop_size
# = 96.5% (alta diversidade mantida)
```

**3. Intensificação Progressiva**
```python
# Ao longo das gerações:
# - Elite sempre representa os melhores
# - Torneio favorece cada vez mais bons indivíduos
#   (pois população melhora)
# - Convergência natural sem forçar
```

## Análise Teórica e Comparações

### Comparação com Outras Estratégias

#### Roulette Wheel Selection (Roleta)

**Conceito:** Probabilidade proporcional ao fitness inverso.

$$P_i = \frac{f_{max} - f_i}{\sum_{j=1}^N (f_{max} - f_j)}$$

**Problemas:**
- ❌ Requer normalização complexa
- ❌ Sensível a escala de fitness
- ❌ Fitness negativos causam problemas
- ❌ Convergência prematura se um indivíduo dominar

**Por que NÃO usamos:**
- Torneio é mais simples
- Torneio não precisa normalizar
- Torneio controla pressão via k

#### Rank Selection (Seleção por Ranking)

**Conceito:** Probabilidade baseada em rank, não fitness absoluto.

$$P_i = \frac{2 - s + 2(s-1)(r_i - 1)}{N(N-1)}$$

Onde $s$ é pressão seletiva e $r_i$ é rank.

**Vantagens sobre Roleta:**
- ✓ Independente de escala
- ✓ Funciona com fitness negativos

**Por que preferimos Torneio:**
- Torneio é mais eficiente: O(k) vs O(N log N)
- Torneio é mais simples de implementar
- Torneio oferece controle intuitivo (k)

#### Stochastic Universal Sampling (SUS)

**Conceito:** Múltiplos ponteiros equidistantes na roleta.

**Vantagens:**
- ✓ Menor variância que roleta simples
- ✓ Garante representação proporcional

**Por que preferimos Torneio + Elitismo:**
- Nossa combinação oferece:
  - Garantia de elite (melhor que SUS)
  - Simplicidade de implementação
  - Eficiência computacional

### Análise de Convergência

#### Velocidade de Convergência

**Com Elitismo:**
```
Geração 0:    Fitness médio = 2000, Melhor = 1500
Geração 10:   Fitness médio = 1600, Melhor = 1200 ✓ Melhorou
Geração 20:   Fitness médio = 1300, Melhor = 1000 ✓ Melhorou
Geração 50:   Fitness médio = 1050, Melhor = 950  ✓ Melhorou
Geração 100:  Fitness médio = 980,  Melhor = 950  ✓ Manteve
```

**Sem Elitismo:**
```
Geração 0:    Fitness médio = 2000, Melhor = 1500
Geração 10:   Fitness médio = 1600, Melhor = 1200 ✓
Geração 20:   Fitness médio = 1300, Melhor = 1050 ✓
Geração 50:   Fitness médio = 1100, Melhor = 1150 ✗ PIOROU!
Geração 100:  Fitness médio = 1000, Melhor = 1020 ✗ Nunca recuperou
```

**Teorema (Rudolph, 1994):**
> Algoritmo genético com elitismo converge para ótimo global com probabilidade 1.

#### Diversidade ao Longo do Tempo

$$D(t) = \frac{1}{N(N-1)} \sum_{i=1}^N \sum_{j=i+1}^N d_H(C_i, C_j)$$

Onde $d_H$ é distância de Hamming.

**Curva Típica:**
```
Diversidade
    ↑
100%│●
    │ ●
 75%│  ●●
    │    ●●
 50%│      ●●
    │        ●●●
 25%│           ●●●●
    │               ●●●●●●
  0%└────────────────────────●●●● → Gerações
    0   20   40   60   80  100
```

**Fases:**
1. **Alta diversidade inicial** (gerações 0-20)
2. **Convergência gradual** (gerações 20-70)
3. **Estabilização** (gerações 70-100)

**Elitismo + Torneio mantém:**
- Diversidade suficiente (torneio não é determinístico)
- Convergência progressiva (elite guia evolução)

## Casos de Uso e Configurações

### Configurações Recomendadas

#### Problema Pequeno (< 50 indivíduos)

```python
select_next_generation(
    population=population,
    pop_size=30,
    elite_ratio=0.05,      # 5% - maior proporção
    tournament_k=2         # Baixa pressão
)
# Elite: 1-2 indivíduos
# Favorece diversidade
```

#### Problema Médio (50-200 indivíduos)

```python
select_next_generation(
    population=population,
    pop_size=100,
    elite_ratio=0.035,     # 3.5% (padrão)
    tournament_k=2         # Padrão
)
# Elite: 3-7 indivíduos
# Balanceado (recomendado)
```

#### Problema Grande (> 200 indivíduos)

```python
select_next_generation(
    population=population,
    pop_size=500,
    elite_ratio=0.02,      # 2% - menor proporção
    tournament_k=3         # Maior pressão
)
# Elite: 10 indivíduos
# Convergência mais rápida
```

### Estratégias Adaptativas

#### Elite Ratio Adaptativo

```python
def adaptive_elite_ratio(generation, max_generations, 
                         start_ratio=0.01, end_ratio=0.10):
    """
    Aumenta elite ao longo do tempo
    Início: Exploração (baixa elite)
    Final: Explotação (alta elite)
    """
    progress = generation / max_generations
    return start_ratio + (end_ratio - start_ratio) * progress

# Uso
for gen in range(max_generations):
    elite_ratio = adaptive_elite_ratio(gen, max_generations)
    selected = select_next_generation(
        population, pop_size, elite_ratio=elite_ratio
    )
```

#### Tournament K Adaptativo

```python
def adaptive_tournament_k(generation, max_generations,
                          start_k=2, end_k=5):
    """
    Aumenta pressão seletiva ao longo do tempo
    """
    progress = generation / max_generations
    k = start_k + int((end_k - start_k) * progress)
    return max(2, k)  # Mínimo k=2

# Uso
for gen in range(max_generations):
    k = adaptive_tournament_k(gen, max_generations)
    selected = select_next_generation(
        population, pop_size, tournament_k=k
    )
```

#### Elitismo Dinâmico Baseado em Estagnação

```python
def dynamic_elite_ratio(generations_without_improvement,
                        base_ratio=0.035):
    """
    Aumenta elite se não houver melhoria
    (força convergência)
    """
    if generations_without_improvement > 20:
        return min(base_ratio * 3, 0.15)  # Triplo, max 15%
    elif generations_without_improvement > 10:
        return min(base_ratio * 2, 0.10)  # Duplo, max 10%
    else:
        return base_ratio  # Normal
```

## Integração no Loop Evolutivo

### Pseudocódigo Completo

```python
def genetic_algorithm(city, pop_size=100, max_generations=200):
    # Inicialização
    population = generate_population_coordinates(city, pop_size)
    
    # Avaliar população inicial
    for individual in population:
        chromosome = individual  # Lista de entregas
        fitness = calculate_fitness(chromosome, city)
        individual = {"chromosome": chromosome, "fitness": fitness}
    
    best_ever = min(population, key=lambda x: x["fitness"])
    
    # Loop evolutivo
    for generation in range(max_generations):
        
        # 1. SELEÇÃO (aqui!)
        selected_parents = select_next_generation(
            population=population,
            pop_size=pop_size,
            elite_ratio=0.035,
            tournament_k=2
        )
        
        # 2. REPRODUÇÃO
        offspring = []
        for i in range(0, len(selected_parents), 2):
            parent1 = selected_parents[i]["chromosome"]
            parent2 = selected_parents[i+1]["chromosome"]
            
            # Crossover
            child = crossover(parent1, parent2, deliveries, vehicles, center)
            
            # Mutação
            child = light_mutation(child, prob=0.15)
            
            offspring.append(child)
        
        # 3. AVALIAÇÃO
        population = []
        for chromosome in offspring:
            fitness = calculate_fitness(chromosome, city)
            population.append({"chromosome": chromosome, "fitness": fitness})
        
        # 4. ATUALIZAR MELHOR
        current_best = min(population, key=lambda x: x["fitness"])
        if current_best["fitness"] < best_ever["fitness"]:
            best_ever = current_best
            print(f"Gen {generation}: Nova melhor solução! Fitness={best_ever['fitness']:.2f}")
    
    return best_ever
```

### Estrutura de Dados

**Indivíduo (antes da seleção):**
```python
individual = {
    "chromosome": [1, 5, 8, 12, 20, 2, 7, 15, ...],  # Lista de IDs
    "fitness": 1250.75  # Valor float
}
```

**População:**
```python
population = [
    {"chromosome": [...], "fitness": 980},
    {"chromosome": [...], "fitness": 1020},
    ...
    {"chromosome": [...], "fitness": 2450}
]
```

## Métricas de Avaliação

### Pressão Seletiva

```python
def selective_pressure(population, selected):
    """
    Mede quão mais "forte" é a seleção comparada à aleatória
    
    SP = fitness_avg_population / fitness_avg_selected
    SP > 1: Seleção favorece melhores
    SP = 1: Seleção aleatória
    """
    avg_pop = sum(ind["fitness"] for ind in population) / len(population)
    avg_sel = sum(ind["fitness"] for ind in selected) / len(selected)
    
    return avg_pop / avg_sel

# Valores típicos:
# SP = 1.2-1.5: Pressão moderada (ideal)
# SP > 2.0: Pressão alta (risco de convergência prematura)
# SP < 1.1: Pressão baixa (convergência lenta)
```

### Taxa de Substituição

```python
def replacement_rate(old_pop, new_pop):
    """
    Percentual de novos indivíduos (não-elite)
    """
    old_chromosomes = {tuple(ind["chromosome"]) for ind in old_pop}
    new_chromosomes = {tuple(ind["chromosome"]) for ind in new_pop}
    
    unique_new = new_chromosomes - old_chromosomes
    return len(unique_new) / len(new_pop) * 100

# Com elite_ratio=3.5%:
# Taxa esperada: ~96.5%
```

### Intensificação vs Diversificação

```python
def exploitation_vs_exploration(selected, elite_size):
    """
    Razão entre explotação (elite) e exploração (torneio)
    """
    exploitation = elite_size / len(selected)
    exploration = 1 - exploitation
    
    return {
        "exploitation": exploitation * 100,  # %
        "exploration": exploration * 100      # %
    }

# Resultado típico:
# {"exploitation": 3.5%, "exploration": 96.5%}
```

## Limitações e Melhorias

### Limitações Atuais

1. **Elite ratio fixo:** Não se adapta automaticamente
2. **Tournament k fixo:** Pressão constante ao longo de gerações
3. **Sem diversidade mínima:** Pode convergir prematuramente
4. **Duplicatas:** Torneio pode selecionar mesmo indivíduo múltiplas vezes

### Melhorias Propostas

#### 1. Seleção com Diversidade Forçada

```python
def diverse_selection(population, pop_size, min_diversity=0.3):
    """
    Garante diversidade mínima na seleção
    """
    selected = get_elite(population, elite_ratio=0.035)
    
    while len(selected) < pop_size:
        candidate = tournament_selection(population, k=2)
        
        # Verificar se adiciona diversidade suficiente
        avg_distance = sum(
            hamming_distance(candidate["chromosome"], s["chromosome"]) 
            for s in selected
        ) / len(selected)
        
        threshold = len(candidate["chromosome"]) * min_diversity
        
        if avg_distance >= threshold:
            selected.append(candidate)
        # else: rejeitar e tentar outro
    
    return selected
```

#### 2. Fitness Sharing (Compartilhamento de Fitness)

```python
def fitness_sharing(population, niche_radius=0.1):
    """
    Penaliza indivíduos similares (promove diversidade)
    """
    for i, ind_i in enumerate(population):
        niche_count = 0
        
        for j, ind_j in enumerate(population):
            distance = hamming_distance(
                ind_i["chromosome"], 
                ind_j["chromosome"]
            ) / len(ind_i["chromosome"])
            
            if distance < niche_radius:
                niche_count += 1
        
        # Ajustar fitness (maior niche_count = pior fitness)
        ind_i["shared_fitness"] = ind_i["fitness"] * niche_count
```

#### 3. Boltzmann Selection (Seleção Temperada)

```python
def boltzmann_tournament(population, temperature, k=2):
    """
    Temperatura controla aleatoriedade
    Alta T: Mais aleatório (exploração)
    Baixa T: Mais determinístico (explotação)
    """
    contenders = random.sample(population, k)
    
    # Calcular probabilidades baseadas em fitness e temperatura
    probabilities = []
    for ind in contenders:
        prob = math.exp(-ind["fitness"] / temperature)
        probabilities.append(prob)
    
    # Normalizar
    total = sum(probabilities)
    probabilities = [p/total for p in probabilities]
    
    # Seleção estocástica
    return random.choices(contenders, weights=probabilities)[0]
```

## Palavras-chave para Busca

- Seleção de indivíduos
- Tournament selection
- Seleção por torneio
- Elitist selection
- Elitismo em GA
- Pressão seletiva
- Survival of the fittest
- Hybrid selection
- Seleção híbrida
- Elite ratio
- População evolutiva
- Convergência garantida
- Diversidade genética
- Algoritmo genético seleção
- Roulette wheel selection
- Rank selection
- Fitness-based selection
- Parent selection
- Next generation selection
- Evolutionary pressure

## Referências Técnicas

### Complexidade Computacional

**get_elite():**
- Tempo: O(N log N) - ordenação
- Espaço: O(elite_size)

**tournament_selection():**
- Tempo: O(k) por seleção
- Espaço: O(k)

**select_next_generation():**
- Tempo: O(N log N + k × N) ≈ O(N log N)
- Espaço: O(N)

### Notação Matemática

- $N$: Tamanho da população
- $k$: Tamanho do torneio
- $\alpha$: Elite ratio (elite_ratio)
- $F_i$: Fitness do indivíduo $i$
- $P_i$: Probabilidade de seleção do indivíduo $i$
- $t$: Geração atual

### Teoremas Importantes

**Teorema de Convergência (Rudolph, 1994):**
> Algoritmo genético com elitismo e mutação não-zero converge para ótimo global com probabilidade 1 quando $t \to \infty$.

**Teorema de Holland (Schema):**
> Esquemas (padrões) acima da média recebem número exponencialmente crescente de tentativas em gerações sucessivas.

### Bibliografia

- Goldberg, D. E. (1989). *Genetic Algorithms in Search, Optimization, and Machine Learning*
- Miller, B. L., & Goldberg, D. E. (1995). *Genetic algorithms, tournament selection, and the effects of noise*
- Rudolph, G. (1994). *Convergence analysis of canonical genetic algorithms*
- Back, T., Fogel, D. B., & Michalewicz, Z. (1997). *Handbook of Evolutionary Computation*
- De Jong, K. A. (1975). *An analysis of the behavior of a class of genetic adaptive systems*

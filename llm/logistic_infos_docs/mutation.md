# Módulo de Mutação - Algoritmo Genético para Otimização Logística

## Visão Geral

O módulo `e_mutation.py` implementa operadores de mutação para o algoritmo genético, responsáveis por introduzir variabilidade genética na população através de pequenas alterações aleatórias nos cromossomos. Este módulo oferece três estratégias de mutação: **Swap Mutation** (troca), **Relocate Mutation** (realocação) e **Light Mutation** (mutação leve híbrida).

## Objetivo

Manter diversidade genética na população, evitar convergência prematura para ótimos locais, e possibilitar a exploração de novas regiões do espaço de soluções. A mutação é o mecanismo de **inovação** no algoritmo genético, complementando a **recombinação** do crossover.

## Fundamento em Algoritmos Genéticos

### Papel da Mutação

A mutação simula **erros de cópia** ou **variações aleatórias** na reprodução biológica:

```
Cromossomo Original: [1, 2, 3, 4, 5, 6, 7, 8, 9]
         ↓ Mutação (Swap)
Cromossomo Mutante:  [1, 2, 7, 4, 5, 6, 3, 8, 9]
                           ↑           ↑
                           └─── trocados ───┘
```

**Princípios:**
- **Diversidade:** Introduz genes/características não presentes nos pais
- **Exploração:** Permite escapar de ótimos locais
- **Inovação:** Gera soluções que não seriam alcançadas apenas por crossover
- **Baixa frequência:** Geralmente com probabilidades baixas (1-15%)

### Equilíbrio Exploração vs Explotação

```
Taxa de Mutação    Comportamento         Risco
─────────────────────────────────────────────────
Muito baixa (< 1%) Explotação excessiva  Convergência prematura
Baixa (1-5%)       Balanceado            Ideal para refinamento
Média (5-15%)      Exploração moderada   Bom para fuga de ótimos locais
Alta (> 15%)       Exploração excessiva  Busca aleatória, perde boas soluções
```

### Mutação vs Crossover

| Aspecto | Crossover | Mutação |
|---------|-----------|---------|
| **Função** | Recombina características existentes | Cria novas características |
| **Frequência** | Alta (60-95%) | Baixa (1-15%) |
| **Magnitude** | Grandes mudanças estruturais | Pequenas alterações locais |
| **Operandos** | 2 pais → 1 ou 2 filhos | 1 indivíduo → 1 mutante |
| **Propósito** | Explotação (combinar boas características) | Exploração (diversidade) |

## Técnicas de Mutação Implementadas

### 1. Swap Mutation (Mutação por Troca)

#### Conceito

Seleciona **dois genes aleatórios** no cromossomo e **troca suas posições**, preservando todos os genes mas alterando a ordem de duas entregas.

#### Algoritmo Detalhado

**Entrada:**
- `chromosome`: Lista de genes (IDs de entregas)
- `prob`: Probabilidade de mutação (padrão: 0.1 = 10%)

**Processo:**

```
1. Verificar se a mutação ocorrerá
   if random.random() > prob:
       return chromosome_copy  # Sem mutação (90% dos casos)

2. Selecionar dois índices aleatórios distintos
   i, j = random.sample(range(len(chromosome)), 2)
   
   Exemplo: len=25, i=3, j=17

3. Criar cópia do cromossomo
   mutant = chromosome[:]

4. Trocar os genes nas posições i e j
   mutant[i], mutant[j] = mutant[j], mutant[i]

5. Retornar mutante
   return mutant
```

**Saída:**
- Cromossomo mutado com dois genes trocados, ou cópia inalterada

#### Exemplo Detalhado

**Configuração:**
```python
# Cromossomo original (25 entregas)
chromosome = [1, 5, 8, 12, 20, 2, 7, 15, 18, 23, 3, 6, 9, 14, 22,
              4, 10, 13, 17, 21, 11, 16, 19, 24, 25]

# Probabilidade de mutação
prob = 0.1  # 10%
```

**Execução:**

```python
# 1. Sorteio: random.random() = 0.05
# 0.05 < 0.1 → MUTAÇÃO OCORRE

# 2. Seleção de índices
i, j = 3, 17
# chromosome[3] = 12
# chromosome[17] = 17

# 3. Estado antes da troca
mutant = [1, 5, 8, 12, 20, 2, 7, 15, 18, 23, 3, 6, 9, 14, 22,
          4, 10, 13, 17, 21, 11, 16, 19, 24, 25]
               ↑                          ↑
            idx 3                      idx 17

# 4. Após a troca
mutant = [1, 5, 8, 17, 20, 2, 7, 15, 18, 23, 3, 6, 9, 14, 22,
          4, 10, 13, 12, 21, 11, 16, 19, 24, 25]
               ↑                          ↑
            agora 17                   agora 12
```

**Impacto na Rota:**

```
Antes (decodificado):
V1: [1, 5, 8, 12, 20]   → Entrega 12 na posição 3 do V1
V4: [4, 10, 13, 17, 21] → Entrega 17 na posição 3 do V4

Depois:
V1: [1, 5, 8, 17, 20]   → Entrega 17 movida para V1
V4: [4, 10, 13, 12, 21] → Entrega 12 movida para V4

Resultado: Redistribuição entre veículos
```

#### Representação Matemática

Para um cromossomo $C = [c_1, c_2, ..., c_n]$:

$$\text{Swap}(C, i, j) = [c_1, ..., c_{i-1}, c_j, c_{i+1}, ..., c_{j-1}, c_i, c_{j+1}, ..., c_n]$$

Onde:
- $i, j \in \{1, 2, ..., n\}$ e $i \neq j$
- $c_i$ e $c_j$ trocam de posição

**Distância de Hamming:**
$$d_H(C, \text{Swap}(C)) = 2$$

Apenas 2 posições diferem entre o original e o mutante.

#### Propriedades

**Características:**
- ✅ **Preserva validade:** Não cria duplicatas ou omissões
- ✅ **Impacto local:** Altera apenas 2 posições
- ✅ **Simples e rápida:** O(1) complexidade de troca
- ✅ **Reversível:** Aplicar swap(i,j) duas vezes retorna ao original

**Adequação:**
- Ideal para **ajustes finos** em soluções já boas
- Útil em **fases finais** de convergência
- Eficaz para **roteamento** (TSP, VRP)

#### Vantagens e Desvantagens

**Vantagens:**
- ✅ Simplicidade de implementação
- ✅ Baixo custo computacional: O(n) total
- ✅ Não viola restrições de integridade
- ✅ Pequena perturbação: boa para convergência
- ✅ Mantém estrutura global da solução

**Desvantagens:**
- ❌ Mudança limitada: apenas 2 posições
- ❌ Pode não escapar de ótimos locais profundos
- ❌ Menos exploratória que outras técnicas
- ❌ Efeito pode ser mínimo se i e j estiverem próximos

**Complexidade:**
- **Tempo:** O(n) - criar cópia do cromossomo
- **Espaço:** O(n) - armazenar mutante
- **Troca:** O(1) - operação atômica

#### Casos de Uso Ideais

```python
# 1. População madura (gerações finais)
if generation > 0.7 * max_generations:
    mutate_with_swap(chromosome, prob=0.05)

# 2. Refinamento local
if fitness < threshold:
    mutate_with_swap(chromosome, prob=0.03)

# 3. Elites (pequenas mutações em melhores soluções)
if is_elite(individual):
    mutate_with_swap(chromosome, prob=0.02)
```

### 2. Relocate Mutation (Mutação por Realocação)

#### Conceito

Seleciona um gene aleatório, **remove-o** de sua posição original e **insere-o** em outra posição aleatória, alterando a sequência de múltiplos genes.

#### Algoritmo Detalhado

**Entrada:**
- `chromosome`: Lista de genes
- `prob`: Probabilidade de mutação (padrão: 0.1 = 10%)

**Processo:**

```
1. Verificar se a mutação ocorrerá
   if random.random() > prob:
       return chromosome_copy

2. Criar cópia do cromossomo
   mutant = chromosome[:]

3. Selecionar dois índices aleatórios
   i, j = random.sample(range(len(mutant)), 2)
   
   Exemplo: i=5, j=15

4. Remover gene da posição i
   gene = mutant.pop(i)  # Remove e retorna o gene
   
   mutant agora tem len-1 elementos

5. Inserir gene na posição j
   mutant.insert(j, gene)
   
   ATENÇÃO: Se j > i, posição efetiva é j-1 (devido ao pop)

6. Retornar mutante
   return mutant
```

**Saída:**
- Cromossomo com um gene realocado

#### Exemplo Detalhado

**Configuração:**
```python
# Cromossomo original
chromosome = [1, 5, 8, 12, 20, 2, 7, 15, 18, 23, 3, 6, 9, 14, 22,
              4, 10, 13, 17, 21, 11, 16, 19, 24, 25]
#             0  1  2   3   4  5  6   7   8   9 10 11 12 13  14
#            15 16  17  18  19 20  21  22  23  24

# Índices selecionados
i = 5   # gene = 2
j = 15  # posição destino
```

**Execução Passo a Passo:**

```python
# Estado inicial
mutant = [1, 5, 8, 12, 20, 2, 7, 15, 18, 23, 3, 6, 9, 14, 22,
          4, 10, 13, 17, 21, 11, 16, 19, 24, 25]
          0  1  2   3   4  5  6   7   8   9 10 11 12 13  14
                        ↑
                     idx=5, gene=2

# Após pop(5)
gene = 2
mutant = [1, 5, 8, 12, 20, 7, 15, 18, 23, 3, 6, 9, 14, 22, 4,
          10, 13, 17, 21, 11, 16, 19, 24, 25]
         0  1  2   3   4  5   6   7   8  9 10 11 12  13 14
                                                      ↑
                                               idx=15 (original)
# Agora len=24, então idx 15 original → idx 14 efetivo

# Após insert(15, 2)
mutant = [1, 5, 8, 12, 20, 7, 15, 18, 23, 3, 6, 9, 14, 22, 4,
          2, 10, 13, 17, 21, 11, 16, 19, 24, 25]
         0  1  2   3   4  5   6   7   8  9 10 11 12  13 14
                                                      ↑
                                               gene 2 inserido
```

**Impacto na Rota:**

```
Antes:
[1, 5, 8, 12, 20, 2, 7, 15, 18, 23, ...]
              ↑   └── gene 2 aqui

Depois:
[1, 5, 8, 12, 20, 7, 15, 18, 23, 3, 6, 9, 14, 22, 4, 2, ...]
                                                    ↑
                                            gene 2 movido para cá

Efeito: Múltiplos genes deslocados (7, 15, 18, ..., 4)
```

#### Representação Matemática

Para cromossomo $C = [c_1, c_2, ..., c_n]$ e índices $i < j$:

$$\text{Relocate}(C, i, j) = [c_1, ..., c_{i-1}, c_{i+1}, ..., c_j, c_i, c_{j+1}, ..., c_n]$$

Gene $c_i$ é removido e inserido após $c_j$.

**Distância de Hamming:**
$$d_H(C, \text{Relocate}(C)) = |j - i|$$

Maior impacto que Swap (que sempre é 2).

#### Propriedades

**Características:**
- ✅ **Impacto maior:** Desloca múltiplos genes
- ✅ **Reestruturação:** Altera ordem relativa de vários elementos
- ✅ **Exploratória:** Mais disruptiva que Swap
- ✅ **Mantém validade:** Sem duplicatas/omissões

**Adequação:**
- Ideal para **reordenação de rotas**
- Útil em **fases iniciais/intermediárias**
- Eficaz para **escape de ótimos locais**

#### Vantagens e Desvantagens

**Vantagens:**
- ✅ Maior poder exploratório que Swap
- ✅ Reordena sequências de entregas
- ✅ Pode mover entregas entre veículos diferentes
- ✅ Útil para otimização de sequenciamento
- ✅ Mantém integridade da solução

**Desvantagens:**
- ❌ Mais disruptiva (pode piorar boas soluções)
- ❌ Efeito difícil de prever
- ❌ Pode ser excessiva para refinamento fino
- ❌ Complexidade ligeiramente maior

**Complexidade:**
- **Tempo:** O(n) - pop e insert deslocam elementos
- **Espaço:** O(n) - cópia do cromossomo
- **Deslocamento:** O(|j - i|) elementos movidos

#### Casos de Uso Ideais

```python
# 1. Fase exploratória (gerações iniciais)
if generation < 0.3 * max_generations:
    mutate_with_relocate(chromosome, prob=0.15)

# 2. População estagnada
if diversity < threshold:
    mutate_with_relocate(chromosome, prob=0.20)

# 3. Busca de novos caminhos
if no_improvement_generations > 10:
    mutate_with_relocate(chromosome, prob=0.12)
```

### 3. Light Mutation (Mutação Leve Híbrida)

#### Conceito

Estratégia **híbrida** que escolhe **aleatoriamente** entre Swap e Relocate com probabilidades iguais (50/50), oferecendo balanceamento automático entre exploração e explotação.

#### Algoritmo Detalhado

**Entrada:**
- `chromosome`: Lista de genes
- `prob`: Probabilidade de mutação ocorrer (padrão: 0.15 = 15%)

**Processo:**

```
1. Verificar se a mutação ocorrerá
   if random.random() > prob:
       return chromosome_copy  # Sem mutação (85% dos casos)

2. Escolher estratégia aleatoriamente
   if random.random() < 0.5:
       # 50% de chance: Swap
       return swap_mutation(chromosome, prob=1.0)
   else:
       # 50% de chance: Relocate
       return relocate_mutation(chromosome, prob=1.0)
```

**Nota Importante:**
- Quando Light Mutation decide mutar, passa `prob=1.0` para as funções subjacentes
- Isso **garante** que a mutação escolhida sempre ocorrerá
- Evita duplo sorteio probabilístico

**Saída:**
- Cromossomo mutado por Swap ou Relocate

#### Modelo Probabilístico

$$P(\text{Mutação Light}) = 0.15$$

$$P(\text{Swap} | \text{Mutação Light}) = 0.5$$
$$P(\text{Relocate} | \text{Mutação Light}) = 0.5$$

**Probabilidades Efetivas:**
$$P(\text{Swap efetiva}) = 0.15 \times 0.5 = 0.075 = 7.5\%$$
$$P(\text{Relocate efetiva}) = 0.15 \times 0.5 = 0.075 = 7.5\%$$
$$P(\text{Sem mutação}) = 0.85 = 85\%$$

#### Exemplo de Execução

**Cenário 1: Mutação Não Ocorre**
```python
chromosome = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Sorteio inicial
random.random() = 0.92  # 0.92 > 0.15

# Resultado: SEM MUTAÇÃO
result = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  # Cópia inalterada
```

**Cenário 2: Mutação por Swap**
```python
chromosome = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Sorteio inicial
random.random() = 0.08  # 0.08 < 0.15 → MUTAÇÃO OCORRE

# Escolha de estratégia
random.random() = 0.35  # 0.35 < 0.5 → SWAP

# Swap com prob=1.0 (sempre executa)
i, j = 2, 7
result = [1, 2, 8, 4, 5, 6, 7, 3, 9, 10]
              ↑              ↑
           trocados
```

**Cenário 3: Mutação por Relocate**
```python
chromosome = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Sorteio inicial
random.random() = 0.12  # 0.12 < 0.15 → MUTAÇÃO OCORRE

# Escolha de estratégia
random.random() = 0.67  # 0.67 > 0.5 → RELOCATE

# Relocate com prob=1.0 (sempre executa)
i, j = 3, 8
gene = 4  # pop(3)
result = [1, 2, 3, 5, 6, 7, 8, 9, 4, 10]
                                ↑
                        gene 4 realocado
```

#### Justificativa da Estratégia Híbrida

**Problema:**
- Swap: Excelente para refinamento, mas limitado em exploração
- Relocate: Ótimo para exploração, mas pode ser excessivo

**Solução:**
- Light Mutation combina ambos automaticamente
- 50/50 garante balanceamento natural
- Evita necessidade de ajustar múltiplos parâmetros

**Benefícios:**

1. **Adaptação automática:** Alterna entre conservador e exploratório
2. **Simplicidade:** Um único parâmetro (`prob`)
3. **Robustez:** Funciona bem em diferentes fases da evolução
4. **Diversidade:** Maior variedade de mutações

#### Vantagens e Desvantagens

**Vantagens:**
- ✅ Balanceamento automático exploração/explotação
- ✅ Menor necessidade de tuning de parâmetros
- ✅ Adaptável a diferentes estágios da evolução
- ✅ Combina forças de ambas estratégias
- ✅ Probabilidade ligeiramente maior (15% vs 10%)

**Desvantagens:**
- ❌ Menos controle fino sobre tipo de mutação
- ❌ Comportamento menos previsível
- ❌ Pode não ser ideal em casos específicos
- ❌ Overhead de duas funções (mínimo)

**Complexidade:**
- **Tempo:** O(n) - dominado por Swap ou Relocate
- **Espaço:** O(n) - uma cópia
- **Overhead:** Desprezível (apenas um if adicional)

#### Casos de Uso Ideais

```python
# 1. Uso padrão (configuração recomendada)
def default_mutation(chromosome):
    return light_mutation(chromosome, prob=0.15)

# 2. População diversa (qualquer fase)
mutated = light_mutation(chromosome, prob=0.15)

# 3. Quando não se sabe qual estratégia priorizar
if uncertain_phase:
    use_light_mutation()
```

## Comparação Entre Técnicas

### Tabela Resumida

| Aspecto | Swap | Relocate | Light |
|---------|------|----------|-------|
| **Impacto** | Baixo (2 posições) | Médio (múltiplas) | Variável |
| **Exploração** | Baixa | Alta | Média |
| **Complexidade** | O(n) | O(n) | O(n) |
| **Prob. Padrão** | 10% | 10% | 15% |
| **Fase ideal** | Final | Inicial | Todas |
| **Previsibilidade** | Alta | Média | Baixa |
| **Diversidade** | Baixa | Alta | Média-Alta |

### Comparação Visual de Impacto

```
Original:     [A, B, C, D, E, F, G, H, I]

Swap(2,6):    [A, B, G, D, E, F, C, H, I]
                     ↑           ↑
                  Apenas 2 mudanças

Relocate(2,6):[A, B, D, E, F, G, C, H, I]
                     ↑ ↑ ↑ ↑ ↑
                  Múltiplas mudanças

Light:         50% Swap ou 50% Relocate
```

### Hamming Distance Esperada

$$E[d_H(\text{Swap})] = 2$$
$$E[d_H(\text{Relocate})] \approx \frac{n}{3}$$ (em média)
$$E[d_H(\text{Light})] \approx 0.5 \times 2 + 0.5 \times \frac{n}{3}$$

Para n=25:
- Swap: ~2 posições alteradas
- Relocate: ~8 posições alteradas
- Light: ~5 posições alteradas (média)

## Configuração de Probabilidades

### Taxa de Mutação Ótima

**Regra Geral:** 
$$p_{mut} = \frac{1}{n}$$

Onde $n$ é o tamanho do cromossomo.

**Para 25 entregas:**
$$p_{mut} = \frac{1}{25} = 0.04 = 4\%$$

**Valores Implementados:**
- Swap: 10% (2.5× regra geral) → Mais conservador
- Relocate: 10% (2.5× regra geral) → Mais conservador
- Light: 15% (3.75× regra geral) → Balanceado

### Estratégia Adaptativa

```python
def adaptive_mutation_rate(generation, max_gen, base_rate=0.1):
    """
    Ajusta taxa de mutação ao longo das gerações
    
    Início: Alta exploração
    Meio: Balanceado
    Final: Baixa exploração (refinamento)
    """
    progress = generation / max_gen
    
    if progress < 0.3:
        # Fase exploratória
        return base_rate * 1.5  # 15%
    elif progress < 0.7:
        # Fase intermediária
        return base_rate  # 10%
    else:
        # Fase de refinamento
        return base_rate * 0.5  # 5%
```

### Mutação por Elitismo

```python
def mutate_with_elitism(population, elite_size=2):
    """
    Elite não sofre mutação
    Restante sofre mutação normal
    """
    # Ordenar por fitness
    sorted_pop = sorted(population, key=fitness)
    
    # Elite preservada
    elite = sorted_pop[:elite_size]
    
    # Restante com mutação
    mutated = []
    for individual in sorted_pop[elite_size:]:
        mutant = light_mutation(individual, prob=0.15)
        mutated.append(mutant)
    
    return elite + mutated
```

## Integração com Algoritmo Genético

### Fluxo Completo

```
População Geração N
    ↓
Seleção (f_selection.py)
    ↓
Crossover (d_crossover.py)
    ↓
Mutação (e_mutation.py) ← AQUI
    ↓
Avaliação (c_fitness.py)
    ↓
População Geração N+1
```

### Pseudocódigo de Integração

```python
def genetic_algorithm_step(population):
    new_population = []
    
    # Para cada par de pais
    for i in range(0, len(population), 2):
        # Seleção
        parent1, parent2 = select_parents(population)
        
        # Crossover
        child1 = crossover(parent1, parent2)
        child2 = crossover(parent2, parent1)
        
        # Mutação
        child1 = light_mutation(child1, prob=0.15)
        child2 = light_mutation(child2, prob=0.15)
        
        new_population.extend([child1, child2])
    
    return new_population
```

### Exemplo Completo

```python
from e_mutation import light_mutation, swap_mutation, relocate_mutation
from c_fitness import calculate_fitness

# Cromossomo original
chromosome = [1, 5, 8, 12, 20, 2, 7, 15, 18, 23, 3, 6, 9, 14, 22,
              4, 10, 13, 17, 21, 11, 16, 19, 24, 25]

# Fitness original
fitness_original = calculate_fitness(chromosome, "SP")
print(f"Fitness original: {fitness_original:.2f}")

# Aplicar mutações
mutant_swap = swap_mutation(chromosome, prob=1.0)
mutant_relocate = relocate_mutation(chromosome, prob=1.0)
mutant_light = light_mutation(chromosome, prob=1.0)

# Avaliar mutantes
fitness_swap = calculate_fitness(mutant_swap, "SP")
fitness_relocate = calculate_fitness(mutant_relocate, "SP")
fitness_light = calculate_fitness(mutant_light, "SP")

print(f"\nFitness Swap: {fitness_swap:.2f}")
print(f"Fitness Relocate: {fitness_relocate:.2f}")
print(f"Fitness Light: {fitness_light:.2f}")

# Análise
if fitness_swap < fitness_original:
    print("✓ Swap melhorou a solução")
if fitness_relocate < fitness_original:
    print("✓ Relocate melhorou a solução")
if fitness_light < fitness_original:
    print("✓ Light melhorou a solução")
```

## Análise de Eficácia

### Métricas de Avaliação

#### 1. Taxa de Melhoria

```python
def improvement_rate(original_fitness, mutant_fitness):
    """Percentual de melhoria após mutação"""
    if mutant_fitness < original_fitness:
        improvement = (original_fitness - mutant_fitness) / original_fitness
        return improvement * 100
    else:
        return 0  # Sem melhoria
```

#### 2. Diversidade Populacional

```python
def population_diversity(population):
    """
    Mede diversidade usando distância Hamming média
    entre todos os pares de indivíduos
    """
    n = len(population)
    total_distance = 0
    comparisons = 0
    
    for i in range(n):
        for j in range(i+1, n):
            distance = hamming_distance(population[i], population[j])
            total_distance += distance
            comparisons += 1
    
    return total_distance / comparisons if comparisons > 0 else 0

def hamming_distance(chrom1, chrom2):
    """Número de posições diferentes"""
    return sum(1 for a, b in zip(chrom1, chrom2) if a != b)
```

#### 3. Taxa de Aceitação

```python
def acceptance_rate(mutants, originals, fitness_func):
    """
    Percentual de mutantes aceitos (fitness melhor ou igual)
    """
    accepted = 0
    
    for mutant, original in zip(mutants, originals):
        if fitness_func(mutant) <= fitness_func(original):
            accepted += 1
    
    return (accepted / len(mutants)) * 100
```

### Benchmarking

```python
import time
import statistics

def benchmark_mutations(chromosome, n_tests=1000):
    """
    Compara desempenho e eficácia das técnicas
    """
    results = {
        'swap': {'times': [], 'improvements': []},
        'relocate': {'times': [], 'improvements': []},
        'light': {'times': [], 'improvements': []}
    }
    
    original_fitness = calculate_fitness(chromosome, "SP")
    
    for _ in range(n_tests):
        # Swap
        start = time.time()
        mutant = swap_mutation(chromosome, prob=1.0)
        results['swap']['times'].append(time.time() - start)
        fitness = calculate_fitness(mutant, "SP")
        improvement = (original_fitness - fitness) / original_fitness * 100
        results['swap']['improvements'].append(improvement)
        
        # Relocate
        start = time.time()
        mutant = relocate_mutation(chromosome, prob=1.0)
        results['relocate']['times'].append(time.time() - start)
        fitness = calculate_fitness(mutant, "SP")
        improvement = (original_fitness - fitness) / original_fitness * 100
        results['relocate']['improvements'].append(improvement)
        
        # Light
        start = time.time()
        mutant = light_mutation(chromosome, prob=1.0)
        results['light']['times'].append(time.time() - start)
        fitness = calculate_fitness(mutant, "SP")
        improvement = (original_fitness - fitness) / original_fitness * 100
        results['light']['improvements'].append(improvement)
    
    # Estatísticas
    for method in results:
        times = results[method]['times']
        improvements = results[method]['improvements']
        
        print(f"\n{method.upper()}:")
        print(f"  Tempo médio: {statistics.mean(times)*1000:.3f} ms")
        print(f"  Melhoria média: {statistics.mean(improvements):.2f}%")
        print(f"  Taxa de melhoria: {sum(1 for i in improvements if i > 0)/n_tests*100:.1f}%")
```

## Justificativas das Escolhas

### Por Que Swap Mutation?

**Justificativa:**
1. **Simplicidade:** Implementação direta e eficiente
2. **Localidade:** Mudanças pequenas ideais para convergência
3. **Estabilidade:** Não desestabiliza soluções boas
4. **Tradição:** Técnica amplamente validada na literatura

**Referências:**
- Davis (1991): Handbook of Genetic Algorithms
- Goldberg (1989): Demonstra eficácia em TSP

### Por Que Relocate Mutation?

**Justificativa:**
1. **Exploração:** Maior capacidade de reestruturação
2. **Escape:** Eficaz para sair de ótimos locais
3. **Sequenciamento:** Adequada para problemas de ordem (VRP)
4. **Complementaridade:** Balanceia a limitação do Swap

**Referências:**
- Potvin (1996): "A hybrid genetic algorithm for the vehicle routing problem"
- Oliver et al. (1987): Mutation em permutações

### Por Que Light Mutation (Híbrida)?

**Justificativa:**
1. **Robustez:** Funciona bem sem tuning fino
2. **Versatilidade:** Adequada para todas as fases
3. **Simplicidade de uso:** Um único parâmetro
4. **Balanceamento:** Combina conservadorismo e exploração

**Vantagem Competitiva:**
```
Abordagem tradicional: Escolher Swap OU Relocate
    → Difícil saber qual é melhor
    → Necessita experimentação

Light Mutation: Usa AMBOS automaticamente
    → Melhor dos dois mundos
    → Adaptação automática
```

## Melhorias Possíveis

### 1. Inversion Mutation

```python
def inversion_mutation(chromosome, prob=0.1):
    """
    Inverte ordem de uma subsequência
    
    [1, 2, 3, 4, 5, 6, 7, 8] 
           └─────┘
    [1, 2, 6, 5, 4, 3, 7, 8]
    """
    if random.random() > prob:
        return chromosome[:]
    
    i, j = sorted(random.sample(range(len(chromosome)), 2))
    mutant = chromosome[:]
    mutant[i:j+1] = reversed(mutant[i:j+1])
    
    return mutant
```

### 2. Scramble Mutation

```python
def scramble_mutation(chromosome, prob=0.1):
    """
    Embaralha aleatoriamente uma subsequência
    
    [1, 2, 3, 4, 5, 6, 7, 8]
           └─────┘
    [1, 2, 5, 3, 6, 4, 7, 8]
    """
    if random.random() > prob:
        return chromosome[:]
    
    i, j = sorted(random.sample(range(len(chromosome)), 2))
    mutant = chromosome[:]
    subset = mutant[i:j+1]
    random.shuffle(subset)
    mutant[i:j+1] = subset
    
    return mutant
```

### 3. Adaptive Mutation

```python
def adaptive_mutation(chromosome, fitness, avg_fitness, prob_base=0.1):
    """
    Ajusta probabilidade baseado em qualidade da solução
    
    Solução ruim → maior probabilidade (exploração)
    Solução boa → menor probabilidade (explotação)
    """
    if fitness > avg_fitness:
        # Solução abaixo da média → aumentar mutação
        prob = min(prob_base * 2.0, 0.3)
    else:
        # Solução acima da média → reduzir mutação
        prob = max(prob_base * 0.5, 0.01)
    
    return light_mutation(chromosome, prob)
```

### 4. Guided Mutation (Orientada por Fitness)

```python
def guided_mutation(chromosome, deliveries, prob=0.1):
    """
    Mutação que tenta melhorar proximidade geográfica
    
    Troca genes que reduziriam distância se estivessem próximos
    """
    if random.random() > prob:
        return chromosome[:]
    
    # Encontrar par com maior distância
    max_dist = 0
    best_pair = (0, 1)
    
    for i in range(len(chromosome) - 1):
        d1 = chromosome[i]
        d2 = chromosome[i + 1]
        dist = manhattan(
            (deliveries[d1]["lat"], deliveries[d1]["lon"]),
            (deliveries[d2]["lat"], deliveries[d2]["lon"])
        )
        if dist > max_dist:
            max_dist = dist
            best_pair = (i, i + 1)
    
    # Swap ou relocate neste par
    if random.random() < 0.5:
        return swap_mutation_at(chromosome, best_pair[0], best_pair[1])
    else:
        return relocate_mutation_at(chromosome, best_pair[0], best_pair[1])
```

## Palavras-chave para Busca

- Mutação genética
- Operadores de mutação
- Swap mutation
- Relocate mutation
- Light mutation híbrida
- Diversidade populacional
- Taxa de mutação
- Exploração vs explotação
- Distância Hamming
- Mutação adaptativa
- Permutação cromossômica
- Variabilidade genética
- Ótimos locais
- Convergência prematura
- Inversion mutation
- Scramble mutation
- Guided mutation
- Algoritmo genético VRP
- TSP mutation
- Probabilidade de mutação

## Referências Técnicas

### Complexidade Computacional
- **Swap:** O(n) tempo, O(n) espaço
- **Relocate:** O(n) tempo, O(n) espaço
- **Light:** O(n) tempo, O(n) espaço

### Notação Matemática
- $C$: Cromossomo (chromosome)
- $p_{mut}$: Probabilidade de mutação
- $d_H$: Distância de Hamming
- $i, j$: Índices de mutação
- $n$: Tamanho do cromossomo

### Fórmulas Importantes

**Taxa de mutação ideal:**
$$p_{mut} \approx \frac{1}{n}$$

**Probabilidade efetiva Light:**
$$P(\text{Mutação efetiva}) = p_{light} \times 0.5$$

**Diversidade esperada:**
$$D = E[d_H] = p_{mut} \times E[\text{genes alterados}]$$

### Bibliografia
- Goldberg, D. E. (1989). *Genetic Algorithms in Search, Optimization and Machine Learning*
- Davis, L. (1991). *Handbook of Genetic Algorithms*
- Eiben, A. E., & Smith, J. E. (2015). *Introduction to Evolutionary Computing*
- Michalewicz, Z. (1996). *Genetic Algorithms + Data Structures = Evolution Programs*

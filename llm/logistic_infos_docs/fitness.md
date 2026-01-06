# Módulo de Função de Fitness - Algoritmo Genético para Otimização Logística

## Visão Geral

O módulo `c_fitness.py` implementa a função de fitness do algoritmo genético, responsável por avaliar a qualidade de cada solução candidata. Esta função multiobjetivo pondera diversos critérios logísticos, transformando restrições operacionais e objetivos de negócio em um único valor numérico que guia o processo evolutivo.

## Objetivo

Avaliar soluções de roteamento de veículos considerando múltiplos fatores: custos operacionais, restrições físicas dos veículos (capacidade e autonomia), prioridades de entrega, e eficiência das rotas. A função retorna um valor de fitness onde **valores menores indicam soluções melhores** (problema de minimização).

## Modelo Matemático Completo

### Função de Fitness (Variável Dependente)

A função de fitness total é definida como:

$$F_{total} = C_{viagem} + P_{total}$$

Onde:
- $F_{total}$: Fitness total da solução (variável dependente)
- $C_{viagem}$: Custo total de viagem (componente de custo)
- $P_{total}$: Soma de todas as penalidades (componente de restrições)

### Decomposição Detalhada

Para uma solução com $V$ veículos e rotas $R_v$ (conjunto de entregas do veículo $v$):

$$F_{total} = \sum_{v=1}^{V} \left[ d_v \cdot c_v + P_{cap}(v) + P_{aut}(v) + P_{efic}(v) + P_{prior}(v) \right]$$

Onde:
- $d_v$: Distância Manhattan da rota do veículo $v$
- $c_v$: Custo por unidade de distância do veículo $v$
- $P_{cap}(v)$: Penalidade por excesso de capacidade
- $P_{aut}(v)$: Penalidade por excesso de autonomia
- $P_{efic}(v)$: Penalidade por ineficiência de rota
- $P_{prior}(v)$: Penalidades acumuladas de prioridade

## Variáveis Independentes (Hiperparâmetros)

### 1. CAPACITY_PENALTY = 100 (Peso da Penalidade de Capacidade)

**Tipo:** Restrição suave (soft constraint)

**Função Matemática:**
$$P_{cap}(v) = \begin{cases} 
W_{cap} \cdot (L_v - K_v) & \text{se } L_v > K_v \\
0 & \text{caso contrário}
\end{cases}$$

Onde:
- $W_{cap} = 100$ (CAPACITY_PENALTY)
- $L_v$: Carga atual do veículo $v$ (soma das demandas)
- $K_v$: Capacidade máxima do veículo $v$

**Significado:**
- Penaliza soluções onde veículos carregam mais do que sua capacidade
- Valor de 100 indica restrição "suave" - permite pequenas violações com custo moderado
- Cada unidade de excesso adiciona 100 pontos ao fitness

**Exemplo:**
```python
# Veículo V1: capacidade = 100kg, carga = 110kg
excesso = 110 - 100 = 10kg
penalidade = 100 * 10 = 1000 pontos
```

**Impacto na Otimização:**
- Valor menor (< 100): Algoritmo tolera mais violações de capacidade
- Valor maior (> 100): Força distribuição mais rígida de entregas
- Valor atual (100): Balanceamento entre flexibilidade e restrição

### 2. AUTONOMY_PENALTY = 200 (Peso da Penalidade de Autonomia)

**Tipo:** Restrição rígida (hard constraint)

**Função Matemática:**
$$P_{aut}(v) = \begin{cases} 
W_{aut} \cdot (d_v - A_v) & \text{se } d_v > A_v \\
0 & \text{caso contrário}
\end{cases}$$

Onde:
- $W_{aut} = 200$ (AUTONOMY_PENALTY)
- $d_v$: Distância total da rota do veículo $v$
- $A_v$: Autonomia máxima do veículo $v$ (em unidades Manhattan)

**Significado:**
- **Penalidade mais severa** (200 vs 100 da capacidade)
- Representa restrição crítica de segurança: veículo não pode ficar sem combustível
- Violações de autonomia são inaceitáveis na prática

**Exemplo:**
```python
# Veículo V1: autonomia = 50km, distância rota = 55km
excesso = 55 - 50 = 5km
penalidade = 200 * 5 = 1000 pontos
```

**Justificativa do Valor Alto:**
- Autonomia é restrição operacional crítica
- Falha pode resultar em entregas não realizadas
- Custos reais: reboque, perda de tempo, insatisfação do cliente

### 3. CRITICAL_WEIGHT = 12 (Peso Linear de Prioridade Crítica)

**Tipo:** Incentivo de priorização

**Função Matemática (Componente Linear):**
$$P_{crit\_lin}(i, v) = W_{crit} \cdot i + W_{crit\_pos} \cdot p$$

Onde:
- $W_{crit} = 12$ (CRITICAL_WEIGHT)
- $i$: Índice da rota (ordem do veículo no processamento, 0-based)
- $p$: Posição da entrega na rota do veículo
- $W_{crit\_pos} = 1.5$ (CRITICAL_POS_WEIGHT)

**Significado:**
- Incentiva entregas críticas (prioridade 3) em rotas iniciais
- Quanto maior o índice da rota, maior a penalidade
- Peso 12 = alto custo para atrasar entregas críticas

**Exemplo:**
```python
# Entrega crítica na Rota 2 (índice 1), Posição 3
penalidade_linear = 12 * 1 + 1.5 * 3 = 12 + 4.5 = 16.5 pontos

# Mesma entrega na Rota 1 (índice 0), Posição 0
penalidade_linear = 12 * 0 + 1.5 * 0 = 0 pontos
```

**Impacto Comparativo:**
```
Rota 0 (primeira): 0 pontos por entrega crítica
Rota 1: 12 pontos por entrega crítica
Rota 2: 24 pontos por entrega crítica
Rota 3: 36 pontos por entrega crítica
Rota 4: 48 pontos por entrega crítica
```

### 4. HIGH_PRIORITY_WEIGHT = 3 (Peso Linear de Alta Prioridade)

**Tipo:** Incentivo moderado de priorização

**Função Matemática:**
$$P_{high}(i, v) = W_{high} \cdot i + W_{high\_pos} \cdot p$$

Onde:
- $W_{high} = 3$ (HIGH_PRIORITY_WEIGHT)
- $W_{high\_pos} = 0.6$ (HIGH_PRIORITY_POS_WEIGHT)

**Significado:**
- Penalidade 4x menor que entregas críticas (3 vs 12)
- Incentiva priorização, mas com menor urgência
- Permite mais flexibilidade no agendamento

**Exemplo:**
```python
# Entrega de alta prioridade na Rota 3 (índice 2), Posição 2
penalidade = 3 * 2 + 0.6 * 2 = 6 + 1.2 = 7.2 pontos

# Entrega crítica na mesma posição
penalidade_crítica = 12 * 2 + 1.5 * 2 = 24 + 3 = 27 pontos
```

**Hierarquia de Prioridades:**
- Prioridade 3 (Crítica): Peso 12 (máxima urgência)
- Prioridade 2 (Alta): Peso 3 (moderada urgência)
- Prioridade 1 (Normal): Peso 0 (sem penalidade especial)

### 5. CRITICAL_POS_WEIGHT = 1.5 (Peso de Posição para Entrega Crítica)

**Tipo:** Refinamento de priorização

**Função Matemática:**
$$P_{crit\_pos} = W_{crit\_pos} \cdot p$$

Onde:
- $W_{crit\_pos} = 1.5$ (CRITICAL_POS_WEIGHT)
- $p$: Posição da entrega na rota (0 = primeira, 1 = segunda, etc.)

**Significado:**
- Incentiva entregas críticas no **início** da rota do veículo
- Última posição (posição 4) adiciona 6 pontos (1.5 × 4)
- Combina com CRITICAL_WEIGHT para priorização dupla

**Lógica Operacional:**
```
Posição 0 (primeira): +0 pontos
Posição 1 (segunda): +1.5 pontos
Posição 2 (terceira): +3.0 pontos
Posição 3 (quarta): +4.5 pontos
Posição 4 (última): +6.0 pontos
```

**Exemplo Prático:**
```python
# Cenário: Entrega crítica no Veículo V3 (índice 2)

# Na primeira posição da rota
penalidade = 12 * 2 + 1.5 * 0 = 24 pontos

# Na última posição da rota
penalidade = 12 * 2 + 1.5 * 4 = 30 pontos

# Diferença: 6 pontos de penalidade por estar no final
```

### 6. HIGH_PRIORITY_POS_WEIGHT = 0.6 (Peso de Posição para Alta Prioridade)

**Tipo:** Refinamento moderado de priorização

**Função Matemática:**
$$P_{high\_pos} = W_{high\_pos} \cdot p$$

Onde:
- $W_{high\_pos} = 0.6$ (HIGH_PRIORITY_POS_WEIGHT)
- Proporcional a 40% do peso crítico (0.6/1.5 = 0.4)

**Significado:**
- Incentivo menor que entregas críticas
- Última posição adiciona 2.4 pontos (0.6 × 4)
- Permite mais flexibilidade na sequência de entrega

**Comparação de Impacto:**
```
                    Posição 0   Posição 4   Diferença
Crítica:            +0          +6.0        6.0 pontos
Alta Prioridade:    +0          +2.4        2.4 pontos
Proporção:          -           2.5x        -
```

### 7. COST_EFFICIENCY_THRESHOLD = 5.0 (Limite de Custo por Entrega)

**Tipo:** Métrica de eficiência operacional

**Função Matemática:**
$$\text{Custo/Entrega} = \frac{C_{viagem}(v)}{|R_v|}$$

Onde:
- $C_{viagem}(v) = d_v \cdot c_v$ (custo total da rota)
- $|R_v|$: Número de entregas na rota

**Significado:**
- Define o custo aceitável por entrega: 5.0 unidades
- Penaliza rotas com poucos pontos de entrega (ineficientes)
- Incentiva consolidação de entregas

**Exemplo:**
```python
# Rota A: 30km, custo 3/km, 10 entregas
custo_total = 30 * 3 = 90
custo_por_entrega = 90 / 10 = 9.0
excesso = 9.0 - 5.0 = 4.0 (ineficiente)

# Rota B: 30km, custo 3/km, 15 entregas
custo_total = 30 * 3 = 90
custo_por_entrega = 90 / 15 = 6.0
excesso = 6.0 - 5.0 = 1.0 (mais eficiente)
```

**Impacto Estratégico:**
- Incentiva rotas densas (muitas entregas próximas)
- Penaliza rotas longas com poucas entregas
- Alinha com objetivo de maximizar entregas por km rodado

### 8. COST_EFFICIENCY_WEIGHT = 5 (Peso da Penalidade de Eficiência)

**Tipo:** Multiplicador de penalidade de eficiência

**Função Matemática:**
$$P_{efic}(v) = \begin{cases}
W_{efic} \cdot (\frac{C_{viagem}(v)}{|R_v|} - T_{efic}) & \text{se } \frac{C_{viagem}(v)}{|R_v|} > T_{efic} \\
0 & \text{caso contrário}
\end{cases}$$

Onde:
- $W_{efic} = 5$ (COST_EFFICIENCY_WEIGHT)
- $T_{efic} = 5.0$ (COST_EFFICIENCY_THRESHOLD)

**Significado:**
- Cada unidade de ineficiência adiciona 5 pontos ao fitness
- Peso moderado (5) - balanceado entre priorização e restrições físicas
- Incentivo econômico sem ser proibitivo

**Exemplo Completo:**
```python
# Veículo: custo 2.5/km
# Rota: 40km, 3 entregas

custo_total = 40 * 2.5 = 100
custo_por_entrega = 100 / 3 = 33.33
ineficiência = 33.33 - 5.0 = 28.33
penalidade = 5 * 28.33 = 141.65 pontos

# Interpretação: Rota muito ineficiente (poucas entregas dispersas)
```

**Cenários de Aplicação:**
```
Custo/Entrega    Status          Penalidade
≤ 5.0            Eficiente       0
6.0              Aceitável       5 pontos
10.0             Ineficiente     25 pontos
20.0             Muito inef.     75 pontos
```

## Componentes Calculados (Variáveis Intermediárias)

### 1. Carga do Veículo ($L_v$)

**Cálculo:**
$$L_v = \sum_{d \in R_v} \text{demand}_d$$

Onde:
- $R_v$: Conjunto de entregas atribuídas ao veículo $v$
- $\text{demand}_d$: Demanda (peso/volume) da entrega $d$

**Código:**
```python
load = sum(deliveries[d]["demand"] for d in route)
```

### 2. Distância Manhattan da Rota ($d_v$)

**Cálculo:**
$$d_v = d(C, P_1) + \sum_{i=1}^{n-1} d(P_i, P_{i+1}) + d(P_n, C)$$

Onde:
- $C$: Centro de distribuição
- $P_i$: Ponto de entrega $i$ na rota
- $d(A, B)$: Distância Manhattan entre pontos $A$ e $B$

**Código:**
```python
dist_M = route_distance(list_coords, center_coords=get_center_coordinates(city))
```

**Referência:** Ver [manhattan_distance.md](manhattan_distance.md) para detalhes

### 3. Custo de Viagem ($C_{viagem}(v)$)

**Cálculo:**
$$C_{viagem}(v) = d_v \cdot c_v$$

Onde:
- $d_v$: Distância total da rota (Manhattan)
- $c_v$: Custo operacional por unidade de distância do veículo

**Código:**
```python
travel_cost = dist_M * vehicle["cost_M"]
```

**Exemplo:**
```python
# Veículo elétrico: R$ 0.50/km
# Rota: 80km
custo = 80 * 0.50 = R$ 40.00
```

### 4. Penalidade Quadrática de Prioridade Crítica

**Função Matemática:**
$$P_{crit\_quad}(i) = \alpha \cdot i^2$$

Onde:
- $\alpha = 2.0$ (fator de crescimento quadrático)
- $i$: Índice da rota

**Código:**
```python
quadratic_penalty = (route_index ** 2) * 2.0
```

**Crescimento da Penalidade:**
```
Rota 0: 2.0 * 0² = 0
Rota 1: 2.0 * 1² = 2
Rota 2: 2.0 * 2² = 8
Rota 3: 2.0 * 3² = 18
Rota 4: 2.0 * 4² = 32
```

**Significado:**
- Crescimento **exponencial** das penalidades
- Rotas tardias sofrem penalização desproporcional
- Força entregas críticas nas primeiras rotas

### 5. Penalidade Total por Prioridade Crítica

**Modelo Híbrido (Linear + Quadrático):**
$$P_{crit\_total} = (W_{crit} \cdot i + W_{crit\_pos} \cdot p) + (\alpha \cdot i^2)$$

**Exemplo Detalhado:**
```python
# Entrega crítica na Rota 3 (índice 2), Posição 4

# Componente linear
linear = 12 * 2 + 1.5 * 4 = 24 + 6 = 30

# Componente quadrático
quadratico = 2.0 * 2² = 8

# Total
total = 30 + 8 = 38 pontos
```

**Comparação por Rota:**
```
Rota  Linear  Quadrático  Total
0     0       0           0
1     12      2           14
2     24      8           32
3     36      18          54
4     48      32          80
```

## Fluxo de Execução da Função

### Pseudocódigo Estruturado

```
FUNÇÃO calculate_fitness(solução, cidade):
    total_cost ← 0
    penalty ← 0
    
    PARA CADA (veículo, rota) EM solução:
        # 1. Verificar capacidade
        carga ← SOMAR demandas das entregas
        SE carga > capacidade_veículo:
            penalty ← penalty + CAPACITY_PENALTY × (carga - capacidade)
        
        # 2. Calcular distância
        coordenadas ← OBTER coordenadas das entregas
        distância ← route_distance(coordenadas, centro)
        
        # 3. Verificar autonomia
        SE distância > autonomia_veículo:
            penalty ← penalty + AUTONOMY_PENALTY × (distância - autonomia)
        
        # 4. Calcular custo de viagem
        custo_viagem ← distância × custo_por_km_veículo
        total_cost ← total_cost + custo_viagem
        
        # 5. Penalidade de eficiência
        SE número_entregas > 0:
            custo_por_entrega ← custo_viagem / número_entregas
            SE custo_por_entrega > THRESHOLD:
                ineficiência ← custo_por_entrega - THRESHOLD
                penalty ← penalty + ineficiência × COST_EFFICIENCY_WEIGHT
        
        # 6. Penalidades de prioridade
        PARA CADA (posição, entrega) EM rota:
            prioridade ← OBTER prioridade da entrega
            
            SE prioridade = 3 (crítica):
                # Linear
                penalty ← penalty + índice_rota × CRITICAL_WEIGHT
                penalty ← penalty + posição × CRITICAL_POS_WEIGHT
                
                # Quadrático
                penalty ← penalty + (índice_rota²) × 2.0
            
            SENÃO SE prioridade = 2 (alta):
                penalty ← penalty + índice_rota × HIGH_PRIORITY_WEIGHT
                penalty ← penalty + posição × HIGH_PRIORITY_POS_WEIGHT
    
    RETORNAR total_cost + penalty
```

## Exemplo Completo de Cálculo

### Cenário: Solução com 2 Veículos

**Dados de Entrada:**

**Veículo V1 (elétrico):**
- Capacidade: 100kg
- Autonomia: 80km
- Custo: R$ 0.50/km

**Rota V1:** 3 entregas
- Entrega E1: demanda 30kg, prioridade 3 (crítica), posição 0
- Entrega E2: demanda 25kg, prioridade 2 (alta), posição 1
- Entrega E3: demanda 40kg, prioridade 1 (normal), posição 2
- Distância total: 60km

**Veículo V2 (combustão):**
- Capacidade: 150kg
- Autonomia: 120km
- Custo: R$ 1.20/km

**Rota V2:** 2 entregas
- Entrega E4: demanda 80kg, prioridade 2 (alta), posição 0
- Entrega E5: demanda 90kg, prioridade 1 (normal), posição 1
- Distância total: 100km

### Cálculo Detalhado - V1 (Rota 0)

```python
# 1. Capacidade
carga = 30 + 25 + 40 = 95kg
95 ≤ 100: OK, penalidade = 0

# 2. Distância
dist_M = 60km (calculado via Manhattan)

# 3. Autonomia
60 ≤ 80: OK, penalidade = 0

# 4. Custo de viagem
custo_viagem = 60 * 0.50 = R$ 30.00

# 5. Eficiência
custo_por_entrega = 30 / 3 = 10.0
ineficiência = 10.0 - 5.0 = 5.0
penalidade_efic = 5.0 * 5 = 25.0

# 6. Prioridades (route_index = 0)

## E1 (crítica, posição 0)
linear = 12 * 0 + 1.5 * 0 = 0
quadratico = 2.0 * 0² = 0
total_E1 = 0

## E2 (alta, posição 1)
penalidade_E2 = 3 * 0 + 0.6 * 1 = 0.6

## E3 (normal, posição 2)
penalidade_E3 = 0

# TOTAL V1
total_cost_V1 = 30.00
penalty_V1 = 0 + 0 + 25.0 + 0 + 0.6 + 0 = 25.6
```

### Cálculo Detalhado - V2 (Rota 1)

```python
# 1. Capacidade
carga = 80 + 90 = 170kg
170 > 150: VIOLAÇÃO
penalidade_cap = 100 * (170 - 150) = 2000

# 2. Distância
dist_M = 100km

# 3. Autonomia
100 ≤ 120: OK, penalidade = 0

# 4. Custo de viagem
custo_viagem = 100 * 1.20 = R$ 120.00

# 5. Eficiência
custo_por_entrega = 120 / 2 = 60.0
ineficiência = 60.0 - 5.0 = 55.0
penalidade_efic = 55.0 * 5 = 275.0

# 6. Prioridades (route_index = 1)

## E4 (alta, posição 0)
penalidade_E4 = 3 * 1 + 0.6 * 0 = 3.0

## E5 (normal, posição 1)
penalidade_E5 = 0

# TOTAL V2
total_cost_V2 = 120.00
penalty_V2 = 2000 + 0 + 275.0 + 3.0 + 0 = 2278.0
```

### Fitness Total da Solução

```python
total_cost = 30.00 + 120.00 = 150.00
penalty = 25.6 + 2278.0 = 2303.6

FITNESS = 150.00 + 2303.6 = 2453.6
```

**Análise:**
- Solução inviável (excesso de capacidade em V2)
- Alta ineficiência (poucos pontos de entrega)
- Penalidades dominam o fitness
- Necessita otimização via operadores genéticos

## Interpretação e Otimização

### Objetivos Conflitantes

A função de fitness equilibra múltiplos objetivos:

1. **Minimizar custo** ↔ **Respeitar restrições**
2. **Eficiência de rota** ↔ **Priorização de entregas**
3. **Consolidar entregas** ↔ **Limites de capacidade**

### Estratégias de Melhoria

**Para reduzir fitness:**

1. **Redistribuir cargas** entre veículos (evitar violações de capacidade)
2. **Otimizar sequência** de entregas (reduzir distância)
3. **Priorizar entregas críticas** em rotas iniciais
4. **Consolidar entregas** em regiões próximas (aumentar eficiência)
5. **Selecionar veículos adequados** (custo vs capacidade vs autonomia)

### Sensibilidade dos Parâmetros

**Impacto no comportamento do algoritmo:**

```
Parâmetro              Impacto se ↑        Impacto se ↓
─────────────────────────────────────────────────────────
CAPACITY_PENALTY       Força distribuição  Tolera sobrecarga
AUTONOMY_PENALTY       Rotas mais curtas   Permite rotas longas
CRITICAL_WEIGHT        Prioriza críticas   Mais flexibilidade
COST_EFFICIENCY_W      Rotas densas        Aceita dispersão
```

## Integração com Algoritmo Genético

### Papel na Evolução

```
Geração 0: População aleatória → Avaliação fitness
    ↓
Seleção: Melhores fitness (menores valores)
    ↓
Crossover: Combina soluções promissoras
    ↓
Mutação: Introduz variação
    ↓
Geração 1: Nova população → Avaliação fitness
    ↓
    ...repetir até convergência...
```

### Critérios de Convergência

O algoritmo pode parar quando:
- Fitness médio estabiliza (variação < ε)
- Melhor fitness não melhora por N gerações
- Número máximo de gerações atingido
- Solução viável satisfatória encontrada

### Métricas de Qualidade

**Além do fitness, monitorar:**
- Taxa de soluções viáveis (sem violações)
- Distribuição de custos de viagem
- Média de entregas por veículo
- Taxa de entregas críticas em rotas iniciais

## Dependências de Dados

### Estrutura de Deliveries (entregas)

```python
deliveries[delivery_id] = {
    "demand": float,       # Peso/volume da entrega
    "priority": int,       # 1=normal, 2=alta, 3=crítica
    "lat": float,          # Latitude
    "lon": float           # Longitude
}
```

**Fonte:** `delivery_setup/deliveries.py`

### Estrutura de Vehicles (veículos)

```python
vehicles[vehicle_id] = {
    "capacity": float,     # Capacidade máxima (kg ou m³)
    "max_range_M": float,  # Autonomia em distância Manhattan
    "cost_M": float        # Custo por unidade de distância
}
```

**Fonte:** `delivery_setup/vehicles.py`

### Estrutura de Solution (solução)

```python
solution = [
    ("V1", (1, 5, 8, 12, 20)),  # Veículo V1 com 5 entregas
    ("V2", (2, 7, 15, 18, 23)), # Veículo V2 com 5 entregas
    ...
]
```

**Fonte:** `a_generate_population.py`

## Casos de Uso e Perguntas Frequentes

### Q: Por que fitness menor é melhor?

**R:** Estamos em um problema de minimização:
- Queremos **minimizar custos** operacionais
- Queremos **minimizar penalidades** (violações)
- Fitness = Custo + Penalidades → quanto menor, melhor

### Q: O que acontece se todas as soluções forem inviáveis?

**R:** O algoritmo continuará evoluindo:
- Soluções menos inviáveis terão vantagem seletiva
- Operadores genéticos buscam viabilidade ao longo das gerações
- Penalidades altas guiam o algoritmo para regiões viáveis do espaço de busca

### Q: Como ajustar para priorizar custo sobre restrições?

**R:** Reduzir pesos de penalidade:
```python
CAPACITY_PENALTY = 50   # Reduzido de 100
AUTONOMY_PENALTY = 100  # Reduzido de 200
```
**Cuidado:** Pode gerar soluções inviáveis operacionalmente

### Q: Como garantir entregas críticas sempre primeiro?

**R:** Aumentar pesos de prioridade:
```python
CRITICAL_WEIGHT = 50     # Aumentado de 12
CRITICAL_POS_WEIGHT = 5  # Aumentado de 1.5
```
**Efeito:** Dominância absoluta de priorização sobre custo

### Q: Qual o fitness de uma solução perfeita?

**R:** Fitness = Custo mínimo possível + 0 (sem penalidades)
```python
# Solução ideal
penalty = 0  # Sem violações
total_cost = soma mínima de (distância × custo)
fitness_ideal = total_cost
```

## Exemplo de Execução

```python
from c_fitness import calculate_fitness
from a_generate_population import generate_population_coordinates

# Gerar população
population = generate_population_coordinates("SP", 50)

# Avaliar primeira solução
solution = population[0]
fitness = calculate_fitness(solution, "SP")

print(f"Solução: {solution}")
print(f"Fitness: {fitness:.2f}")

# Avaliar toda população
fitness_scores = []
for individual in population:
    score = calculate_fitness(individual, "SP")
    fitness_scores.append(score)

# Estatísticas
print(f"\nMelhor fitness: {min(fitness_scores):.2f}")
print(f"Pior fitness: {max(fitness_scores):.2f}")
print(f"Fitness médio: {sum(fitness_scores)/len(fitness_scores):.2f}")
```

## Palavras-chave para Busca

- Função de fitness
- Avaliação de solução
- Algoritmo genético multiobjetivo
- Penalidades de restrição
- Soft constraint
- Hard constraint
- Priorização de entregas
- Custo operacional logístico
- Otimização de capacidade
- Autonomia de veículos
- Eficiência de rota
- VRP fitness
- Função objetivo
- Minimização multiobjetivo
- Balanceamento de pesos
- Hiperparâmetros GA
- Variáveis independentes fitness
- Modelo matemático otimização

## Referências Técnicas

### Notação Matemática
- $F$: Fitness (objetivo a minimizar)
- $C$: Custo (componente econômico)
- $P$: Penalidade (componente de restrição)
- $W$: Peso (hiperparâmetro)
- $v$: Veículo (índice)
- $d$: Entrega (delivery)
- $i$: Índice de rota
- $p$: Posição na rota

### Complexidade
- **Tempo:** $O(V \times E)$ onde $V$ = veículos, $E$ = entregas médias
- **Espaço:** $O(1)$ - cálculos in-place
- **Chamadas:** Uma avaliação por indivíduo por geração

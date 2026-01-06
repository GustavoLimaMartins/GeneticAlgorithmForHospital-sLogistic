# Módulo de Avaliação de Rotas - Métricas de Qualidade da Solução

## Visão Geral

O módulo `routes_evaluation.py` implementa a classe `RouteEvaluator`, responsável por avaliar a qualidade das rotas geradas pelo algoritmo genético através de **três métricas-chave** que mensuram diferentes aspectos da eficiência operacional logística. Este módulo fornece uma análise pós-otimização das soluções, permitindo validação e comparação entre diferentes execuções do algoritmo.

## Objetivo

Avaliar de forma **multidimensional** a qualidade das rotas finais obtidas pelo algoritmo genético, considerando:
1. **Eficiência de carga** (utilização de capacidade dos veículos)
2. **Custo operacional** (despesas totais de deslocamento)
3. **Priorização de entregas** (tratamento de entregas críticas)

Estas métricas complementam a função de fitness, fornecendo visibilidade sobre diferentes aspectos da solução que não são diretamente otimizados mas são importantes para avaliação gerencial.

## Arquitetura da Classe

### Estrutura Básica

```python
class RouteEvaluator:
    def __init__(self, routes_metadata, vehicle_data, delivery_data):
        self.routes_metadata = routes_metadata  # Rotas da solução
        self.vehicle_data = vehicle_data        # Dados dos veículos
        self.delivery_data = delivery_data      # Dados das entregas
```

**Atributos:**
- `routes_metadata`: Dicionário com metadados das rotas
- `vehicle_data`: Informações sobre capacidade, autonomia e custos dos veículos
- `delivery_data`: Informações sobre demanda, prioridade e localização das entregas

### Estrutura de Dados de Entrada

#### routes_metadata (Rotas da Solução)

```python
routes_metadata = {
    1: [("1", "V1"), ("5", "V1"), ("8", "V1"), ("12", "V1"), ("20", "V1")],
    2: [("2", "V2"), ("7", "V2"), ("15", "V2"), ("18", "V2"), ("23", "V2")],
    3: [("3", "V3"), ("6", "V3"), ("9", "V3"), ("14", "V3"), ("22", "V3")],
    4: [("4", "V4"), ("10", "V4"), ("13", "V4"), ("17", "V4"), ("21", "V4")],
    5: [("11", "V5"), ("16", "V5"), ("19", "V5"), ("24", "V5"), ("25", "V5")]
}
```

**Formato:**
- Chave: `route_id` (int) - Identificador da rota
- Valor: Lista de tuplas `(delivery_id, vehicle_id)`
  - `delivery_id` (str): ID da entrega
  - `vehicle_id` (str): ID do veículo atribuído

**Interpretação:**
- Rota 1: Veículo V1 realiza entregas 1, 5, 8, 12, 20
- Cada rota representa a sequência de entregas de um veículo

#### vehicle_data (Dados dos Veículos)

```python
vehicle_data = {
    "V1": {
        "capacity": 100,        # kg ou m³
        "max_range_M": 80,      # Autonomia em unidades Manhattan
        "cost_M": 0.50          # Custo por unidade de distância
    },
    "V2": {
        "capacity": 120,
        "max_range_M": 100,
        "cost_M": 0.60
    },
    ...
}
```

#### delivery_data (Dados das Entregas)

```python
delivery_data = {
    1: {
        "demand": 25,           # kg ou m³
        "priority": 3,          # 1=normal, 2=alta, 3=crítica
        "lat": -23.561684,      # Latitude
        "lon": -46.655981       # Longitude
    },
    2: {
        "demand": 30,
        "priority": 2,
        "lat": -23.550520,
        "lon": -46.633308
    },
    ...
}
```

## Métricas de Avaliação

### 1. Capacity Utilization (Utilização de Capacidade)

#### Conceito

Mede o **percentual de capacidade** de cada veículo que está sendo efetivamente utilizado para transportar entregas. Indica eficiência no aproveitamento dos recursos disponíveis.

#### Função de Cálculo

```python
def capacity_utilization(self) -> dict[int, float]:
    utilization = {}
    for route_id, deliveries in self.routes_metadata.items():
        vehicle_id = deliveries[0][1]  # Primeiro veículo da rota
        vehicle_capacity = self.vehicle_data[vehicle_id]["capacity"]
        total_demand = sum(
            self.delivery_data[int(delivery[0])]["demand"] 
            for delivery in deliveries
        )
        utilization[route_id] = (
            total_demand / vehicle_capacity 
            if vehicle_capacity > 0 
            else 0.0
        )
    return utilization
```

#### Modelo Matemático

Para cada rota $r$:

$$U_r = \frac{\sum_{d \in D_r} \text{demand}_d}{C_v}$$

Onde:
- $U_r$: Utilização da rota $r$ (0.0 a 1.0 ou superior)
- $D_r$: Conjunto de entregas na rota $r$
- $\text{demand}_d$: Demanda (peso/volume) da entrega $d$
- $C_v$: Capacidade máxima do veículo $v$

**Retorno:**
```python
{
    1: 0.85,  # Rota 1: 85% de utilização
    2: 0.92,  # Rota 2: 92% de utilização
    3: 1.05,  # Rota 3: 105% (sobrecarga!)
    4: 0.78,  # Rota 4: 78% de utilização
    5: 0.88   # Rota 5: 88% de utilização
}
```

#### Exemplo Detalhado

**Rota 1:**
```python
# Dados
vehicle_id = "V1"
vehicle_capacity = 100  # kg
deliveries = [("1", "V1"), ("5", "V1"), ("8", "V1"), ("12", "V1"), ("20", "V1")]

# Demandas
demands = {1: 25, 5: 20, 8: 15, 12: 18, 20: 12}

# Cálculo
total_demand = 25 + 20 + 15 + 18 + 12 = 90 kg
utilization = 90 / 100 = 0.90 = 90%
```

**Rota 3 (Sobrecarga):**
```python
# Dados
vehicle_id = "V3"
vehicle_capacity = 80  # kg
demands = {3: 22, 6: 28, 9: 18, 14: 20, 22: 17}

# Cálculo
total_demand = 22 + 28 + 18 + 20 + 17 = 105 kg
utilization = 105 / 80 = 1.3125 = 131.25%  # VIOLAÇÃO!
```

#### Interpretação dos Valores

| Faixa | Interpretação | Ação Recomendada |
|-------|---------------|------------------|
| < 50% | Subutilização severa | Consolidar rotas, usar veículo menor |
| 50-70% | Subutilização moderada | Otimizar alocação |
| 70-90% | Utilização adequada | Ideal para operação |
| 90-100% | Utilização ótima | Excelente aproveitamento |
| > 100% | Sobrecarga (violação) | Redistribuir entregas |

#### Significado Operacional

**Alta Utilização (> 85%):**
- ✅ Máximo aproveitamento da frota
- ✅ Redução de custos fixos por entrega
- ✅ Menor número de veículos necessários

**Baixa Utilização (< 60%):**
- ❌ Desperdício de capacidade
- ❌ Custos operacionais elevados
- ❌ Ineficiência logística

**Sobrecarga (> 100%):**
- ⚠️ Violação de restrição física
- ⚠️ Solução inviável
- ⚠️ Necessita rebalanceamento

#### Métrica Agregada

Na função `metric_summary()`:

```python
"capacity_utilization_metric_positive": 
    sum(capacity_util.values()) / len(capacity_util.keys())
```

**Fórmula:**

$$U_{avg} = \frac{1}{R} \sum_{r=1}^{R} U_r$$

Onde $R$ é o número total de rotas.

**Interpretação:**
- Valor entre 0.0 e 1.0 (ou superior se houver violações)
- **Objetivo:** Maximizar (quanto mais próximo de 1.0, melhor)
- **Ideal:** 0.85 - 0.95 (85-95%)

**Exemplo:**
```python
utilization = {1: 0.90, 2: 0.92, 3: 0.78, 4: 0.88, 5: 0.85}
metric = (0.90 + 0.92 + 0.78 + 0.88 + 0.85) / 5 = 0.866 = 86.6%
# Resultado: Boa utilização média
```

### 2. Travel Costs (Custos de Viagem)

#### Conceito

Calcula o **custo operacional total** de todas as rotas, considerando a distância percorrida por cada veículo e seu custo por unidade de distância. Representa o principal componente de custo variável da operação.

#### Função de Cálculo

```python
def travel_costs(self) -> dict[int, float]:
    costs = {}
    for route_id, deliveries in self.routes_metadata.items():
        vehicle_id = deliveries[0][1]
        vehicle_cost_per_M = self.vehicle_data[vehicle_id]["cost_M"]
        total_distance_M = len(deliveries) * 0.01  # Simplificado
        costs[route_id] = total_distance_M * vehicle_cost_per_M
    return costs
```

**Nota:** O código atual usa uma simplificação (`len(deliveries) * 0.01`). Na implementação completa, deve-se calcular a distância Manhattan real usando `b_manhattan_distance.py`.

#### Modelo Matemático Correto

Para cada rota $r$:

$$C_r = D_r \times K_v$$

Onde:
- $C_r$: Custo da rota $r$
- $D_r$: Distância total da rota (via `route_distance()`)
- $K_v$: Custo por unidade de distância do veículo $v$

**Distância da rota:**

$$D_r = d(C, P_1) + \sum_{i=1}^{n-1} d(P_i, P_{i+1}) + d(P_n, C)$$

Onde:
- $C$: Centro de distribuição
- $P_i$: Ponto de entrega $i$
- $d(A, B)$: Distância Manhattan entre pontos

**Retorno:**
```python
{
    1: 45.50,   # Rota 1: R$ 45.50
    2: 62.30,   # Rota 2: R$ 62.30
    3: 38.90,   # Rota 3: R$ 38.90
    4: 51.20,   # Rota 4: R$ 51.20
    5: 48.75    # Rota 5: R$ 48.75
}
```

#### Exemplo Detalhado

**Rota 1:**
```python
# Dados
vehicle_id = "V1"
cost_per_M = 0.50  # R$/km Manhattan

# Entregas: 1 → 5 → 8 → 12 → 20
# Coordenadas (simplificado)
coords = {
    "center": (0, 0),
    1: (2, 3),
    5: (5, 2),
    8: (7, 4),
    12: (6, 8),
    20: (3, 6)
}

# Cálculo de distância
# Centro → 1: |2-0| + |3-0| = 5
# 1 → 5: |5-2| + |2-3| = 4
# 5 → 8: |7-5| + |4-2| = 4
# 8 → 12: |6-7| + |8-4| = 5
# 12 → 20: |3-6| + |6-8| = 5
# 20 → Centro: |0-3| + |0-6| = 9
# Total: 5 + 4 + 4 + 5 + 5 + 9 = 32 km

# Custo
cost = 32 * 0.50 = R$ 16.00
```

#### Fatores que Influenciam o Custo

**1. Tipo de Veículo:**
```python
# Veículos elétricos: custo menor
cost_electric = distance * 0.30  # R$ 0.30/km

# Veículos a combustão: custo maior
cost_combustion = distance * 0.80  # R$ 0.80/km

# Diferença: 2.67x mais caro
```

**2. Distância da Rota:**
```python
# Rota compacta (entregas próximas)
distance_compact = 25 km
cost_compact = 25 * 0.50 = R$ 12.50

# Rota dispersa (entregas espalhadas)
distance_dispersed = 60 km
cost_dispersed = 60 * 0.50 = R$ 30.00

# Diferença: 2.4x mais caro
```

**3. Número de Entregas:**
```python
# Poucos pontos (mais direto)
points_few = 3
distance_avg = 15 km → custo baixo

# Muitos pontos (mais desvios)
points_many = 10
distance_avg = 45 km → custo alto
```

#### Interpretação dos Valores

**Análise por Rota:**
```python
costs = {1: 45.50, 2: 62.30, 3: 38.90, 4: 51.20, 5: 48.75}

# Rota mais cara: 2 (R$ 62.30)
# Possíveis causas:
# - Veículo com custo/km alto
# - Entregas muito dispersas
# - Muitos desvios

# Rota mais barata: 3 (R$ 38.90)
# Possíveis causas:
# - Veículo econômico
# - Entregas geograficamente próximas
# - Rota otimizada
```

**Análise Comparativa:**
```python
# Custo médio por rota
avg_cost = sum(costs.values()) / len(costs)
avg_cost = 246.65 / 5 = R$ 49.33

# Desvio padrão
import statistics
std_dev = statistics.stdev(costs.values())
std_dev ≈ R$ 8.60

# Coeficiente de variação
cv = std_dev / avg_cost = 8.60 / 49.33 = 0.174 (17.4%)
# Interpretação: Variação moderada entre rotas
```

#### Métrica Agregada

Na função `metric_summary()`:

```python
"travel_costs_metric_negative": 
    sum(travel_costs.values())
```

**Fórmula:**

$$C_{total} = \sum_{r=1}^{R} C_r = \sum_{r=1}^{R} (D_r \times K_v)$$

**Interpretação:**
- Valor em unidades monetárias (R$, $, €, etc.)
- **Objetivo:** Minimizar (quanto menor, melhor)
- Representa custo operacional total da solução

**Exemplo:**
```python
costs = {1: 45.50, 2: 62.30, 3: 38.90, 4: 51.20, 5: 48.75}
total_cost = 45.50 + 62.30 + 38.90 + 51.20 + 48.75 = R$ 246.65
# Custo total da operação logística
```

**Benchmarking:**
```python
# Solução A: R$ 246.65
# Solução B: R$ 289.40
# Solução C: R$ 225.80 ← Melhor

# Economia da C vs A: (246.65 - 225.80) / 246.65 = 8.45%
```

### 3. Critical Delivery Metric (Métrica de Entregas Críticas)

#### Conceito

Avalia a **priorização de entregas críticas** através de uma pontuação ponderada que favorece entregas de alta prioridade em rotas iniciais. Reflete o alinhamento da solução com as prioridades de negócio.

#### Função de Cálculo

**Etapa 1: Contagem por Rota**
```python
def critical_delivery_count_by_deliveries(self) -> dict[int, int]:
    critical_counts = {}
    for route_id, deliveries in self.routes_metadata.items():
        critical_count = sum(
            1 for delivery in deliveries 
            if self.delivery_data[int(delivery[0])]["priority"] > 2
        )
        critical_counts[route_id] = critical_count
    return critical_counts
```

**Retorno:**
```python
{
    1: 3,  # Rota 1: 3 entregas críticas (priority=3)
    2: 1,  # Rota 2: 1 entrega crítica
    3: 0,  # Rota 3: 0 entregas críticas
    4: 2,  # Rota 4: 2 entregas críticas
    5: 0   # Rota 5: 0 entregas críticas
}
```

**Etapa 2: Pontuação Ponderada**
```python
def metric_summary(self):
    critical_counts = self.critical_delivery_count_by_deliveries()
    
    weighted_sum = 0
    for i in critical_counts.keys():
        weighted_sum += critical_counts[i] * (1 - (i * 0.1))
    
    return {
        "critical_delivery_metric_positive": round(weighted_sum, 2)
    }
```

#### Modelo Matemático

**Contagem de Críticas:**

Para cada rota $r$:

$$N_r^{crit} = \sum_{d \in D_r} \mathbb{1}[\text{priority}_d > 2]$$

Onde $\mathbb{1}[\cdot]$ é a função indicadora (1 se verdadeiro, 0 caso contrário).

**Pontuação Ponderada:**

$$S_{crit} = \sum_{r=1}^{R} N_r^{crit} \times w_r$$

Onde o peso da rota é:

$$w_r = 1 - (r \times 0.1)$$

**Tabela de Pesos:**

| Rota | Peso $w_r$ | Significado |
|------|------------|-------------|
| 1 | $1 - (1 \times 0.1) = 0.9$ | 90% do valor |
| 2 | $1 - (2 \times 0.1) = 0.8$ | 80% do valor |
| 3 | $1 - (3 \times 0.1) = 0.7$ | 70% do valor |
| 4 | $1 - (4 \times 0.1) = 0.6$ | 60% do valor |
| 5 | $1 - (5 \times 0.1) = 0.5$ | 50% do valor |
| 6 | $1 - (6 \times 0.1) = 0.4$ | 40% do valor |
| ... | ... | ... |
| 10 | $1 - (10 \times 0.1) = 0.0$ | 0% do valor |
| > 10 | Negativo | Penalização |

#### Lógica da Ponderação

**Princípio:**
- Entregas críticas em **rotas iniciais** recebem **maior pontuação**
- Entregas críticas em **rotas tardias** recebem **menor pontuação**
- Decréscimo linear de 10% por posição de rota

**Justificativa:**
```
Rota 1 (primeira a sair):
- Maior probabilidade de cumprir prazo
- Menos risco de atraso
- Peso máximo (0.9)

Rota 5 (última a sair):
- Menor probabilidade de cumprir prazo
- Maior risco de atraso
- Peso mínimo (0.5)
```

#### Exemplo Detalhado

**Dados:**
```python
critical_counts = {
    1: 3,  # 3 críticas na rota 1
    2: 1,  # 1 crítica na rota 2
    3: 0,  # 0 críticas na rota 3
    4: 2,  # 2 críticas na rota 4
    5: 0   # 0 críticas na rota 5
}
```

**Cálculo:**
```python
# Rota 1: 3 críticas × (1 - 1*0.1)
score_1 = 3 * 0.9 = 2.7

# Rota 2: 1 crítica × (1 - 2*0.1)
score_2 = 1 * 0.8 = 0.8

# Rota 3: 0 críticas × (1 - 3*0.1)
score_3 = 0 * 0.7 = 0.0

# Rota 4: 2 críticas × (1 - 4*0.1)
score_4 = 2 * 0.6 = 1.2

# Rota 5: 0 críticas × (1 - 5*0.1)
score_5 = 0 * 0.5 = 0.0

# Total
weighted_sum = 2.7 + 0.8 + 0.0 + 1.2 + 0.0 = 4.7
```

**Resultado:**
```python
"critical_delivery_metric_positive": 4.7
```

#### Comparação de Cenários

**Cenário A (Ideal): Críticas nas primeiras rotas**
```python
critical_counts = {1: 4, 2: 2, 3: 0, 4: 0, 5: 0}

score = 4*0.9 + 2*0.8 + 0*0.7 + 0*0.6 + 0*0.5
      = 3.6 + 1.6 + 0 + 0 + 0
      = 5.2  ← Alta pontuação (BOM)
```

**Cenário B (Ruim): Críticas nas últimas rotas**
```python
critical_counts = {1: 0, 2: 0, 3: 2, 4: 2, 5: 2}

score = 0*0.9 + 0*0.8 + 2*0.7 + 2*0.6 + 2*0.5
      = 0 + 0 + 1.4 + 1.2 + 1.0
      = 3.6  ← Baixa pontuação (RUIM)
```

**Cenário C (Médio): Distribuído**
```python
critical_counts = {1: 1, 2: 1, 3: 1, 4: 1, 5: 2}

score = 1*0.9 + 1*0.8 + 1*0.7 + 1*0.6 + 2*0.5
      = 0.9 + 0.8 + 0.7 + 0.6 + 1.0
      = 4.0  ← Pontuação média
```

**Análise:**
```
Cenário A: 5.2 (melhor - críticas priorizadas)
Cenário C: 4.0 (médio - distribuição equilibrada)
Cenário B: 3.6 (pior - críticas negligenciadas)

Diferença A-B: 5.2 - 3.6 = 1.6 pontos (44.4% maior)
```

#### Interpretação dos Valores

**Pontuação Alta (> 5.0):**
- ✅ Excelente priorização de entregas críticas
- ✅ Críticas concentradas em rotas iniciais
- ✅ Alta probabilidade de cumprimento de SLA

**Pontuação Média (3.0 - 5.0):**
- ⚠️ Priorização moderada
- ⚠️ Algumas críticas em rotas tardias
- ⚠️ Risco moderado de atraso

**Pontuação Baixa (< 3.0):**
- ❌ Priorização inadequada
- ❌ Críticas em rotas finais
- ❌ Alto risco de descumprimento de SLA

#### Limitações da Métrica Atual

**1. Não considera posição dentro da rota:**
```python
# Ambas têm mesmo peso, mas diferentes riscos:
Rota 1: [crítica_pos_0, normal, normal, normal, normal]  # Melhor
Rota 1: [normal, normal, normal, normal, crítica_pos_4]  # Pior
```

**2. Não pondera por nível de prioridade:**
```python
# Priority 3 (crítica) e Priority 2 (alta) têm tratamento diferente:
# Priority > 2 → Conta
# Priority = 2 → Não conta (embora seja alta prioridade)
```

**3. Pesos fixos e lineares:**
```python
# Decaimento linear pode não refletir realidade operacional
# Decaimento exponencial seria mais realista em alguns casos
```

## Função de Resumo (metric_summary)

### Objetivo

Agregar as três métricas individuais em um **resumo consolidado** que fornece uma visão holística da qualidade da solução.

### Implementação

```python
def metric_summary(self) -> dict[str, float]:
    capacity_util = self.capacity_utilization()
    travel_costs = self.travel_costs()
    critical_counts = self.critical_delivery_count_by_deliveries()
    
    weighted_sum = 0
    for i in critical_counts.keys():
        weighted_sum += critical_counts[i] * (1 - (i * 0.1))

    return {
        "capacity_utilization_metric_positive": round(
            sum(capacity_util.values()) / len(capacity_util.keys()), 2
        ),
        "travel_costs_metric_negative": round(
            sum(travel_costs.values()), 2
        ),
        "critical_delivery_metric_positive": round(
            weighted_sum, 2
        )
    }
```

### Retorno Exemplo

```python
{
    "capacity_utilization_metric_positive": 0.87,   # 87% utilização
    "travel_costs_metric_negative": 246.65,         # R$ 246.65
    "critical_delivery_metric_positive": 4.7        # Score 4.7
}
```

### Interpretação Integrada

**Solução Excelente:**
```python
{
    "capacity_utilization_metric_positive": 0.92,   # Alta utilização
    "travel_costs_metric_negative": 215.30,         # Baixo custo
    "critical_delivery_metric_positive": 5.4        # Ótima priorização
}
```

**Solução Ruim:**
```python
{
    "capacity_utilization_metric_positive": 0.62,   # Subutilização
    "travel_costs_metric_negative": 310.50,         # Alto custo
    "critical_delivery_metric_positive": 2.8        # Má priorização
}
```

### Análise Multiobjetivo

**Trade-offs Comuns:**

1. **Utilização vs Custo:**
```
Alta utilização (0.95) → Pode aumentar distância (R$ 280)
Baixa utilização (0.75) → Pode reduzir distância (R$ 220)

Razão: Consolidar entregas aumenta desvios
```

2. **Priorização vs Custo:**
```
Alta priorização (5.2) → Pode aumentar custo (R$ 265)
Baixa priorização (3.5) → Pode reduzir custo (R$ 235)

Razão: Priorizar críticas pode causar rotas subótimas
```

3. **Utilização vs Priorização:**
```
Maximizar utilização → Pode dispersar críticas
Maximizar priorização → Pode subutilizar veículos

Razão: Veículos lotados com críticas podem não existir
```

## Uso Prático

### Exemplo de Execução

```python
from routes_evaluation import RouteEvaluator
from genetic_algorithm import GeneticAlgorithm

# Configurar e executar GA
ga = GeneticAlgorithm(
    city_code="SP",
    population_length=50,
    max_generations=100,
    ratio_elitism=0.1,
    ratio_mutation=0.3,
    tournament_k=2
)

# Obter melhor solução
ga_metadata = ga.run()
routes_metadata = ga_metadata['routes_metadata']

# Avaliar rotas
evaluator = RouteEvaluator(
    routes_metadata=routes_metadata,
    vehicle_data=ga.vehicles,
    delivery_data=ga.deliveries
)

# Obter métricas detalhadas
capacity_util = evaluator.capacity_utilization()
travel_costs = evaluator.travel_costs()
critical_counts = evaluator.critical_delivery_count_by_deliveries()

# Obter resumo
summary = evaluator.metric_summary()

print("=== RESUMO DAS MÉTRICAS ===")
print(f"Utilização de Capacidade: {summary['capacity_utilization_metric_positive']:.2%}")
print(f"Custo Total: R$ {summary['travel_costs_metric_negative']:.2f}")
print(f"Score de Priorização: {summary['critical_delivery_metric_positive']:.2f}")
```

### Análise Comparativa Entre Execuções

```python
# Executar GA múltiplas vezes
results = []
for run in range(10):
    ga = GeneticAlgorithm(city_code="SP", ...)
    metadata = ga.run()
    evaluator = RouteEvaluator(...)
    summary = evaluator.metric_summary()
    results.append(summary)

# Análise estatística
import statistics

utilizations = [r["capacity_utilization_metric_positive"] for r in results]
costs = [r["travel_costs_metric_negative"] for r in results]
priorities = [r["critical_delivery_metric_positive"] for r in results]

print(f"Utilização: {statistics.mean(utilizations):.2%} ± {statistics.stdev(utilizations):.2%}")
print(f"Custo: R$ {statistics.mean(costs):.2f} ± R$ {statistics.stdev(costs):.2f}")
print(f"Priorização: {statistics.mean(priorities):.2f} ± {statistics.stdev(priorities):.2f}")

# Identificar melhor execução
best_run = min(results, key=lambda x: x["travel_costs_metric_negative"])
print(f"\nMelhor execução: {best_run}")
```

### Relatório de Desempenho

```python
def generate_performance_report(evaluator):
    """Gera relatório completo de desempenho"""
    
    # Métricas individuais
    capacity_util = evaluator.capacity_utilization()
    travel_costs = evaluator.travel_costs()
    critical_counts = evaluator.critical_delivery_count_by_deliveries()
    summary = evaluator.metric_summary()
    
    print("=" * 60)
    print("RELATÓRIO DE AVALIAÇÃO DE ROTAS")
    print("=" * 60)
    
    print("\n1. UTILIZAÇÃO DE CAPACIDADE POR ROTA")
    print("-" * 60)
    for route_id, util in capacity_util.items():
        status = "✓ OK" if 0.7 <= util <= 1.0 else "⚠ ATENÇÃO" if util > 1.0 else "! SUBUTILIZADO"
        print(f"   Rota {route_id}: {util:.2%} {status}")
    print(f"   → Média Geral: {summary['capacity_utilization_metric_positive']:.2%}")
    
    print("\n2. CUSTOS DE VIAGEM POR ROTA")
    print("-" * 60)
    for route_id, cost in travel_costs.items():
        print(f"   Rota {route_id}: R$ {cost:.2f}")
    print(f"   → Custo Total: R$ {summary['travel_costs_metric_negative']:.2f}")
    
    print("\n3. ENTREGAS CRÍTICAS POR ROTA")
    print("-" * 60)
    for route_id, count in critical_counts.items():
        weight = 1 - (route_id * 0.1)
        contribution = count * weight
        print(f"   Rota {route_id}: {count} críticas (peso {weight:.1f}) → {contribution:.2f} pts")
    print(f"   → Score Total: {summary['critical_delivery_metric_positive']:.2f}")
    
    print("\n4. AVALIAÇÃO GERAL")
    print("-" * 60)
    
    # Avaliação de utilização
    avg_util = summary['capacity_utilization_metric_positive']
    if avg_util >= 0.85:
        print("   ✓ Utilização EXCELENTE")
    elif avg_util >= 0.70:
        print("   ✓ Utilização BOA")
    elif avg_util >= 0.60:
        print("   ⚠ Utilização MODERADA")
    else:
        print("   ✗ Utilização INSUFICIENTE")
    
    # Avaliação de custos
    total_cost = summary['travel_costs_metric_negative']
    cost_per_delivery = total_cost / sum(len(d) for d in evaluator.routes_metadata.values())
    print(f"   • Custo por entrega: R$ {cost_per_delivery:.2f}")
    
    # Avaliação de priorização
    priority_score = summary['critical_delivery_metric_positive']
    total_critical = sum(critical_counts.values())
    max_score = total_critical * 0.9  # Se todas na rota 1
    efficiency = (priority_score / max_score * 100) if max_score > 0 else 100
    print(f"   • Eficiência de priorização: {efficiency:.1f}%")
    
    print("=" * 60)

# Uso
generate_performance_report(evaluator)
```

## Melhorias Propostas

### 1. Métrica de Utilização Normalizada

```python
def normalized_capacity_utilization(self) -> dict[int, float]:
    """
    Normaliza utilização para penalizar sobrecargas
    """
    utilization = {}
    for route_id, deliveries in self.routes_metadata.items():
        vehicle_id = deliveries[0][1]
        capacity = self.vehicle_data[vehicle_id]["capacity"]
        demand = sum(self.delivery_data[int(d[0])]["demand"] for d in deliveries)
        
        util_raw = demand / capacity
        
        # Normalizar: [0, 1] ideal, > 1 penalizado
        if util_raw <= 1.0:
            utilization[route_id] = util_raw
        else:
            # Penalização: 1 / (1 + excesso)
            utilization[route_id] = 1.0 / util_raw
    
    return utilization
```

### 2. Custo Considerando Distância Real

```python
from b_manhattan_distance import route_distance

def accurate_travel_costs(self, center_coords) -> dict[int, float]:
    """
    Calcula custo baseado em distância Manhattan real
    """
    costs = {}
    for route_id, deliveries in self.routes_metadata.items():
        vehicle_id = deliveries[0][1]
        cost_per_M = self.vehicle_data[vehicle_id]["cost_M"]
        
        # Obter coordenadas
        coords = [
            (
                self.delivery_data[int(d[0])]["lat"],
                self.delivery_data[int(d[0])]["lon"]
            )
            for d in deliveries
        ]
        
        # Calcular distância real
        distance = route_distance(coords, center_coords)
        
        # Calcular custo
        costs[route_id] = distance * cost_per_M
    
    return costs
```

### 3. Métrica de Prioridade Multinível

```python
def multilevel_priority_score(self) -> float:
    """
    Considera todos os níveis de prioridade (1, 2, 3)
    """
    score = 0
    
    for route_id, deliveries in self.routes_metadata.items():
        route_weight = 1 - (route_id * 0.1)
        
        for delivery in deliveries:
            priority = self.delivery_data[int(delivery[0])]["priority"]
            
            # Pesos por prioridade
            if priority == 3:  # Crítica
                score += route_weight * 1.0
            elif priority == 2:  # Alta
                score += route_weight * 0.5
            elif priority == 1:  # Normal
                score += route_weight * 0.1
    
    return round(score, 2)
```

### 4. Índice de Qualidade Geral (IQG)

```python
def overall_quality_index(self) -> float:
    """
    Combina todas as métricas em um índice único (0-100)
    """
    summary = self.metric_summary()
    
    # Normalizar cada métrica para [0, 1]
    
    # 1. Utilização (já está em [0, 1])
    util_norm = min(summary["capacity_utilization_metric_positive"], 1.0)
    
    # 2. Custo (inverter e normalizar)
    # Assumir custo máximo aceitável = 500
    cost_norm = max(0, 1 - (summary["travel_costs_metric_negative"] / 500))
    
    # 3. Priorização (normalizar por máximo possível)
    # Assumir score máximo = 6.0
    priority_norm = min(summary["critical_delivery_metric_positive"] / 6.0, 1.0)
    
    # Combinar com pesos
    weights = {"utilization": 0.3, "cost": 0.4, "priority": 0.3}
    
    iqg = (
        util_norm * weights["utilization"] +
        cost_norm * weights["cost"] +
        priority_norm * weights["priority"]
    ) * 100
    
    return round(iqg, 2)

# Interpretação:
# IQG >= 80: Excelente
# IQG >= 60: Bom
# IQG >= 40: Regular
# IQG < 40: Insatisfatório
```

## Palavras-chave para Busca

- Avaliação de rotas
- Métricas de qualidade
- Utilização de capacidade
- Custos de viagem
- Entregas críticas
- Priorização de entregas
- KPI logística
- Análise pós-otimização
- Eficiência operacional
- RouteEvaluator
- Métricas positivas e negativas
- Pontuação ponderada
- Trade-off multiobjetivo
- Benchmarking de soluções
- Relatório de desempenho

## Referências Técnicas

### Complexidade Computacional

**capacity_utilization():**
- Tempo: O(R × D) onde R = rotas, D = entregas por rota
- Espaço: O(R)

**travel_costs():**
- Tempo: O(R × D)
- Espaço: O(R)

**critical_delivery_count_by_deliveries():**
- Tempo: O(R × D)
- Espaço: O(R)

**metric_summary():**
- Tempo: O(R × D)
- Espaço: O(1)

### Notação Matemática

- $R$: Número de rotas
- $D_r$: Conjunto de entregas na rota $r$
- $U_r$: Utilização da rota $r$
- $C_r$: Custo da rota $r$
- $N_r^{crit}$: Número de entregas críticas na rota $r$
- $w_r$: Peso da rota $r$
- $S_{crit}$: Score de priorização total

### Métricas Relacionadas

**OEE (Overall Equipment Effectiveness):**
$$\text{OEE} = \text{Disponibilidade} \times \text{Performance} \times \text{Qualidade}$$

**KPIs Logísticos:**
- Fill Rate: Taxa de atendimento de pedidos
- On-Time Delivery: Taxa de entrega no prazo
- Cost per Delivery: Custo por entrega
- Vehicle Utilization: Utilização de frota

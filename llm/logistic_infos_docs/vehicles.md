# Módulo de Veículos - Configuração de Frota

## Visão Geral

O módulo `vehicles.py` é responsável por **definir e carregar** as características da frota de veículos disponível para o sistema de otimização logística. Especifica capacidade de carga, autonomia e custos operacionais de cada veículo, formando as **restrições operacionais** que o algoritmo genético deve respeitar ao gerar soluções viáveis para o problema de roteamento.

## Objetivo

Fornecer especificações técnicas e operacionais da frota, incluindo:
1. **Capacidade de carga:** Limite de unidades que cada veículo pode transportar
2. **Autonomia:** Distância máxima que cada veículo pode percorrer (em unidades Manhattan)
3. **Custo operacional:** Custo por unidade de distância percorrida
4. **Heterogeneidade da frota:** Diferentes tipos de veículos com trade-offs específicos

## Estrutura do Módulo

### Função Principal

```python
def load_vehicles_info(city: str) -> dict[str, dict]:
    """
    Carrega informações dos veículos disponíveis para uma cidade
    
    Args:
        city: Código da cidade (ex: "SP" para São Paulo)
    
    Returns:
        Dicionário com ID do veículo como chave e especificações:
        {
            "V1": {
                "capacity": int,           # Capacidade de carga (unidades)
                "max_range_M": float,      # Autonomia (unidades Manhattan)
                "cost_M": float            # Custo por unidade Manhattan (R$)
            },
            ...
        }
    
    Retorna dicionário vazio se a cidade não estiver configurada
    """
```

### Assinatura e Retorno

**Input:**
- `city` (str): Código da cidade
  - "SP": São Paulo (único suportado atualmente)

**Output:**
```python
{
    "V1": {"capacity": 45, "max_range_M": 0.065, "cost_M": 180.0},
    "V2": {"capacity": 30, "max_range_M": 0.045, "cost_M": 120.0},
    "V3": {"capacity": 20, "max_range_M": 0.030, "cost_M": 85.0},
    "V4": {"capacity": 12, "max_range_M": 0.020, "cost_M": 60.0},
    "V5": {"capacity": 6,  "max_range_M": 0.012, "cost_M": 35.0}
}
```

**Estrutura de Cada Veículo:**

| Campo | Tipo | Descrição | Unidade | Exemplo |
|-------|------|-----------|---------|---------|
| `capacity` | int | Capacidade máxima de carga | unidades | 45 |
| `max_range_M` | float | Autonomia máxima | unidades Manhattan | 0.065 |
| `cost_M` | float | Custo operacional | R$ por unidade Manhattan | 180.0 |

## Configuração da Frota para São Paulo (SP)

### Especificações Completas

```
┌─────────┬──────────┬──────────────┬────────────┬────────────────────┐
│ Veículo │ Capacity │ Max_Range_M  │  Cost_M    │ Classificação      │
├─────────┼──────────┼──────────────┼────────────┼────────────────────┤
│   V1    │    45    │    0.065     │   180.0    │ Grande             │
│   V2    │    30    │    0.045     │   120.0    │ Médio-Grande       │
│   V3    │    20    │    0.030     │    85.0    │ Médio              │
│   V4    │    12    │    0.020     │    60.0    │ Pequeno-Médio      │
│   V5    │     6    │    0.012     │    35.0    │ Pequeno            │
└─────────┴──────────┴──────────────┴────────────┴────────────────────┘
```

### Perfis Detalhados

#### V1 - Veículo Grande

```python
"V1": {
    "capacity": 45,          # Maior capacidade da frota
    "max_range_M": 0.065,    # Maior autonomia
    "cost_M": 180.0          # Maior custo operacional
}
```

**Características:**
- **Tipo:** Caminhão grande / Van de grande porte
- **Capacidade:** 45 unidades (38.7% da demanda total de 230)
- **Autonomia:** 0.065 unidades Manhattan
- **Custo:** R$ 180.00 por unidade Manhattan
- **Custo/Capacidade:** R$ 4.00 por unidade transportada por unidade Manhattan
- **Eficiência:** Alta para rotas longas com muitas entregas

**Melhor Para:**
- Rotas com muitas entregas consolidadas
- Percursos longos onde autonomia é crítica
- Entregas volumosas (demanda individual alta)
- Maximizar utilização quando há carga suficiente

**Limitações:**
- Custo alto para rotas curtas ou com poucas entregas
- Pode ser ocioso se demanda não preencher capacidade
- Menos flexível para entregas isoladas

#### V2 - Veículo Médio-Grande

```python
"V2": {
    "capacity": 30,
    "max_range_M": 0.045,
    "cost_M": 120.0
}
```

**Características:**
- **Tipo:** Van média / Caminhão médio
- **Capacidade:** 30 unidades (66.7% de V1)
- **Autonomia:** 0.045 unidades Manhattan (69.2% de V1)
- **Custo:** R$ 120.00 por unidade Manhattan (66.7% de V1)
- **Custo/Capacidade:** R$ 4.00 por unidade
- **Eficiência:** Balanceada para rotas médias

**Melhor Para:**
- Rotas de comprimento médio
- Balanceamento entre capacidade e custo
- Flexibilidade operacional
- Substituir V1 quando capacidade não é totalmente utilizada

**Limitações:**
- Menor autonomia pode restringir rotas longas
- Capacidade pode ser insuficiente para grandes consolidações

#### V3 - Veículo Médio

```python
"V3": {
    "capacity": 20,
    "max_range_M": 0.030,
    "cost_M": 85.0
}
```

**Características:**
- **Tipo:** Van compacta / Utilitário médio
- **Capacidade:** 20 unidades (44.4% de V1)
- **Autonomia:** 0.030 unidades Manhattan (46.2% de V1)
- **Custo:** R$ 85.00 por unidade Manhattan (47.2% de V1)
- **Custo/Capacidade:** R$ 4.25 por unidade
- **Eficiência:** Média, ponto de equilíbrio

**Melhor Para:**
- Rotas locais com entregas próximas
- Atender clusters de entregas pequenas
- Backup para veículos maiores
- Rotas onde autonomia não é crítica

**Limitações:**
- Custo/capacidade ligeiramente menos eficiente
- Requer mais veículos para cobrir demanda total
- Autonomia limitada

#### V4 - Veículo Pequeno-Médio

```python
"V4": {
    "capacity": 12,
    "max_range_M": 0.020,
    "cost_M": 60.0
}
```

**Características:**
- **Tipo:** Utilitário pequeno / Van compacta
- **Capacidade:** 12 unidades (26.7% de V1)
- **Autonomia:** 0.020 unidades Manhattan (30.8% de V1)
- **Custo:** R$ 60.00 por unidade Manhattan (33.3% de V1)
- **Custo/Capacidade:** R$ 5.00 por unidade
- **Eficiência:** Menor para transporte, boa para flexibilidade

**Melhor Para:**
- Entregas de última milha
- Rotas muito curtas
- Complementar outros veículos
- Entregas isoladas de baixa demanda

**Limitações:**
- Custo/capacidade menos eficiente que veículos maiores
- Autonomia muito limitada
- Não adequado para consolidação

#### V5 - Veículo Pequeno

```python
"V5": {
    "capacity": 6,
    "max_range_M": 0.012,
    "cost_M": 35.0
}
```

**Características:**
- **Tipo:** Veículo urbano pequeno / Moto com baú
- **Capacidade:** 6 unidades (13.3% de V1, menor da frota)
- **Autonomia:** 0.012 unidades Manhattan (18.5% de V1, menor)
- **Custo:** R$ 35.00 por unidade Manhattan (19.4% de V1, menor)
- **Custo/Capacidade:** R$ 5.83 por unidade
- **Eficiência:** Menor custo absoluto, mas pior custo/capacidade

**Melhor Para:**
- Entregas urgentes individuais
- Rotas extremamente curtas
- Complementar frota em situações específicas
- Baixo custo operacional absoluto

**Limitações:**
- Pior custo/capacidade da frota (R$ 5.83 vs R$ 4.00)
- Autonomia muito restrita
- Não adequado para volume
- Requer muitos veículos para demanda total

## Análise Comparativa da Frota

### 1. Relação Capacidade vs Custo

```python
# Análise de eficiência
vehicles_efficiency = {
    "V1": {"capacity": 45, "cost_M": 180.0, "cost_per_unit": 4.00},
    "V2": {"capacity": 30, "cost_M": 120.0, "cost_per_unit": 4.00},
    "V3": {"capacity": 20, "cost_M": 85.0,  "cost_per_unit": 4.25},
    "V4": {"capacity": 12, "cost_M": 60.0,  "cost_per_unit": 5.00},
    "V5": {"capacity": 6,  "cost_M": 35.0,  "cost_per_unit": 5.83}
}
```

**Gráfico de Eficiência:**
```
Custo por Unidade de Capacidade (R$/unidade por unidade Manhattan)

V1 │████                    4.00 ← Mais eficiente
V2 │████                    4.00 ← Mais eficiente
V3 │████▌                   4.25
V4 │█████                   5.00
V5 │█████▊                  5.83 ← Menos eficiente
   └────────────────────────────────────────────
    0     1     2     3     4     5     6
```

**Interpretação:**
- **V1 e V2** têm a **melhor eficiência** (R$ 4.00 por unidade)
- **V3** é razoável (R$ 4.25, apenas 6.25% mais caro)
- **V4 e V5** são significativamente **menos eficientes**
- Trade-off: eficiência vs flexibilidade/custo absoluto

### 2. Relação Autonomia vs Capacidade

```python
# Proporção autonomia/capacidade
autonomy_ratio = {
    "V1": 0.065 / 45 = 0.001444,  # Melhor proporção
    "V2": 0.045 / 30 = 0.001500,
    "V3": 0.030 / 20 = 0.001500,
    "V4": 0.020 / 12 = 0.001667,
    "V5": 0.012 / 6  = 0.002000   # Pior proporção
}
```

**Observação:**
- Autonomia **não é proporcional** à capacidade
- Veículos maiores têm **melhor relação** autonomia/capacidade
- Veículos pequenos precisam de **mais viagens** para mesma carga em distâncias equivalentes

### 3. Capacidade Total da Frota

```python
# Análise de capacidade
total_capacity = 45 + 30 + 20 + 12 + 6 = 113 unidades
total_demand = 230 unidades  # Das entregas

utilization_scenarios = {
    "ideal": total_demand / total_capacity = 203.5%,  # Requer ~2 viagens
    "single_trip_capacity": total_capacity = 113,      # Máx por viagem
    "coverage": total_capacity / total_demand = 49.1%  # Uma viagem cobre 49.1%
}
```

**Análise:**
- Capacidade total por viagem: **113 unidades**
- Demanda total: **230 unidades**
- **Deficiência:** Capacidade é insuficiente para atender todas as entregas em uma única viagem
- **Implicação:** Sistema deve otimizar uso de capacidade e não permite múltiplas viagens

**Nota Importante:** O sistema atual considera **apenas uma viagem por veículo**, portanto:
- Nem todas as entregas podem ser atendidas se todas são incluídas
- **OU** há erro conceitual: cada veículo deve poder atender um subconjunto das entregas
- **OU** há restrição implícita de priorização (atender mais importantes)

### 4. Estatísticas da Frota

```python
# Médias
avg_capacity = 113 / 5 = 22.6 unidades
avg_autonomy = (0.065 + 0.045 + 0.030 + 0.020 + 0.012) / 5 = 0.0344
avg_cost = (180 + 120 + 85 + 60 + 35) / 5 = 96.0 R$/unidade Manhattan

# Desvio padrão
std_capacity ≈ 14.9 unidades  # Alta variabilidade
std_autonomy ≈ 0.0199          # Alta variabilidade
std_cost ≈ 56.3                # Alta variabilidade

# Coeficiente de variação
cv_capacity = 14.9 / 22.6 = 0.66  (66%)
cv_autonomy = 0.0199 / 0.0344 = 0.58  (58%)
cv_cost = 56.3 / 96.0 = 0.59  (59%)
```

**Interpretação:**
- **Alta heterogeneidade** na frota (CV > 50%)
- Frota **bem diversificada** para diferentes cenários
- Permite **flexibilidade** de alocação
- Requer **otimização cuidadosa** para balanceamento

## Unidades Manhattan

### Conceito

**Distância Manhattan:**
$$d_{Manhattan}(P_1, P_2) = |x_1 - x_2| + |y_1 - y_2|$$

Para coordenadas geográficas:
$$d_{Manhattan} = |\text{lat}_1 - \text{lat}_2| + |\text{lon}_1 - \text{lon}_2|$$

**Exemplo:**
```python
# Ponto A: (-23.5987, -46.7158)
# Ponto B: (-23.5523, -46.7456)

d_M = |-23.5987 - (-23.5523)| + |-46.7158 - (-46.7456)|
    = 0.0464 + 0.0298
    = 0.0762 unidades Manhattan
```

### Conversão para Distância Real

**Aproximação para São Paulo:**
```python
# 1 grau de latitude ≈ 111 km
# 1 grau de longitude ≈ 96 km (na latitude de SP)

# Conversão média
1 unidade Manhattan ≈ (111 + 96) / 2 = 103.5 km

# Exemplo
0.065 unidades Manhattan ≈ 6.7 km
```

### Autonomia dos Veículos em km

```python
autonomy_km = {
    "V1": 0.065 × 103.5 ≈ 6.7 km,
    "V2": 0.045 × 103.5 ≈ 4.7 km,
    "V3": 0.030 × 103.5 ≈ 3.1 km,
    "V4": 0.020 × 103.5 ≈ 2.1 km,
    "V5": 0.012 × 103.5 ≈ 1.2 km
}
```

**Interpretação:**
- Autonomias são **muito baixas** para rotas urbanas típicas
- Valores representam **segmentos curtos** ou **fator de escala**
- Possível interpretação: fator de penalização, não autonomia real

### Custo Real por km

```python
cost_per_km = {
    "V1": 180.0 / 103.5 ≈ R$ 1.74/km,
    "V2": 120.0 / 103.5 ≈ R$ 1.16/km,
    "V3": 85.0 / 103.5  ≈ R$ 0.82/km,
    "V4": 60.0 / 103.5  ≈ R$ 0.58/km,
    "V5": 35.0 / 103.5  ≈ R$ 0.34/km
}
```

**Observação:** Custos realistas para operação urbana em São Paulo.

## Integração com o Sistema

### Fluxo de Uso no Pipeline

```
1. CARREGAMENTO
   └─> load_vehicles_info("SP")
       └─> Retorna dict com 5 veículos

2. INICIALIZAÇÃO DO GA
   └─> GeneticAlgorithm(city_code="SP")
       └─> self.vehicles = load_vehicles_info("SP")

3. FUNÇÃO FITNESS
   └─> fitness_function(solution, deliveries, vehicles)
       ├─> Verifica capacity para cada rota
       ├─> Calcula travel_cost usando cost_M
       └─> Penaliza violações de max_range_M

4. AVALIAÇÃO DE ROTAS
   └─> RouteEvaluator(routes, deliveries, vehicles)
       ├─> capacity_utilization: compara com capacity
       └─> travel_costs: usa cost_M × distância
```

### Exemplo de Uso

```python
from delivery_setup.vehicles import load_vehicles_info

# Carregar veículos
vehicles = load_vehicles_info("SP")

# Acessar veículo específico
v1 = vehicles["V1"]
print(f"Veículo V1:")
print(f"  Capacidade: {v1['capacity']} unidades")
print(f"  Autonomia: {v1['max_range_M']} unidades Manhattan")
print(f"  Custo: R$ {v1['cost_M']}/unidade Manhattan")

# Output:
# Veículo V1:
#   Capacidade: 45 unidades
#   Autonomia: 0.065 unidades Manhattan
#   Custo: R$ 180.0/unidade Manhattan

# Calcular capacidade total
total_cap = sum(v['capacity'] for v in vehicles.values())
print(f"Capacidade total da frota: {total_cap} unidades")
# Output: Capacidade total da frota: 113 unidades

# Encontrar veículo mais eficiente
most_efficient = min(
    vehicles.items(),
    key=lambda x: x[1]['cost_M'] / x[1]['capacity']
)
print(f"Veículo mais eficiente: {most_efficient[0]}")
# Output: Veículo mais eficiente: V1 (ou V2, empate)
```

## Restrições e Penalidades no Sistema

### 1. Restrição de Capacidade

```python
# No módulo c_fitness.py
CAPACITY_PENALTY = 100  # Penalidade por excesso de capacidade

# Para cada rota
route_demand = sum(delivery['demand'] for delivery in route)
vehicle_capacity = vehicles[vehicle_id]['capacity']

if route_demand > vehicle_capacity:
    capacity_penalty = (route_demand - vehicle_capacity) * CAPACITY_PENALTY
else:
    capacity_penalty = 0
```

**Exemplo:**
```python
# Rota com V3 (capacity=20)
route_deliveries = [3, 8]  # Demandas: 15 + 15 = 30
excesso = 30 - 20 = 10 unidades
penalidade = 10 × 100 = 1000

# Fitness penalizado severamente
```

### 2. Restrição de Autonomia

```python
# No módulo c_fitness.py
AUTONOMY_PENALTY = 200  # Penalidade por excesso de autonomia

# Para cada rota
route_distance = calculate_route_distance_manhattan(route)
vehicle_autonomy = vehicles[vehicle_id]['max_range_M']

if route_distance > vehicle_autonomy:
    autonomy_penalty = (route_distance - vehicle_autonomy) * AUTONOMY_PENALTY
else:
    autonomy_penalty = 0
```

**Exemplo:**
```python
# Rota com V5 (max_range_M=0.012)
route_distance = 0.025 unidades Manhattan
excesso = 0.025 - 0.012 = 0.013
penalidade = 0.013 × 200 = 2.6

# Penalidade menor que capacidade, mas significativa
```

### 3. Custo de Viagem

```python
# No módulo c_fitness.py
# Para cada rota
route_distance = calculate_route_distance_manhattan(route)
vehicle_cost = vehicles[vehicle_id]['cost_M']

travel_cost = route_distance × vehicle_cost
```

**Exemplo:**
```python
# Rota de 0.040 unidades Manhattan com V2
travel_cost = 0.040 × 120.0 = 4.8 R$
```

## Análise de Alocação Ótima

### Cenário 1: Maximizar Eficiência

**Estratégia:** Usar apenas V1 e V2 (mais eficientes)

```python
# Capacidades
v1_capacity = 45
v2_capacity = 30
total_v1_v2 = 75 unidades

# Demanda total: 230 unidades
# Não é suficiente, requer incluir outros veículos
```

**Resultado:** Impossível atender todas as entregas apenas com V1 e V2.

### Cenário 2: Usar Toda a Frota

**Estratégia:** Distribuir entregas entre todos os 5 veículos

```python
# Capacidade total
total_capacity = 113 unidades

# Demanda total: 230 unidades
# Déficit: 230 - 113 = 117 unidades

# Conclusão: Ainda insuficiente
```

**Resultado:** Sistema precisa de **priorização** ou **múltiplas viagens**.

### Cenário 3: Priorizar Entregas Críticas

**Estratégia:** Atender apenas entregas críticas e moderadas primeiro

```python
# Entregas críticas (priority=1): 4 entregas, demanda total 60
# Entregas moderadas (priority=2): 12 entregas, demanda total 96
# Total prioritário: 156 unidades

# Alocação sugerida
route_v1 = [3, 8, 17]      # Demanda: 15+15+15=45 (100% utilização)
route_v2 = [22, 2, 10]     # Demanda: 15+12+6=33 (110% utilização - excede!)
# ... ajustar
```

**Resultado:** Requer otimização algorítmica (GA).

### Cenário 4: Balanceamento Ideal

**Estratégia:** Balancear carga entre veículos

```python
# Objetivo: Maximizar utilização média
target_loads = {
    "V1": 43,  # 95.6% utilização
    "V2": 28,  # 93.3% utilização
    "V3": 19,  # 95.0% utilização
    "V4": 11,  # 91.7% utilização
    "V5": 12   # Excede capacidade - não viável
}

# Total: 113 unidades (máximo possível)
# Entregas não atendidas: 230 - 113 = 117 unidades
```

**Conclusão:** Sistema tem **restrição fundamental** de capacidade.

## Trade-offs de Seleção de Veículos

### Trade-off 1: Capacidade vs Custo

```
Alta Capacidade (V1, V2)
├─ Vantagens
│  ├─ Consolidação de entregas
│  ├─ Menos rotas necessárias
│  └─ Melhor custo/unidade
└─ Desvantagens
   ├─ Custo absoluto alto
   ├─ Ociosidade se carga insuficiente
   └─ Menos flexível

Baixa Capacidade (V4, V5)
├─ Vantagens
│  ├─ Custo absoluto baixo
│  ├─ Flexibilidade
│  └─ Adequado para entregas isoladas
└─ Desvantagens
   ├─ Pior custo/unidade
   ├─ Requer mais veículos
   └─ Maior tempo total de operação
```

### Trade-off 2: Autonomia vs Flexibilidade

```
Alta Autonomia (V1, V2, V3)
├─ Vantagens
│  ├─ Rotas mais longas possíveis
│  ├─ Maior raio de ação
│  └─ Menos restrição de planejamento
└─ Desvantagens
   ├─ Custo maior
   └─ Pode ser desnecessária para rotas curtas

Baixa Autonomia (V4, V5)
├─ Vantagens
│  ├─ Custo menor
│  └─ Adequado para entregas locais
└─ Desvantagens
   ├─ Restrição severa de distância
   ├─ Penalidades se rota excede
   └─ Planejamento mais complexo
```

### Trade-off 3: Homogeneidade vs Heterogeneidade

```
Frota Homogênea (ex: 5× V3)
├─ Vantagens
│  ├─ Simplicidade de planejamento
│  ├─ Intercambialidade
│  └─ Previsibilidade de custos
└─ Desvantagens
   ├─ Menos adaptação a cenários variados
   ├─ Eficiência subótima
   └─ Ponto único de falha

Frota Heterogênea (atual: V1-V5)
├─ Vantagens
│  ├─ Adaptação a diferentes necessidades
│  ├─ Otimização por tipo de rota
│  └─ Maior flexibilidade operacional
└─ Desvantagens
   ├─ Complexidade de planejamento
   ├─ Algoritmo deve escolher veículo correto
   └─ Mais difícil balancear carga
```

## Modelagem Matemática

### Função de Custo Total

$$C_{total} = \sum_{v \in V} \left( d_v \times c_v \right)$$

Onde:
- $V$: Conjunto de veículos utilizados
- $d_v$: Distância percorrida pelo veículo $v$ (unidades Manhattan)
- $c_v$: Custo por unidade Manhattan do veículo $v$

### Restrições

**1. Capacidade:**
$$\sum_{i \in R_v} \text{demand}_i \leq \text{capacity}_v \quad \forall v \in V$$

Onde $R_v$ é o conjunto de entregas na rota do veículo $v$.

**2. Autonomia:**
$$d_v \leq \text{max\_range}_v \quad \forall v \in V$$

**3. Cobertura:**
$$\bigcup_{v \in V} R_v = D$$

Onde $D$ é o conjunto de todas as entregas (ideal, mas inviável com frota atual).

**4. Não-sobreposição:**
$$R_v \cap R_w = \emptyset \quad \forall v, w \in V, v \neq w$$

### Objetivo Multi-critério

$$\min \left\{ C_{total}, P_{capacity}, P_{autonomy}, P_{priority} \right\}$$

Onde:
- $C_{total}$: Custo total de viagem
- $P_{capacity}$: Penalidade por violação de capacidade
- $P_{autonomy}$: Penalidade por violação de autonomia
- $P_{priority}$: Penalidade por não priorizar entregas críticas

## Extensibilidade para Novas Cidades

### Template para Nova Cidade

```python
def load_vehicles_info(city: str) -> dict[str, dict]:
    if city == "SP":
        # ... código existente ...
    
    elif city == "RJ":  # Exemplo: Rio de Janeiro
        return {
            "V1": {
                "capacity": 50,          # Ajustado para demanda local
                "max_range_M": 0.070,
                "cost_M": 190.0
            },
            "V2": {
                "capacity": 35,
                "max_range_M": 0.050,
                "cost_M": 130.0
            },
            # ... outros veículos
        }
    
    else:
        return {}
```

### Diretrizes para Configuração

**1. Número de Veículos:**
- Calcular demanda total da cidade
- Definir capacidade mínima: `total_capacity ≥ 1.1 × total_demand`
- Recomendado: 5-10 veículos para flexibilidade

**2. Valores de Capacidade:**
- Refletir tipos reais de veículos disponíveis
- Manter proporções realistas (ex: 2:1, 3:2 entre níveis)
- Garantir cobertura: maior capacidade ≥ max(demand)

**3. Autonomia:**
- Considerar geografia da cidade (área urbana)
- Converter raio típico para unidades Manhattan
- Garantir: `max_range ≥ 2 × max_distance_between_deliveries`

**4. Custos:**
- Basear em custos operacionais reais (combustível, manutenção, depreciação)
- Manter proporção com capacidade (economias de escala)
- Considerar custos locais (pedágio, estacionamento, etc.)

## Validação e Consistência

### Validações Recomendadas

```python
def validate_vehicles(vehicles: dict, deliveries: dict) -> bool:
    """
    Valida consistência dos dados de veículos
    """
    # 1. Verificar estrutura
    for vid, vehicle in vehicles.items():
        required_fields = {'capacity', 'max_range_M', 'cost_M'}
        assert required_fields == set(vehicle.keys()), \
            f"Veículo {vid} com campos inválidos"
    
    # 2. Verificar valores positivos
    for vid, vehicle in vehicles.items():
        assert vehicle['capacity'] > 0, \
            f"Capacidade deve ser positiva no veículo {vid}"
        assert vehicle['max_range_M'] > 0, \
            f"Autonomia deve ser positiva no veículo {vid}"
        assert vehicle['cost_M'] > 0, \
            f"Custo deve ser positivo no veículo {vid}"
    
    # 3. Verificar viabilidade com entregas
    max_demand = max(d['demand'] for d in deliveries.values())
    max_capacity = max(v['capacity'] for v in vehicles.values())
    assert max_capacity >= max_demand, \
        f"Nenhum veículo pode transportar entrega de demanda {max_demand}"
    
    # 4. Verificar capacidade total vs demanda total
    total_capacity = sum(v['capacity'] for v in vehicles.values())
    total_demand = sum(d['demand'] for d in deliveries.values())
    if total_capacity < total_demand:
        print(f"AVISO: Capacidade total ({total_capacity}) < Demanda total ({total_demand})")
        print(f"Sistema requer priorização ou múltiplas viagens")
    
    # 5. Verificar correlação capacidade-custo
    vehicles_sorted = sorted(vehicles.items(), key=lambda x: x[1]['capacity'])
    for i in range(len(vehicles_sorted) - 1):
        v1 = vehicles_sorted[i][1]
        v2 = vehicles_sorted[i+1][1]
        assert v1['cost_M'] <= v2['cost_M'], \
            "Esperado: veículos maiores têm custo maior ou igual"
    
    return True

# Uso
vehicles = load_vehicles_info("SP")
deliveries = load_deliveries_info("SP")
validate_vehicles(vehicles, deliveries)
```

### Verificação de Escalabilidade

```python
def check_fleet_adequacy(vehicles: dict, deliveries: dict) -> dict:
    """
    Analisa adequação da frota para a demanda
    """
    total_capacity = sum(v['capacity'] for v in vehicles.values())
    total_demand = sum(d['demand'] for d in deliveries.values())
    
    return {
        'total_capacity': total_capacity,
        'total_demand': total_demand,
        'coverage_ratio': total_capacity / total_demand,
        'adequate': total_capacity >= total_demand,
        'recommended_vehicles': max(1, int(total_demand / total_capacity) + 1)
    }

# Uso
adequacy = check_fleet_adequacy(vehicles, deliveries)
print(f"Cobertura: {adequacy['coverage_ratio']:.1%}")
# Output: Cobertura: 49.1% (inadequado)
```

## Impacto na Qualidade da Solução

### Fatores de Complexidade

**1. Heterogeneidade:**
- 5 tipos diferentes de veículos
- Requer **decisão de alocação** (qual veículo para qual rota?)
- Aumenta **espaço de busca** do GA
- Mas permite **soluções mais otimizadas**

**2. Restrições Múltiplas:**
- Capacidade **E** autonomia devem ser respeitadas
- Trade-off entre **minimizar custo** e **respeitar restrições**
- Penalidades guiam busca, mas aumentam **complexidade da função fitness**

**3. Capacidade Limitada:**
- **113 unidades** vs **230 unidades** de demanda
- Sistema **não pode atender todas as entregas**
- Requer **priorização** ou **redesign do problema**

## Cenários de Teste

### Cenário 1: Frota Homogênea

```python
# Modificar para teste
def load_uniform_fleet():
    return {
        f"V{i}": {
            "capacity": 25,
            "max_range_M": 0.035,
            "cost_M": 100.0
        }
        for i in range(1, 6)
    }

# Esperado: Simplificação do problema, mas perda de flexibilidade
```

### Cenário 2: Frota Grande

```python
# Teste com veículos maiores
def load_large_fleet():
    return {
        "V1": {"capacity": 60, "max_range_M": 0.080, "cost_M": 220.0},
        "V2": {"capacity": 55, "max_range_M": 0.075, "cost_M": 200.0},
        "V3": {"capacity": 50, "max_range_M": 0.070, "cost_M": 180.0},
        "V4": {"capacity": 45, "max_range_M": 0.065, "cost_M": 160.0},
        "V5": {"capacity": 40, "max_range_M": 0.060, "cost_M": 140.0}
    }
    # Total capacity: 250 > 230 (adequado)

# Esperado: Cobertura completa, mas custos mais altos
```

### Cenário 3: Sem Restrição de Autonomia

```python
# Teste com autonomia infinita
def load_unlimited_autonomy():
    vehicles = load_vehicles_info("SP")
    for v in vehicles.values():
        v['max_range_M'] = 1.0  # Muito alto
    return vehicles

# Esperado: Problema simplificado, apenas restrição de capacidade
```

## Palavras-chave para Busca

- Veículos
- Frota
- Capacidade de carga
- Autonomia
- Distância Manhattan
- Custo operacional
- Cost_M
- Max_range_M
- Heterogeneidade de frota
- Restrições de capacidade
- Restrições de autonomia
- Trade-off capacidade-custo
- Eficiência de veículos
- Alocação de veículos
- V1 V2 V3 V4 V5
- Vehicle Routing
- Configuração de frota
- Especificações técnicas

## Resumo Executivo

### Características Principais

**Frota:**
- **5 veículos** com especificações heterogêneas (V1-V5)
- **Capacidade total:** 113 unidades por viagem
- **Demanda total:** 230 unidades (sistema subdimensionado)

**Veículos:**
- **V1 (Grande):** 45 cap, 0.065 autonomia, R$ 180/M (mais eficiente)
- **V2 (Médio-Grande):** 30 cap, 0.045 autonomia, R$ 120/M (eficiente)
- **V3 (Médio):** 20 cap, 0.030 autonomia, R$ 85/M
- **V4 (Pequeno-Médio):** 12 cap, 0.020 autonomia, R$ 60/M
- **V5 (Pequeno):** 6 cap, 0.012 autonomia, R$ 35/M (menos eficiente)

**Eficiência:**
- **Melhor:** V1 e V2 (R$ 4.00 por unidade/M)
- **Pior:** V5 (R$ 5.83 por unidade/M)
- **Diferença:** 45.75% entre melhor e pior

**Restrições:**
- Capacidade: Penalidade 100 × excesso
- Autonomia: Penalidade 200 × excesso
- Custo: Distância × cost_M

**Desafio Principal:**
- Capacidade insuficiente para atender todas as entregas
- Requer priorização ou redesign

### Uso Típico

```python
# 1. Carregar
vehicles = load_vehicles_info("SP")

# 2. Analisar
total_cap = sum(v['capacity'] for v in vehicles.values())  # 113

# 3. Selecionar mais eficiente
best = min(vehicles.items(), key=lambda x: x[1]['cost_M']/x[1]['capacity'])
# best = ("V1", {...}) ou ("V2", {...})

# 4. Usar no GA
ga = GeneticAlgorithm(city_code="SP")  # Internamente carrega vehicles

# 5. Calcular custo de rota
route_distance = 0.035  # unidades Manhattan
vehicle_id = "V2"
cost = route_distance × vehicles[vehicle_id]['cost_M']  # 0.035 × 120 = 4.2
```

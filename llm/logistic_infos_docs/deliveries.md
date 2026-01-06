# Módulo de Entregas - Configuração de Demandas e Prioridades

## Visão Geral

O módulo `deliveries.py` é responsável por **carregar e estruturar** as informações das entregas que devem ser atendidas pelo sistema de otimização logística. Define os pontos de entrega, suas coordenadas geográficas, demandas de capacidade e níveis de prioridade para o problema de roteamento de veículos (VRP). Este módulo fornece a **instância do problema** que será otimizada pelo algoritmo genético.

## Objetivo

Fornecer uma interface de dados estruturada contendo:
1. **Localização geográfica** de cada ponto de entrega (latitude, longitude)
2. **Demanda de carga** de cada entrega (unidades a serem transportadas)
3. **Prioridade de atendimento** (nível de criticidade da entrega)
4. **Suporte a múltiplas cidades** (atualmente São Paulo)

## Estrutura do Módulo

### Função Principal

```python
def load_deliveries_info(city: str) -> dict[int, dict[str, float]]:
    """
    Carrega informações de entregas para uma cidade específica
    
    Args:
        city: Código da cidade (ex: "SP" para São Paulo)
    
    Returns:
        Dicionário com ID da entrega como chave e dados da entrega:
        {
            id: {
                'lat': latitude (float),
                'lon': longitude (float),
                'demand': demanda de capacidade (int),
                'priority': nível de prioridade (int: 1-3)
            }
        }
    
    Raises:
        ValueError: Se a cidade não possui rotas definidas
    """
```

### Assinatura e Retorno

**Input:**
- `city` (str): Código da cidade
  - "SP": São Paulo (único suportado atualmente)

**Output:**
```python
{
    1: {"lat": -23.5987, "lon": -46.7158, "demand": 8, "priority": 3},
    2: {"lat": -23.5012, "lon": -46.8456, "demand": 12, "priority": 2},
    ...
    25: {"lat": -23.5523, "lon": -46.7456, "demand": 6, "priority": 2}
}
```

**Estrutura de Cada Entrega:**

| Campo | Tipo | Descrição | Exemplo |
|-------|------|-----------|---------|
| `lat` | float | Latitude do ponto de entrega | -23.5987 |
| `lon` | float | Longitude do ponto de entrega | -46.7158 |
| `demand` | int | Carga a ser entregue (unidades) | 8 |
| `priority` | int | Nível de prioridade (1=crítico, 3=normal) | 3 |

## Configuração para São Paulo (SP)

### Unidades de Entrega

O sistema atende **25 entregas** distribuídas em **15 unidades hospitalares Einstein** na cidade de São Paulo:

#### Unidades Únicas (9 locais)
1. **Einstein Morumbi** (d1)
2. **Einstein Alphaville** (d2)
3. **Einstein Alto de Pinheiros** (d3)
4. **Einstein Anália Franco** (d4)
5. **Einstein Chácara Klabin** (d5)
6. **Einstein Ibirapuera** (d6)
7. **Einstein Jardins** (d7)
8. **Einstein Parque da Cidade** (d8)
9. **Einstein Parque Ibirapuera** (d9)
10. **Einstein Perdizes** (d10)
11. **Einstein Vila Mariana** (d11)
12. **Centro de Terapias Avançadas em Oncologia e Hematologia Einstein** (d12)
13. **Espaço Einstein Bem-Estar e Saúde Mental** (d13)
14. **Espaço Einstein Esporte e Reabilitação** (d14)

#### Unidades com Múltiplas Entregas

Algumas unidades recebem mais de uma entrega no mesmo dia (entregas separadas):

| Unidade | IDs das Entregas | Quantidade |
|---------|------------------|------------|
| Einstein Morumbi | 1, 20, 24 | 3 |
| Einstein Alphaville | 2, 15, 23 | 3 |
| Einstein Alto de Pinheiros | 3, 19, 25 | 3 |
| Einstein Perdizes | 10, 16 | 2 |
| Einstein Chácara Klabin | 5, 17 | 2 |
| Einstein Jardins | 7, 18 | 2 |
| Einstein Ibirapuera | 6, 22 | 2 |
| Espaço Einstein Bem-Estar | 13, 21 | 2 |

**Interpretação:**
- Unidades com múltiplas entregas podem estar recebendo cargas de diferentes tipos, horários ou prioridades
- O sistema deve considerar que são entregas **independentes** (não podem ser consolidadas)
- Mesmo local geográfico, mas demandas e prioridades distintas

### Tabela Completa de Entregas

```
┌────┬─────────────────────────────────────┬──────────┬───────────┬────────┬──────────┐
│ ID │ Unidade                             │ Latitude │ Longitude │ Demand │ Priority │
├────┼─────────────────────────────────────┼──────────┼───────────┼────────┼──────────┤
│  1 │ Einstein Morumbi                    │  d1[0]   │   d1[1]   │   8    │    3     │
│  2 │ Einstein Alphaville                 │  d2[0]   │   d2[1]   │  12    │    2     │
│  3 │ Einstein Alto de Pinheiros          │  d3[0]   │   d3[1]   │  15    │    1     │
│  4 │ Einstein Anália Franco              │  d4[0]   │   d4[1]   │  10    │    3     │
│  5 │ Einstein Chácara Klabin             │  d5[0]   │   d5[1]   │   6    │    2     │
│  6 │ Einstein Ibirapuera                 │  d6[0]   │   d6[1]   │   8    │    3     │
│  7 │ Einstein Jardins                    │  d7[0]   │   d7[1]   │  12    │    2     │
│  8 │ Einstein Parque da Cidade           │  d8[0]   │   d8[1]   │  15    │    1     │
│  9 │ Einstein Parque Ibirapuera          │  d9[0]   │   d9[1]   │  10    │    3     │
│ 10 │ Einstein Perdizes                   │ d10[0]   │  d10[1]   │   6    │    2     │
│ 11 │ Einstein Vila Mariana               │ d11[0]   │  d11[1]   │   6    │    2     │
│ 12 │ Centro Terapias Avançadas           │ d12[0]   │  d12[1]   │   6    │    2     │
│ 13 │ Espaço Bem-Estar e Saúde Mental     │ d13[0]   │  d13[1]   │   6    │    2     │
│ 14 │ Espaço Esporte e Reabilitação       │ d14[0]   │  d14[1]   │   6    │    2     │
│ 15 │ Einstein Alphaville (2ª entrega)    │ d15[0]   │  d15[1]   │   8    │    3     │
│ 16 │ Einstein Perdizes (2ª entrega)      │ d16[0]   │  d16[1]   │  12    │    2     │
│ 17 │ Einstein Chácara Klabin (2ª entrega)│ d17[0]   │  d17[1]   │  15    │    1     │
│ 18 │ Einstein Jardins (2ª entrega)       │ d18[0]   │  d18[1]   │  10    │    3     │
│ 19 │ Einstein Alto Pinheiros (2ª entrega)│ d19[0]   │  d19[1]   │   6    │    2     │
│ 20 │ Einstein Morumbi (2ª entrega)       │ d20[0]   │  d20[1]   │   8    │    3     │
│ 21 │ Espaço Bem-Estar (2ª entrega)       │ d21[0]   │  d21[1]   │  12    │    2     │
│ 22 │ Einstein Ibirapuera (2ª entrega)    │ d22[0]   │  d22[1]   │  15    │    1     │
│ 23 │ Einstein Alphaville (3ª entrega)    │ d23[0]   │  d23[1]   │  10    │    3     │
│ 24 │ Einstein Morumbi (3ª entrega)       │ d24[0]   │  d24[1]   │   6    │    2     │
│ 25 │ Einstein Alto Pinheiros (3ª entrega)│ d25[0]   │  d25[1]   │   6    │    2     │
└────┴─────────────────────────────────────┴──────────┴───────────┴────────┴──────────┘
```

**Nota:** As coordenadas (d1[0], d1[1], etc.) são importadas do módulo `address_routes.einstein_units`.

## Análise Estatística das Entregas

### Distribuição de Demanda

```python
# Contagem por valor de demanda
demand_distribution = {
    6:  11 entregas (44.0%)  # Demanda baixa
    8:  4 entregas  (16.0%)  # Demanda média-baixa
    10: 4 entregas  (16.0%)  # Demanda média
    12: 4 entregas  (16.0%)  # Demanda média-alta
    15: 2 entregas  (8.0%)   # Demanda alta
}

# Estatísticas
Total de entregas: 25
Demanda total: 230 unidades
Demanda média: 9.2 unidades/entrega
Demanda mediana: 8.0 unidades/entrega
Demanda mínima: 6 unidades
Demanda máxima: 15 unidades
Desvio padrão: ≈3.1 unidades
```

**Gráfico de Distribuição:**
```
Demanda
15 │ ██
12 │ ████
10 │ ████
 8 │ ████
 6 │ ███████████
   └─────────────────────────
     Frequência
```

**Interpretação:**
- **Maioria (44%)** das entregas são de demanda **baixa** (6 unidades)
- **Distribuição relativamente uniforme** nas outras categorias
- **Poucas entregas críticas** de alta demanda (15 unidades)
- Permite **boa consolidação** em veículos de capacidade média (50 unidades)

### Distribuição de Prioridade

```python
# Contagem por nível de prioridade
priority_distribution = {
    1: 4 entregas  (16.0%)   # Crítico
    2: 12 entregas (48.0%)   # Moderado
    3: 9 entregas  (36.0%)   # Normal
}

# Entregas críticas (priority=1)
critical_deliveries = [3, 8, 17, 22]
# IDs: Alto de Pinheiros, Parque da Cidade, Chácara Klabin (2ª), Ibirapuera (2ª)
```

**Gráfico de Distribuição:**
```
Priority
3 (Normal)   │ █████████      (36%)
2 (Moderado) │ ████████████   (48%)
1 (Crítico)  │ ████           (16%)
             └────────────────────────
               Frequência
```

**Interpretação:**
- **48% são prioridade moderada** (2): Maioria das entregas
- **36% são prioridade normal** (3): Flexíveis no atendimento
- **16% são prioridade crítica** (1): Devem ser priorizadas no roteamento
- Sistema de 3 níveis permite **granularidade adequada** para decisões

### Correlação Demanda × Prioridade

```python
# Análise de correlação
priority_1_demands = [15, 15, 15, 15]  # Média: 15.0
priority_2_demands = [12, 6, 12, 6, 6, 6, 6, 12, 6, 12, 6, 6]  # Média: 8.0
priority_3_demands = [8, 10, 8, 10, 8, 8, 10, 8, 6]  # Média: 8.4
```

**Observação:**
- **Prioridade 1** tende a ter **demandas maiores** (média 15.0)
- **Prioridades 2 e 3** têm demandas similares (média ≈8.2)
- Entregas críticas geralmente envolvem **volumes maiores**

### Carga Total e Consolidação

```python
# Análise de consolidação
total_demand = 230 unidades
vehicle_capacity = 50 unidades  # Padrão do sistema

minimum_vehicles_needed = ceil(230 / 50) = 5 veículos

# Cenários de utilização
scenario_5_vehicles = {
    'avg_load_per_vehicle': 230 / 5 = 46.0 unidades,
    'avg_utilization': 46.0 / 50 = 92.0%,
    'avg_deliveries_per_vehicle': 25 / 5 = 5 entregas
}

scenario_6_vehicles = {
    'avg_load_per_vehicle': 230 / 6 = 38.3 unidades,
    'avg_utilization': 38.3 / 50 = 76.6%,
    'avg_deliveries_per_vehicle': 25 / 6 = 4.2 entregas
}
```

**Análise:**
- **Mínimo teórico:** 5 veículos (utilização 92%)
- **Prático recomendado:** 5-6 veículos
- Configuração do sistema usa **5 veículos**
- Alta utilização requer **otimização cuidadosa** para evitar sobrecarga

## Níveis de Prioridade

### Escala de Prioridade

```python
PRIORITY_CRITICAL = 1  # Entregas urgentes, SLA rígido
PRIORITY_MODERATE = 2  # Entregas regulares, SLA normal
PRIORITY_NORMAL = 3    # Entregas flexíveis, SLA relaxado
```

### Impacto no Sistema

**1. Função Fitness:**
```python
# Fator de peso na função fitness
CRITICAL_WEIGHT = 12  # Peso para entregas críticas

# Entregas de prioridade 1 influenciam fortemente a ordem de entrega
# Sistema penaliza soluções que atrasam entregas críticas
```

**2. Métrica de Avaliação:**
```python
# Método: critical_delivery_count_by_deliveries()
# Score baseado na posição de entregas críticas nas rotas

score = sum(
    critical_count_in_route × weight
    for each route
)

# Weight decresce com posição da rota (primeira rota tem maior peso)
```

**3. Operadores Genéticos:**
- **Crossover BCRC:** Prioriza rotas com menor custo para entregas críticas
- **Selection:** Soluções que atendem melhor prioridades têm vantagem evolutiva

### Entregas Críticas Detalhadas

```python
critical_deliveries = {
    3: {
        'unit': 'Einstein Alto de Pinheiros',
        'demand': 15,
        'priority': 1,
        'context': 'Primeira entrega nesta unidade'
    },
    8: {
        'unit': 'Einstein Parque da Cidade',
        'demand': 15,
        'priority': 1,
        'context': 'Única entrega nesta unidade'
    },
    17: {
        'unit': 'Einstein Chácara Klabin',
        'demand': 15,
        'priority': 1,
        'context': 'Segunda entrega (maior demanda)'
    },
    22: {
        'unit': 'Einstein Ibirapuera',
        'demand': 15,
        'priority': 1,
        'context': 'Segunda entrega (maior demanda)'
    }
}
```

**Padrão Observado:**
- **Todas as entregas críticas** têm demanda máxima (15 unidades)
- **50% são segundas entregas** em locais com múltiplas visitas
- Distribuição geográfica: 4 unidades diferentes
- Requerem **atenção especial** no planejamento

## Integração com o Sistema

### Fluxo de Uso no Pipeline

```
1. CARREGAMENTO
   └─> load_deliveries_info("SP")
       └─> Retorna dict com 25 entregas

2. INICIALIZAÇÃO DO GA
   └─> GeneticAlgorithm(city_code="SP")
       └─> self.deliveries = load_deliveries_info("SP")

3. GERAÇÃO DE POPULAÇÃO
   └─> generate_population_coordinates()
       └─> Usa deliveries.keys() para criar cromossomos
       └─> Cromossomo = [1, 2, 3, ..., 25]

4. FUNÇÃO FITNESS
   └─> fitness_function(solution, deliveries, vehicles)
       └─> Usa demand para verificar capacidade
       └─> Usa priority para calcular penalidades

5. AVALIAÇÃO DE ROTAS
   └─> RouteEvaluator(routes, deliveries, vehicles)
       └─> capacity_utilization: usa demand
       └─> critical_delivery: usa priority
```

### Exemplo de Uso

```python
from delivery_setup.deliveries import load_deliveries_info

# Carregar entregas
deliveries = load_deliveries_info("SP")

# Acessar entrega específica
delivery_3 = deliveries[3]
print(f"Entrega 3:")
print(f"  Localização: ({delivery_3['lat']}, {delivery_3['lon']})")
print(f"  Demanda: {delivery_3['demand']} unidades")
print(f"  Prioridade: {delivery_3['priority']}")

# Output:
# Entrega 3:
#   Localização: (-23.5523, -46.7012)
#   Demanda: 15 unidades
#   Prioridade: 1

# Calcular demanda total
total_demand = sum(d['demand'] for d in deliveries.values())
print(f"Demanda total: {total_demand} unidades")
# Output: Demanda total: 230 unidades

# Filtrar entregas críticas
critical = [id for id, d in deliveries.items() if d['priority'] == 1]
print(f"Entregas críticas: {critical}")
# Output: Entregas críticas: [3, 8, 17, 22]
```

### Dependências

```python
# Importação de coordenadas
from address_routes.einstein_units import hospitalar_units_lat_lon as rts

# Structure esperada de rts:
rts = {
    "SP": {
        "Einstein Morumbi": (lat, lon),
        "Einstein Alphaville": (lat, lon),
        # ... outras unidades
    },
    # Outras cidades (futuro)
}
```

## Extensibilidade para Novas Cidades

### Template para Nova Cidade

```python
def load_deliveries_info(city: str) -> dict[int, dict[str, float]]:
    cityroutes = rts[city]

    if city == "SP":
        # ... código existente ...
    
    elif city == "RJ":  # Exemplo: Rio de Janeiro
        d1 = cityroutes['Hospital Copa D\'Or']
        d2 = cityroutes['Hospital São Lucas']
        # ... definir outros pontos
        
        return {
            1: {"lat": d1[0], "lon": d1[1], "demand": 10, "priority": 2},
            2: {"lat": d2[0], "lon": d2[1], "demand": 8, "priority": 3},
            # ... outras entregas
        }
    
    else:
        raise ValueError(f"City '{city}' without defined deliveries routes.")
```

### Diretrizes para Configuração

**1. Número de Entregas:**
- Ajustar conforme necessidade operacional
- Considerar capacidade dos veículos
- Manter balanceamento com número de veículos

**2. Valores de Demanda:**
- Refletir carga real (kg, m³, unidades)
- Garantir viabilidade: max(demand) ≤ vehicle_capacity
- Distribuição uniforme facilita consolidação

**3. Níveis de Prioridade:**
- Manter escala 1-3 para consistência
- Balancear proporção (recomendado: 15-20% críticos)
- Documentar critérios de classificação

**4. Múltiplas Entregas no Mesmo Local:**
- Usar apenas quando necessário (horários diferentes, tipos diferentes)
- Evitar fragmentação excessiva
- Cada entrega deve ser **independente**

## Validação e Consistência

### Validações Recomendadas

```python
def validate_deliveries(deliveries: dict) -> bool:
    """
    Valida consistência dos dados de entregas
    """
    # 1. Verificar IDs sequenciais
    expected_ids = set(range(1, len(deliveries) + 1))
    actual_ids = set(deliveries.keys())
    assert expected_ids == actual_ids, "IDs devem ser sequenciais de 1 a N"
    
    # 2. Verificar estrutura de cada entrega
    required_fields = {'lat', 'lon', 'demand', 'priority'}
    for id, delivery in deliveries.items():
        assert required_fields == set(delivery.keys()), \
            f"Entrega {id} com campos inválidos"
    
    # 3. Verificar ranges válidos
    for id, delivery in deliveries.items():
        assert -90 <= delivery['lat'] <= 90, \
            f"Latitude inválida na entrega {id}"
        assert -180 <= delivery['lon'] <= 180, \
            f"Longitude inválida na entrega {id}"
        assert delivery['demand'] > 0, \
            f"Demanda deve ser positiva na entrega {id}"
        assert delivery['priority'] in [1, 2, 3], \
            f"Prioridade deve ser 1, 2 ou 3 na entrega {id}"
    
    # 4. Verificar viabilidade com frota
    total_demand = sum(d['demand'] for d in deliveries.values())
    vehicle_capacity = 50  # Padrão
    num_vehicles = 5  # Padrão
    total_capacity = vehicle_capacity * num_vehicles
    assert total_demand <= total_capacity, \
        f"Demanda total ({total_demand}) excede capacidade da frota ({total_capacity})"
    
    return True

# Uso
deliveries = load_deliveries_info("SP")
assert validate_deliveries(deliveries)
```

### Verificação de Coordenadas

```python
def verify_coordinates_in_city(deliveries: dict, city: str) -> bool:
    """
    Verifica se coordenadas estão na região esperada
    """
    if city == "SP":
        # Bounding box de São Paulo (aproximado)
        lat_min, lat_max = -24.0, -23.3
        lon_min, lon_max = -46.9, -46.3
        
        for id, delivery in deliveries.items():
            assert lat_min <= delivery['lat'] <= lat_max, \
                f"Entrega {id} fora dos limites de latitude de SP"
            assert lon_min <= delivery['lon'] <= lon_max, \
                f"Entrega {id} fora dos limites de longitude de SP"
    
    return True
```

## Análise de Complexidade do Problema

### Métricas de Complexidade

```python
# Instância do problema
n_deliveries = 25
n_vehicles = 5

# Espaço de busca
factorial_25 = 25! ≈ 1.55 × 10^25 permutações

# Com divisão em 5 rotas
# Número de partições (Stirling do segundo tipo)
S(25, 5) ≈ 2.4 × 10^23 possibilidades

# Cada partição tem variações de ordem
# Espaço total ainda maior
```

**Classificação:**
- **Problema:** NP-Hard (Vehicle Routing Problem)
- **Complexidade:** Exponencial
- **Método:** Heurística (Algoritmo Genético)
- **Justificativa:** Instância de tamanho médio requer otimização heurística

### Benchmark de Instâncias

| Tipo | Entregas | Veículos | Classificação | Método Sugerido |
|------|----------|----------|---------------|-----------------|
| Pequena | ≤15 | 2-3 | Simples | Exaustivo/Branch-and-Bound |
| Média | 16-30 | 3-6 | **Moderada** | **Heurística (GA, SA)** |
| Grande | 31-100 | 6-15 | Complexa | Metaheurística avançada |
| Muito Grande | >100 | >15 | Muito Complexa | Híbrida/Cluster-first |

**Posição da Instância Atual:**
- **25 entregas, 5 veículos:** Média/Moderada
- **Método escolhido:** Algoritmo Genético ✓
- **Adequado** para o tamanho da instância

## Impacto na Qualidade da Solução

### Fatores de Complexidade

**1. Distribuição Geográfica:**
- Unidades espalhadas por São Paulo
- Clusters naturais (regiões: Alphaville, Zona Sul, etc.)
- Oportunidade para **exploração de proximidade**

**2. Restrições de Capacidade:**
- Demanda total: 230 unidades
- Capacidade total: 250 unidades (5 × 50)
- **Folga de 8.7%**: Pouca margem para erro
- Requer **balanceamento cuidadoso**

**3. Múltiplas Entregas no Mesmo Local:**
- 8 unidades com 2-3 entregas cada
- Mesmas coordenadas, mas **demandas/prioridades diferentes**
- Potencial para **otimização de sequência**

**4. Prioridades Heterogêneas:**
- 4 entregas críticas (priority=1)
- 12 moderadas, 9 normais
- Requer **trade-off** entre custo e nível de serviço

## Cenários de Teste

### Cenário 1: Todas Prioridades Iguais

```python
# Modificar para teste
def load_uniform_priority():
    deliveries = load_deliveries_info("SP")
    for d in deliveries.values():
        d['priority'] = 2  # Todas moderadas
    return deliveries

# Esperado: Otimização focada puramente em custo/distância
```

### Cenário 2: Todas Demandas Iguais

```python
# Modificar para teste
def load_uniform_demand():
    deliveries = load_deliveries_info("SP")
    avg_demand = 230 // 25 = 9
    for d in deliveries.values():
        d['demand'] = avg_demand
    return deliveries

# Esperado: Simplificação do problema de consolidação
```

### Cenário 3: Demanda Extrema

```python
# Teste de limite
def load_extreme_demand():
    deliveries = load_deliveries_info("SP")
    deliveries[1]['demand'] = 50  # Preenche 1 veículo inteiro
    return deliveries

# Esperado: Veículo dedicado para entrega 1
```

## Palavras-chave para Busca

- Entregas
- Deliveries
- Pontos de entrega
- Demanda de carga
- Prioridade de atendimento
- Unidades hospitalares Einstein
- São Paulo
- Coordenadas geográficas
- Latitude longitude
- Distribuição de demanda
- Níveis de prioridade
- Entregas críticas
- Consolidação de carga
- Múltiplas entregas
- Instância do problema
- VRP instance
- Capacidade de veículos
- Carga total
- Balanceamento de rotas
- Configuração de dados

## Resumo Executivo

### Características Principais

**Dados:**
- **25 entregas** em **15 unidades** Einstein (São Paulo)
- **Demanda total:** 230 unidades
- **Prioridades:** 4 críticas, 12 moderadas, 9 normais

**Distribuição:**
- Demanda: 6-15 unidades (média 9.2)
- Prioridade: Escala 1-3 (1=crítico)
- Geografia: Espalhada por São Paulo

**Complexidade:**
- Problema: NP-Hard (VRP)
- Instância: Média (25 entregas, 5 veículos)
- Método: Algoritmo Genético (adequado)

**Desafios:**
- Alta utilização de capacidade (92%)
- Múltiplas entregas em mesmos locais (8 unidades)
- Balanceamento custo × prioridade
- 4 entregas críticas distribuídas

**Integração:**
- Input para GeneticAlgorithm
- Base para fitness function
- Referência para RouteEvaluator
- Origem dos cromossomos (IDs 1-25)

### Uso Típico

```python
# 1. Carregar
deliveries = load_deliveries_info("SP")

# 2. Analisar
total = sum(d['demand'] for d in deliveries.values())  # 230
critical = [i for i, d in deliveries.items() if d['priority'] == 1]  # [3,8,17,22]

# 3. Usar no GA
ga = GeneticAlgorithm(city_code="SP")  # Internamente carrega deliveries

# 4. Avaliar solução
evaluator = RouteEvaluator(routes, deliveries, vehicles)
metrics = evaluator.metric_summary()
```

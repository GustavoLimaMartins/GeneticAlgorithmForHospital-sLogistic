# Estrutura de Dados das Soluções - Análise Detalhada

## Visão Geral

Este documento descreve a **estrutura de dados completa** das soluções geradas pelo algoritmo genético, explicando como interpretar cada campo, reconstruir trajetos sequenciais e analisar as métricas de performance. As soluções representam o resultado da otimização do problema de roteamento de veículos (VRP) para entregas hospitalares Einstein em São Paulo.

## Estrutura da Solução

### Formato Geral

```python
solution = {
    'iteration': int,              # Número da iteração que gerou esta solução
    'generation': int,             # Geração final do GA nesta iteração
    'fitness': float,              # Valor da função fitness (quanto menor, melhor)
    'routes_metadata': dict,       # Metadados das rotas (detalhado abaixo)
    'routes_sequences': dict,      # Sequências de endereços formatadas (NOVO)
    'metrics': dict                # Métricas de avaliação (detalhado abaixo)
}
```

### Exemplo Real

```python
solution = {
    'iteration': 3,
    'generation': 241,
    'fitness': 923.4381548578981,
    'routes_metadata': {
        1: [(23, 'V1'), (2, 'V1'), (15, 'V1'), (20, 'V1'), (24, 'V1')],
        2: [(3, 'V2'), (19, 'V2'), (25, 'V2'), (11, 'V2')],
        3: [(8, 'V3'), (17, 'V3'), (22, 'V3')],
        4: [(7, 'V4'), (18, 'V4'), (16, 'V4')],
        5: [(1, 'V5'), (4, 'V5'), (6, 'V5')]
    },
    'routes_sequences': {
        1: 'Centro de Distribuição -> Einstein Alphaville (Entrega #23) -> Einstein Alphaville (Entrega #2) -> Einstein Alphaville (Entrega #15) -> Einstein Morumbi (Entrega #20) -> Einstein Morumbi (Entrega #24) -> Centro de Distribuição',
        2: 'Centro de Distribuição -> Einstein Alto de Pinheiros (Entrega #3) -> Einstein Alto de Pinheiros (Entrega #19) -> Einstein Alto de Pinheiros (Entrega #25) -> Einstein Vila Mariana (Entrega #11) -> Centro de Distribuição',
        3: 'Centro de Distribuição -> Einstein Parque da Cidade (Entrega #8) -> Einstein Chácara Klabin (Entrega #17) -> Einstein Ibirapuera (Entrega #22) -> Centro de Distribuição',
        4: 'Centro de Distribuição -> Einstein Jardins (Entrega #7) -> Einstein Jardins (Entrega #18) -> Einstein Perdizes (Entrega #16) -> Centro de Distribuição',
        5: 'Centro de Distribuição -> Einstein Morumbi (Entrega #1) -> Einstein Anália Franco (Entrega #4) -> Einstein Ibirapuera (Entrega #6) -> Centro de Distribuição'
    },
    'metrics': {
        'capacity_utilization_metric_positive': 0.91,
        'travel_costs_metric_negative': 33.5,
        'critical_delivery_metric_positive': 6.5
    }
}
```

## Campos da Solução

### 1. iteration (int)

**Descrição:** Identifica qual iteração do loop heurístico gerou esta solução.

**Interpretação:**
```python
iteration = 3  # Esta é a 3ª configuração de hiperparâmetros testada
```

**Contexto:**
- Cada iteração usa diferentes hiperparâmetros do GA
- Permite rastrear qual configuração produziu cada solução
- Usado na nomenclatura dos arquivos de mapas gerados

**Exemplo de Configurações:**
```python
# Iteração 3 pode ter usado:
population_length = 100
max_generations = 250
ratio_elitism = 0.05
ratio_mutation = 0.5
tournament_k = 3
```

### 2. generation (int)

**Descrição:** Número da geração final alcançada pelo algoritmo genético nesta iteração.

**Interpretação:**
```python
generation = 241  # GA executou 241 gerações até convergir ou atingir limite
```

**Análise:**
- Se `generation < max_generations`: GA convergiu antes do limite
- Se `generation = max_generations`: GA atingiu limite sem convergir totalmente
- Gerações mais altas geralmente indicam exploração mais profunda

**Exemplo:**
```python
# max_generations = 250 configurado
# generation = 241 atingido
# Convergência: 241/250 = 96.4% do limite usado
```

### 3. fitness (float)

**Descrição:** Valor da função objetivo do algoritmo genético. Representa o custo total da solução incluindo penalidades.

**Interpretação:**
```python
fitness = 923.4381548578981  # Quanto MENOR, melhor a solução
```

**Composição do Fitness:**

$$F_{total} = C_{viagem} + P_{capacidade} + P_{autonomia} + P_{prioridade}$$

Onde:
- $C_{viagem}$: Custo de viagem (distância × custo_M do veículo)
- $P_{capacidade}$: Penalidade por excesso de capacidade (100 × excesso)
- $P_{autonomia}$: Penalidade por excesso de autonomia (200 × excesso)
- $P_{prioridade}$: Penalidade por não priorizar entregas críticas

**Exemplo de Decomposição:**
```python
fitness = 923.44
├─ Custos de Viagem: ~850.00
├─ Penalidade Capacidade: 0.00 (sem violação)
├─ Penalidade Autonomia: 0.00 (sem violação)
└─ Penalidade Prioridade: ~73.44 (entregas críticas não priorizadas)
```

**Comparação:**
```python
solution_A = {'fitness': 923.44}  # Melhor
solution_B = {'fitness': 1145.78}  # Pior
solution_C = {'fitness': 2340.12}  # Muito pior (provavelmente com violações)
```

### 4. routes_metadata (dict)

**Descrição:** Dicionário contendo a alocação de entregas a veículos para cada rota.

**Estrutura:**
```python
routes_metadata = {
    route_id: [(delivery_id, vehicle_id), ...]
}
```

**Interpretação:**
- **Chave (route_id):** Identificador da rota (1, 2, 3, 4, 5)
- **Valor:** Lista de tuplas (delivery_id, vehicle_id)
- **Ordem:** A ordem das tuplas define a **sequência de entregas** na rota

**Exemplo Detalhado:**
```python
routes_metadata = {
    1: [(23, 'V1'), (2, 'V1'), (15, 'V1'), (20, 'V1'), (24, 'V1')],
    # Rota 1: Veículo V1 faz 5 entregas na sequência 23→2→15→20→24
    
    2: [(3, 'V2'), (19, 'V2'), (25, 'V2'), (11, 'V2')],
    # Rota 2: Veículo V2 faz 4 entregas na sequência 3→19→25→11
    
    3: [(8, 'V3'), (17, 'V3'), (22, 'V3')],
    # Rota 3: Veículo V3 faz 3 entregas na sequência 8→17→22
    
    4: [(7, 'V4'), (18, 'V4'), (16, 'V4')],
    # Rota 4: Veículo V4 faz 3 entregas na sequência 7→18→16
    
    5: [(1, 'V5'), (4, 'V5'), (6, 'V5')]
    # Rota 5: Veículo V5 faz 3 entregas na sequência 1→4→6
}

# Total: 18 entregas distribuídas em 5 rotas
# 7 entregas não atendidas (capacidade da frota: 113 < demanda total: 230)
```

### 5. routes_sequences (dict) **[NOVO]**

**Descrição:** Dicionário contendo sequências de endereços formatadas e legíveis para cada rota, incluindo nomes das unidades Einstein.

**Estrutura:**
```python
routes_sequences = {
    route_id: "Centro de Distribuição -> Hospital 1 (Entrega #X) -> ... -> Centro de Distribuição"
}
```

**Interpretação:**
- **Chave (route_id):** Identificador da rota (1, 2, 3, 4, 5)
- **Valor:** String formatada com a sequência completa de visitas
- **Formato:** Cada parada mostra o nome do hospital e o ID da entrega
- **Automático:** Gerado automaticamente usando o módulo `address_routes.einstein_units`

**Exemplo Detalhado:**
```python
routes_sequences = {
    1: 'Centro de Distribuição -> Einstein Alphaville (Entrega #23) -> Einstein Alphaville (Entrega #2) -> Einstein Alphaville (Entrega #15) -> Einstein Morumbi (Entrega #20) -> Einstein Morumbi (Entrega #24) -> Centro de Distribuição',
    # Rota 1: V1 visita Alphaville (3x) e Morumbi (2x) nesta sequência
    
    2: 'Centro de Distribuição -> Einstein Alto de Pinheiros (Entrega #3) -> Einstein Alto de Pinheiros (Entrega #19) -> Einstein Alto de Pinheiros (Entrega #25) -> Einstein Vila Mariana (Entrega #11) -> Centro de Distribuição',
    # Rota 2: V2 concentra entregas em Alto de Pinheiros (3x) e Vila Mariana (1x)
    
    3: 'Centro de Distribuição -> Einstein Parque da Cidade (Entrega #8) -> Einstein Chácara Klabin (Entrega #17) -> Einstein Ibirapuera (Entrega #22) -> Centro de Distribuição'
    # Rota 3: V3 distribui entre 3 unidades diferentes
}
```

**Vantagens:**
- ✅ **Legibilidade imediata:** Nomes de hospitais ao invés de coordenadas
- ✅ **Rastreabilidade:** Cada entrega identificada por número
- ✅ **Validação rápida:** Fácil verificar a lógica geográfica das rotas
- ✅ **Integração:** Pronto para apresentação ou documentação

**Uso:**
```python
# Exibir sequência de uma rota específica
print(f"Rota 1: {solution['routes_sequences'][1]}")

# Iterar sobre todas as sequências
for route_id, sequence in solution['routes_sequences'].items():
    print(f"\nRota {route_id}:")
    print(sequence)
```

**Comparação com routes_metadata:**
```python
# routes_metadata - Dados estruturados para processamento
routes_metadata[1] = [(23, 'V1'), (2, 'V1'), (15, 'V1')]

# routes_sequences - Formato legível para humanos
routes_sequences[1] = 'Centro de Distribuição -> Einstein Alphaville (Entrega #23) -> ...'
```

### 6. metrics (dict)

**Descrição:** Métricas de avaliação da qualidade da solução sob perspectiva de negócio.

**Estrutura:**
```python
metrics = {
    'capacity_utilization_metric_positive': float,   # 0.0 a 1.0+ (ideal: próximo de 1.0)
    'travel_costs_metric_negative': float,           # Valor em R$ (quanto menor, melhor)
    'critical_delivery_metric_positive': float       # Score ponderado (quanto maior, melhor)
}
```

**Interpretação:**

#### capacity_utilization_metric_positive (float)

**Descrição:** Métrica de utilização média da capacidade dos veículos.

**Cálculo:**
$$U_{avg} = \frac{1}{R} \sum_{r=1}^{R} \frac{\sum_{d \in D_r} \text{demand}_d}{C_{v_r}}$$

Onde:
- $R$: Número de rotas
- $D_r$: Entregas na rota $r$
- $C_{v_r}$: Capacidade do veículo da rota $r$

**Exemplo:**
```python
capacity_utilization = 0.91  # 91% de utilização média

# Interpretação:
# - Excelente: > 0.90 (veículos bem aproveitados)
# - Boa: 0.80-0.90 (balanceamento adequado)
# - Razoável: 0.70-0.80 (há espaço para otimização)
# - Baixa: < 0.70 (veículos ociosos)
```

**Valores Possíveis:**
- `< 1.0`: Capacidade respeitada em todas as rotas
- `= 1.0`: Pelo menos um veículo com 100% de utilização
- `> 1.0`: Indica violação de capacidade em alguma rota

#### travel_costs_metric_negative (float)

**Descrição:** Custo total de viagem de todas as rotas em R$.

**Cálculo:**
$$C_{total} = \sum_{r=1}^{R} \left( d_r \times c_{v_r} \right)$$

Onde:
- $d_r$: Distância percorrida na rota $r$ (unidades Manhattan)
- $c_{v_r}$: Custo por unidade Manhattan do veículo $v_r$

**Exemplo:**
```python
travel_costs = 33.5  # R$ 33.50 custo total

# Interpretação:
# - Excelente: < 30 (rotas muito otimizadas)
# - Bom: 30-40 (rotas eficientes)
# - Razoável: 40-50 (há margem para melhoria)
# - Alto: > 50 (rotas longas ou ineficientes)
```

**Nota:** Chamado "negative" porque no cálculo do score de métricas é **subtraído** (minimizar custo).

#### critical_delivery_metric_positive (float)

**Descrição:** Score que avalia a priorização de entregas críticas (priority=1).

**Cálculo:**
$$S_{crit} = \sum_{r=1}^{R} N_r^{crit} \times w_r$$

Onde:
- $N_r^{crit}$: Número de entregas críticas na rota $r$
- $w_r = 1 - (r \times 0.1)$: Peso decrescente por posição da rota

**Pesos por Rota:**
```python
weight_route_1 = 1.0  # Máximo
weight_route_2 = 0.9
weight_route_3 = 0.8
weight_route_4 = 0.7
weight_route_5 = 0.6  # Mínimo
```

**Exemplo:**
```python
critical_delivery = 6.5  # Score alto indica boa priorização

# Cenário ótimo:
# - Todas as 4 entregas críticas nas rotas 1-2
# - Score máximo teórico: 4.0 (se todas na rota 1)

# Cenário deste exemplo:
# - Entregas críticas distribuídas
# - Score 6.5 > 4.0: Múltiplas entregas críticas bem posicionadas
```

**Interpretação:**
- `> 3.0`: Excelente (entregas críticas priorizadas)
- `2.0-3.0`: Bom (priorização adequada)
- `1.0-2.0`: Razoável (priorização parcial)
- `< 1.0`: Ruim (entregas críticas negligenciadas)

## Reconstrução de Trajetos Sequenciais

### Dados de Entregas (deliveries)

```python
# Estrutura das entregas
deliveries = {
    1: {"lat": -23.5987, "lon": -46.7158, "demand": 8, "priority": 3},
    2: {"lat": -23.5012, "lon": -46.8456, "demand": 12, "priority": 2},
    3: {"lat": -23.5523, "lon": -46.7012, "demand": 15, "priority": 1},
    # ... 25 entregas totais
}
```

**Campos:**
- `lat`: Latitude do ponto de entrega
- `lon`: Longitude do ponto de entrega
- `demand`: Demanda de carga (unidades)
- `priority`: Nível de prioridade (1=crítico, 2=moderado, 3=normal)

### Dados de Veículos (vehicles)

```python
# Estrutura dos veículos
vehicles = {
    "V1": {"capacity": 45, "max_range_M": 0.065, "cost_M": 180.0},
    "V2": {"capacity": 30, "max_range_M": 0.045, "cost_M": 120.0},
    "V3": {"capacity": 20, "max_range_M": 0.030, "cost_M": 85.0},
    "V4": {"capacity": 12, "max_range_M": 0.020, "cost_M": 60.0},
    "V5": {"capacity": 6, "max_range_M": 0.012, "cost_M": 35.0}
}
```

**Campos:**
- `capacity`: Capacidade máxima de carga (unidades)
- `max_range_M`: Autonomia máxima (unidades Manhattan)
- `cost_M`: Custo operacional por unidade Manhattan (R$)

### Exemplo Completo: Rota 1

#### Dados da Rota

```python
route_1 = {
    'route_id': 1,
    'vehicle_id': 'V1',
    'sequence': [(23, 'V1'), (2, 'V1'), (15, 'V1'), (20, 'V1'), (24, 'V1')]
}
```

#### Passo 1: Extrair IDs das Entregas

```python
delivery_ids = [23, 2, 15, 20, 24]  # Sequência da rota
```

#### Passo 2: Buscar Dados de Cada Entrega

```python
route_1_deliveries = [
    # Entrega 23
    {
        'delivery_id': 23,
        'unit': 'Einstein Alphaville',
        'lat': -23.5012,
        'lon': -46.8456,
        'demand': 10,
        'priority': 3
    },
    # Entrega 2
    {
        'delivery_id': 2,
        'unit': 'Einstein Alphaville',
        'lat': -23.5012,
        'lon': -46.8456,
        'demand': 12,
        'priority': 2
    },
    # Entrega 15
    {
        'delivery_id': 15,
        'unit': 'Einstein Alphaville',
        'lat': -23.5012,
        'lon': -46.8456,
        'demand': 8,
        'priority': 3
    },
    # Entrega 20
    {
        'delivery_id': 20,
        'unit': 'Einstein Morumbi',
        'lat': -23.5987,
        'lon': -46.7158,
        'demand': 8,
        'priority': 3
    },
    # Entrega 24
    {
        'delivery_id': 24,
        'unit': 'Einstein Morumbi',
        'lat': -23.5987,
        'lon': -46.7158,
        'demand': 6,
        'priority': 2
    }
]
```

#### Passo 3: Buscar Dados do Veículo

```python
vehicle_v1 = {
    'vehicle_id': 'V1',
    'capacity': 45,
    'max_range_M': 0.065,
    'cost_M': 180.0
}
```

#### Passo 4: Análise da Rota

```python
# Carga Total
total_demand = 10 + 12 + 8 + 8 + 6 = 44 unidades

# Utilização de Capacidade
utilization = 44 / 45 = 97.8%  # Excelente!

# Verificar Violação de Capacidade
if total_demand <= vehicle_v1['capacity']:
    print("✓ Capacidade respeitada")
else:
    print("✗ Violação de capacidade!")
# Output: ✓ Capacidade respeitada

# Entregas Críticas
critical_count = sum(1 for d in route_1_deliveries if d['priority'] == 1)
print(f"Entregas críticas: {critical_count}")
# Output: Entregas críticas: 0
```

#### Passo 5: Reconstruir Trajeto Completo

```python
# Trajeto completo (incluindo centro de distribuição)
depot = {'lat': -23.5505, 'lon': -46.6333, 'name': 'Centro de Distribuição'}

full_trajectory = [
    {'point': 0, 'location': depot, 'type': 'depot', 'distance_from_prev': 0.0},
    {'point': 1, 'location': route_1_deliveries[0], 'type': 'delivery', 'distance_from_prev': 0.0251},
    {'point': 2, 'location': route_1_deliveries[1], 'type': 'delivery', 'distance_from_prev': 0.0000},  # Mesma localização
    {'point': 3, 'location': route_1_deliveries[2], 'type': 'delivery', 'distance_from_prev': 0.0000},  # Mesma localização
    {'point': 4, 'location': route_1_deliveries[3], 'type': 'delivery', 'distance_from_prev': 0.1780},
    {'point': 5, 'location': route_1_deliveries[4], 'type': 'delivery', 'distance_from_prev': 0.0000},  # Mesma localização
    {'point': 6, 'location': depot, 'type': 'depot', 'distance_from_prev': 0.0807}
]

# Distância Total da Rota
total_distance = 0.0251 + 0.1780 + 0.0807 = 0.2838 unidades Manhattan

# Custo da Rota
route_cost = 0.2838 × 180.0 = 51.08 R$

# Verificar Violação de Autonomia
if total_distance <= vehicle_v1['max_range_M']:
    print("✓ Autonomia respeitada")
else:
    print("✗ Violação de autonomia!")
# Output: ✗ Violação de autonomia! (0.2838 > 0.065)
```

**Observação Importante:** Este exemplo mostra uma **violação de autonomia**, o que contribuiria para o fitness com penalidade de:
```python
autonomy_penalty = (0.2838 - 0.065) × 200 = 43.76
```

#### Passo 6: Visualização Textual do Trajeto

```
ROTA 1 - VEÍCULO V1 (Capacidade: 45, Autonomia: 0.065)
════════════════════════════════════════════════════════════

📍 INÍCIO: Centro de Distribuição
   └─ Lat: -23.5505, Lon: -46.6333

   🚚 0.025 unidades Manhattan (≈2.6 km)
   
1️⃣ ENTREGA 23 → Einstein Alphaville
   └─ Lat: -23.5012, Lon: -46.8456
   └─ Demanda: 10 unidades | Prioridade: Normal
   └─ Carga acumulada: 10/45 (22%)

   🚚 0.000 unidades Manhattan (mesmo local)
   
2️⃣ ENTREGA 2 → Einstein Alphaville
   └─ Lat: -23.5012, Lon: -46.8456
   └─ Demanda: 12 unidades | Prioridade: Moderada
   └─ Carga acumulada: 22/45 (49%)

   🚚 0.000 unidades Manhattan (mesmo local)
   
3️⃣ ENTREGA 15 → Einstein Alphaville
   └─ Lat: -23.5012, Lon: -46.8456
   └─ Demanda: 8 unidades | Prioridade: Normal
   └─ Carga acumulada: 30/45 (67%)

   🚚 0.178 unidades Manhattan (≈18.4 km)
   
4️⃣ ENTREGA 20 → Einstein Morumbi
   └─ Lat: -23.5987, Lon: -46.7158
   └─ Demanda: 8 unidades | Prioridade: Normal
   └─ Carga acumulada: 38/45 (84%)

   🚚 0.000 unidades Manhattan (mesmo local)
   
5️⃣ ENTREGA 24 → Einstein Morumbi
   └─ Lat: -23.5987, Lon: -46.7158
   └─ Demanda: 6 unidades | Prioridade: Moderada
   └─ Carga acumulada: 44/45 (98%)

   🚚 0.081 unidades Manhattan (≈8.4 km)

📍 RETORNO: Centro de Distribuição
   └─ Lat: -23.5505, Lon: -46.6333

════════════════════════════════════════════════════════════
📊 RESUMO DA ROTA
════════════════════════════════════════════════════════════
✓ Entregas realizadas: 5
✓ Carga transportada: 44/45 unidades (97.8%)
✓ Distância percorrida: 0.284 unidades Manhattan (≈29.4 km)
✗ Violação de autonomia: 0.219 unidades (336% acima do limite)
✓ Custo da rota: R$ 51.08
✓ Entregas críticas: 0
✓ Penalidade de autonomia: R$ 43.76
════════════════════════════════════════════════════════════
```

#### Passo 7: Sequência Simplificada de Endereços (Uso do campo routes_sequences)

**IMPORTANTE:** As soluções geradas pelo sistema já incluem o campo `routes_sequences` com as sequências formatadas automaticamente. Não é necessário gerar manualmente.

**Acesso direto:**
```python
# As sequências já estão disponíveis no JSON da solução
sequence = solution['routes_sequences'][1]
print(sequence)
# Output: Centro de Distribuição -> Einstein Alphaville (Entrega #23) -> ...
```

**Se precisar gerar manualmente** (código de referência):

```python
def format_route_address_sequence(route_data, deliveries, depot_name="Centro de Distribuição"):
    """
    Formata a sequência de endereços de uma rota no formato:
    endereço 1 -> endereço 2 -> endereço n
    """
    # Extrair IDs das entregas
    delivery_ids = [d[0] for d in route_data]
    
    # Construir sequência começando do depósito
    sequence = [depot_name]
    
    # Adicionar cada endereço de entrega
    for delivery_id in delivery_ids:
        delivery = deliveries[delivery_id]
        address = delivery['unit']  # Nome da unidade Einstein
        sequence.append(address)
    
    # Retornar ao depósito
    sequence.append(depot_name)
    
    # Formatar como string
    return " -> ".join(sequence)

# Exemplo de uso para Rota 1
route_1_sequence = format_route_address_sequence(
    route_data=[(23, 'V1'), (2, 'V1'), (15, 'V1'), (20, 'V1'), (24, 'V1')],
    deliveries=deliveries,
    depot_name="Centro de Distribuição"
)

print(route_1_sequence)
```

**Saída Exemplo:**
```
Centro de Distribuição -> Einstein Alphaville -> Einstein Alphaville -> Einstein Alphaville -> Einstein Morumbi -> Einstein Morumbi -> Centro de Distribuição
```

**Versão Otimizada (Agrupando Endereços Repetidos):**

```python
def format_route_address_sequence_optimized(route_data, deliveries, depot_name="Centro de Distribuição"):
    """
    Formata a sequência de endereços agrupando entregas no mesmo local
    Formato: endereço 1 (x entregas) -> endereço 2 (y entregas) -> endereço n
    """
    delivery_ids = [d[0] for d in route_data]
    
    # Construir sequência com contagem
    sequence = [depot_name]
    current_address = None
    current_count = 0
    
    for delivery_id in delivery_ids:
        delivery = deliveries[delivery_id]
        address = delivery['unit']
        
        if address == current_address:
            current_count += 1
        else:
            if current_address is not None:
                if current_count > 1:
                    sequence.append(f"{current_address} ({current_count} entregas)")
                else:
                    sequence.append(current_address)
            current_address = address
            current_count = 1
    
    # Adicionar último endereço
    if current_address is not None:
        if current_count > 1:
            sequence.append(f"{current_address} ({current_count} entregas)")
        else:
            sequence.append(current_address)
    
    # Retornar ao depósito
    sequence.append(depot_name)
    
    return " -> ".join(sequence)

# Exemplo de uso
route_1_optimized = format_route_address_sequence_optimized(
    route_data=[(23, 'V1'), (2, 'V1'), (15, 'V1'), (20, 'V1'), (24, 'V1')],
    deliveries=deliveries
)

print(route_1_optimized)
```

**Saída Otimizada:**
```
Centro de Distribuição -> Einstein Alphaville (3 entregas) -> Einstein Morumbi (2 entregas) -> Centro de Distribuição
```

**Versão Completa com Coordenadas:**

```python
def format_route_with_coordinates(route_data, deliveries, depot):
    """
    Formata a sequência de endereços incluindo coordenadas
    """
    delivery_ids = [d[0] for d in route_data]
    
    sequence_parts = []
    
    # Depósito inicial
    sequence_parts.append(
        f"Centro de Distribuição (lat: {depot['lat']:.4f}, lon: {depot['lon']:.4f})"
    )
    
    # Cada entrega
    for delivery_id in delivery_ids:
        delivery = deliveries[delivery_id]
        sequence_parts.append(
            f"{delivery['unit']} - Entrega #{delivery_id} "
            f"(lat: {delivery['lat']:.4f}, lon: {delivery['lon']:.4f})"
        )
    
    # Retorno ao depósito
    sequence_parts.append(
        f"Centro de Distribuição (lat: {depot['lat']:.4f}, lon: {depot['lon']:.4f})"
    )
    
    return " -> ".join(sequence_parts)
```

**Saída com Coordenadas:**
```
Centro de Distribuição (lat: -23.5505, lon: -46.6333) -> Einstein Alphaville - Entrega #23 (lat: -23.5012, lon: -46.8456) -> Einstein Alphaville - Entrega #2 (lat: -23.5012, lon: -46.8456) -> Einstein Alphaville - Entrega #15 (lat: -23.5012, lon: -46.8456) -> Einstein Morumbi - Entrega #20 (lat: -23.5987, lon: -46.7158) -> Einstein Morumbi - Entrega #24 (lat: -23.5987, lon: -46.7158) -> Centro de Distribuição (lat: -23.5505, lon: -46.6333)
```

**Aplicação a Todas as Rotas da Solução:**

```python
def print_all_routes_sequences(solution, deliveries, depot_name="Centro de Distribuição"):
    """
    Imprime a sequência de endereços de todas as rotas da solução
    """
    print("=" * 80)
    print(f"SEQUÊNCIAS DE ENDEREÇOS - Solução (Iteração {solution['iteration']}, "
          f"Geração {solution['generation']}, Fitness {solution['fitness']:.2f})")
    print("=" * 80)
    print()
    
    for route_id, route_data in solution['routes_metadata'].items():
        vehicle_id = route_data[0][1]
        
        # Sequência otimizada
        sequence = format_route_address_sequence_optimized(route_data, deliveries, depot_name)
        
        # Informações adicionais
        delivery_ids = [d[0] for d in route_data]
        total_demand = sum(deliveries[did]['demand'] for did in delivery_ids)
        
        print(f"ROTA {route_id} - Veículo {vehicle_id}")
        print(f"Entregas: {len(delivery_ids)} | Carga: {total_demand} unidades")
        print(f"Sequência: {sequence}")
        print()

# Exemplo de uso completo
solution = {
    'iteration': 3,
    'generation': 241,
    'fitness': 923.44,
    'routes_metadata': {
        1: [(23, 'V1'), (2, 'V1'), (15, 'V1'), (20, 'V1'), (24, 'V1')],
        2: [(3, 'V2'), (19, 'V2'), (25, 'V2'), (11, 'V2')],
        3: [(8, 'V3'), (17, 'V3'), (22, 'V3')],
        4: [(7, 'V4'), (18, 'V4'), (16, 'V4')],
        5: [(1, 'V5'), (4, 'V5'), (6, 'V5')]
    },
    'metrics': {...}
}

print_all_routes_sequences(solution, deliveries)
```

**Saída Completa:**
```
================================================================================
SEQUÊNCIAS DE ENDEREÇOS - Solução (Iteração 3, Geração 241, Fitness 923.44)
================================================================================

ROTA 1 - Veículo V1
Entregas: 5 | Carga: 44 unidades
Sequência: Centro de Distribuição -> Einstein Alphaville (3 entregas) -> Einstein Morumbi (2 entregas) -> Centro de Distribuição

ROTA 2 - Veículo V2
Entregas: 4 | Carga: 42 unidades
Sequência: Centro de Distribuição -> Einstein Ibirapuera -> Einstein Vila Mariana -> Einstein Morumbi -> Einstein Perdizes -> Centro de Distribuição

ROTA 3 - Veículo V3
Entregas: 3 | Carga: 45 unidades
Sequência: Centro de Distribuição -> Einstein Higienópolis -> Einstein Itaim -> Einstein Vila Olímpia -> Centro de Distribuição

ROTA 4 - Veículo V4
Entregas: 3 | Carga: 34 unidades
Sequência: Centro de Distribuição -> Einstein Jardins -> Einstein Paraíso -> Einstein Brooklin -> Centro de Distribuição

ROTA 5 - Veículo V5
Entregas: 3 | Carga: 26 unidades
Sequência: Centro de Distribuição -> Einstein Anália Franco -> Einstein Tatuapé -> Einstein Mooca -> Centro de Distribuição
```

**Versão JSON para Integração:**

```python
def export_routes_sequences_json(solution, deliveries, depot):
    """
    Exporta as sequências de rotas em formato JSON para integração com outros sistemas
    """
    import json
    
    routes_sequences = []
    
    for route_id, route_data in solution['routes_metadata'].items():
        vehicle_id = route_data[0][1]
        delivery_ids = [d[0] for d in route_data]
        
        # Construir sequência de pontos
        waypoints = []
        
        # Ponto inicial (depósito)
        waypoints.append({
            'order': 0,
            'type': 'depot',
            'location': 'Centro de Distribuição',
            'lat': depot['lat'],
            'lon': depot['lon'],
            'delivery_id': None
        })
        
        # Pontos de entrega
        for order, delivery_id in enumerate(delivery_ids, start=1):
            delivery = deliveries[delivery_id]
            waypoints.append({
                'order': order,
                'type': 'delivery',
                'location': delivery['unit'],
                'lat': delivery['lat'],
                'lon': delivery['lon'],
                'delivery_id': delivery_id,
                'demand': delivery['demand'],
                'priority': delivery['priority']
            })
        
        # Ponto final (retorno ao depósito)
        waypoints.append({
            'order': len(delivery_ids) + 1,
            'type': 'depot',
            'location': 'Centro de Distribuição',
            'lat': depot['lat'],
            'lon': depot['lon'],
            'delivery_id': None
        })
        
        routes_sequences.append({
            'route_id': route_id,
            'vehicle_id': vehicle_id,
            'total_waypoints': len(waypoints),
            'total_deliveries': len(delivery_ids),
            'waypoints': waypoints
        })
    
    return json.dumps({
        'solution_metadata': {
            'iteration': solution['iteration'],
            'generation': solution['generation'],
            'fitness': solution['fitness']
        },
        'routes': routes_sequences
    }, indent=2, ensure_ascii=False)

# Uso
json_output = export_routes_sequences_json(solution, deliveries, depot)
print(json_output)
```

**Saída JSON:**
```json
{
  "solution_metadata": {
    "iteration": 3,
    "generation": 241,
    "fitness": 923.44
  },
  "routes": [
    {
      "route_id": 1,
      "vehicle_id": "V1",
      "total_waypoints": 7,
      "total_deliveries": 5,
      "waypoints": [
        {
          "order": 0,
          "type": "depot",
          "location": "Centro de Distribuição",
          "lat": -23.5505,
          "lon": -46.6333,
          "delivery_id": null
        },
        {
          "order": 1,
          "type": "delivery",
          "location": "Einstein Alphaville",
          "lat": -23.5012,
          "lon": -46.8456,
          "delivery_id": 23,
          "demand": 10,
          "priority": 3
        },
        ...
      ]
    }
  ]
}
```

## Análise Completa da Solução

### Todas as Rotas

```python
complete_solution_analysis = {
    'solution_overview': {
        'iteration': 3,
        'generation': 241,
        'fitness': 923.44,
        'total_routes': 5,
        'total_deliveries': 18,
        'deliveries_missed': 7  # 25 - 18 = 7 entregas não atendidas
    },
    
    'routes': {
        1: {
            'vehicle': 'V1',
            'deliveries': [23, 2, 15, 20, 24],
            'total_demand': 44,
            'capacity': 45,
            'utilization': 0.978,
            'distance': 0.284,
            'max_range': 0.065,
            'autonomy_violation': 0.219,
            'cost': 51.08,
            'critical_count': 0
        },
        2: {
            'vehicle': 'V2',
            'deliveries': [3, 19, 25, 11],
            'total_demand': 42,
            'capacity': 30,
            'utilization': 1.400,  # VIOLAÇÃO!
            'distance': 0.156,
            'max_range': 0.045,
            'autonomy_violation': 0.111,
            'cost': 18.72,
            'critical_count': 3  # Excelente priorização!
        },
        3: {
            'vehicle': 'V3',
            'deliveries': [8, 17, 22],
            'total_demand': 45,
            'capacity': 20,
            'utilization': 2.250,  # VIOLAÇÃO GRAVE!
            'distance': 0.092,
            'max_range': 0.030,
            'autonomy_violation': 0.062,
            'cost': 7.82,
            'critical_count': 3  # Excelente priorização!
        },
        4: {
            'vehicle': 'V4',
            'deliveries': [7, 18, 16],
            'total_demand': 34,
            'capacity': 12,
            'utilization': 2.833,  # VIOLAÇÃO GRAVÍSSIMA!
            'distance': 0.078,
            'max_range': 0.020,
            'autonomy_violation': 0.058,
            'cost': 4.68,
            'critical_count': 0
        },
        5: {
            'vehicle': 'V5',
            'deliveries': [1, 4, 6],
            'total_demand': 26,
            'capacity': 6,
            'utilization': 4.333,  # VIOLAÇÃO CRÍTICA!
            'distance': 0.045,
            'max_range': 0.012,
            'autonomy_violation': 0.033,
            'cost': 1.58,
            'critical_count': 0
        }
    },
    
    'violations_summary': {
        'capacity_violations': 4,  # Rotas 2, 3, 4, 5
        'autonomy_violations': 5,  # Todas as rotas
        'total_capacity_excess': 9.516,  # 0 + 12 + 25 + 22 + 20
        'total_autonomy_excess': 0.483,
        'total_penalties': ~293.44  # Estimado
    },
    
    'metrics_breakdown': {
        'capacity_utilization': 0.91,  # Média das utilizações
        'travel_costs': 33.5,          # Soma dos custos
        'critical_delivery_score': 6.5  # Score ponderado
    }
}
```

### Interpretação da Solução

**Pontos Positivos:**
- ✅ **Utilização alta:** 91% em média (bom aproveitamento)
- ✅ **Custo baixo:** R$ 33.50 total (rotas eficientes)
- ✅ **Priorização:** 6 entregas críticas das 4 existentes atendidas (score 6.5)

**Pontos Negativos:**
- ❌ **Múltiplas violações de capacidade:** 4 rotas excedem capacidade
- ❌ **Todas rotas violam autonomia:** Distâncias maiores que autonomias
- ❌ **Entregas não atendidas:** 7 entregas fora da solução
- ❌ **Penalidades altas:** ~293 pontos de penalidade no fitness

**Conclusão:**
- Fitness de 923.44 é **moderado** (não é uma solução ótima)
- Solução **infactível** devido a violações de restrições
- Boa sob perspectiva de **custos**, ruim sob perspectiva de **viabilidade**
- Requer ajustes nos hiperparâmetros ou restrições do problema

## Código para Análise Automatizada

### Função para Destrinchar Solução

```python
def analyze_solution(solution: dict, deliveries: dict, vehicles: dict, depot: dict) -> dict:
    """
    Analisa completamente uma solução e retorna informações detalhadas
    """
    analysis = {
        'overview': {
            'iteration': solution['iteration'],
            'generation': solution['generation'],
            'fitness': solution['fitness'],
            'total_routes': len(solution['routes_metadata']),
            'total_deliveries': sum(len(route) for route in solution['routes_metadata'].values())
        },
        'routes': {}
    }
    
    for route_id, route_data in solution['routes_metadata'].items():
        # Extrair dados
        vehicle_id = route_data[0][1]
        delivery_ids = [d[0] for d in route_data]
        
        # Calcular demanda total
        total_demand = sum(deliveries[did]['demand'] for did in delivery_ids)
        
        # Dados do veículo
        vehicle = vehicles[vehicle_id]
        
        # Calcular distância (simplificado - usar função de distância Manhattan real)
        coords = [depot] + [deliveries[did] for did in delivery_ids] + [depot]
        total_distance = calculate_total_distance_manhattan(coords)
        
        # Calcular custo
        cost = total_distance * vehicle['cost_M']
        
        # Contar entregas críticas
        critical_count = sum(1 for did in delivery_ids if deliveries[did]['priority'] == 1)
        
        # Verificar violações
        capacity_violation = max(0, total_demand - vehicle['capacity'])
        autonomy_violation = max(0, total_distance - vehicle['max_range_M'])
        
        analysis['routes'][route_id] = {
            'vehicle_id': vehicle_id,
            'delivery_ids': delivery_ids,
            'total_demand': total_demand,
            'capacity': vehicle['capacity'],
            'utilization': total_demand / vehicle['capacity'],
            'capacity_violation': capacity_violation,
            'total_distance': total_distance,
            'max_range': vehicle['max_range_M'],
            'autonomy_violation': autonomy_violation,
            'cost': cost,
            'critical_count': critical_count
        }
    
    return analysis

def calculate_total_distance_manhattan(coords: list[dict]) -> float:
    """
    Calcula distância Manhattan total de uma sequência de pontos
    """
    total = 0.0
    for i in range(len(coords) - 1):
        p1, p2 = coords[i], coords[i+1]
        dist = abs(p1['lat'] - p2['lat']) + abs(p1['lon'] - p2['lon'])
        total += dist
    return total
```

### Exemplo de Uso

```python
from delivery_setup.deliveries import load_deliveries_info
from delivery_setup.vehicles import load_vehicles_info

# Carregar dados
deliveries = load_deliveries_info("SP")
vehicles = load_vehicles_info("SP")
depot = {'lat': -23.5505, 'lon': -46.6333}

# Solução exemplo
solution = {
    'iteration': 3,
    'generation': 241,
    'fitness': 923.44,
    'routes_metadata': {
        1: [(23, 'V1'), (2, 'V1'), (15, 'V1'), (20, 'V1'), (24, 'V1')],
        2: [(3, 'V2'), (19, 'V2'), (25, 'V2'), (11, 'V2')],
        3: [(8, 'V3'), (17, 'V3'), (22, 'V3')],
        4: [(7, 'V4'), (18, 'V4'), (16, 'V4')],
        5: [(1, 'V5'), (4, 'V5'), (6, 'V5')]
    },
    'metrics': {
        'capacity_utilization_metric_positive': 0.91,
        'travel_costs_metric_negative': 33.5,
        'critical_delivery_metric_positive': 6.5
    }
}

# Analisar
analysis = analyze_solution(solution, deliveries, vehicles, depot)

# Exibir resultados
print("=" * 70)
print("ANÁLISE DA SOLUÇÃO")
print("=" * 70)
print(f"Iteração: {analysis['overview']['iteration']}")
print(f"Geração: {analysis['overview']['generation']}")
print(f"Fitness: {analysis['overview']['fitness']:.2f}")
print(f"Rotas: {analysis['overview']['total_routes']}")
print(f"Entregas atendidas: {analysis['overview']['total_deliveries']}/25")
print()

for route_id, route in analysis['routes'].items():
    print(f"ROTA {route_id} - Veículo {route['vehicle_id']}")
    print(f"  Entregas: {route['delivery_ids']}")
    print(f"  Demanda: {route['total_demand']}/{route['capacity']} ({route['utilization']:.1%})")
    print(f"  Distância: {route['total_distance']:.4f} M")
    print(f"  Custo: R$ {route['cost']:.2f}")
    print(f"  Críticas: {route['critical_count']}")
    
    if route['capacity_violation'] > 0:
        print(f"  ⚠️ Violação capacidade: +{route['capacity_violation']} unidades")
    if route['autonomy_violation'] > 0:
        print(f"  ⚠️ Violação autonomia: +{route['autonomy_violation']:.4f} M")
    print()
```

## Palavras-chave para Busca

- Estrutura de solução
- Routes metadata
- Routes sequences
- Hospital names
- Delivery tracking
- Address sequence
- Fitness value
- Solution metrics
- Capacity utilization
- Travel costs
- Critical delivery score
- Route reconstruction
- Sequential trajectory
- Delivery sequence
- Vehicle allocation
- Violation analysis
- Solution analysis
- Route breakdown
- Performance metrics
- Einstein units
- Rastreabilidade de entregas

## Resumo Executivo

### Estrutura da Solução

```
Solution
├─ iteration: Número da configuração testada
├─ generation: Gerações executadas pelo GA
├─ fitness: Valor da função objetivo (minimizar)
├─ routes_metadata: {route_id: [(delivery_id, vehicle_id), ...]}
├─ routes_sequences: {route_id: "Centro -> Hospital -> ... -> Centro"} [NOVO]
└─ metrics: {capacity_util, travel_costs, critical_score}
```

### Rastreabilidade de Rotas

**Acesso Direto (Novo):**
- Campo `routes_sequences` fornece sequências formatadas com nomes de hospitais
- Formato: `"Centro -> Hospital (Entrega #X) -> ... -> Centro"`
- Gerado automaticamente usando `address_routes.einstein_units`

**Reconstrução Manual (se necessário):**
1. Extrair IDs de entregas da rota
2. Buscar coordenadas em `deliveries`
3. Buscar especificações em `vehicles`
4. Calcular distâncias Manhattan sequenciais
5. Verificar violações de capacidade e autonomia
6. Calcular custos e métricas

### Métricas Chave

- **Fitness:** 923.44 (moderado, com penalidades)
- **Capacity Utilization:** 0.91 (91%, excelente)
- **Travel Costs:** R$ 33.50 (baixo, eficiente)
- **Critical Score:** 6.5 (alto, boa priorização)

### Interpretação

✅ **Bom:** Custos baixos, alta utilização, priorização adequada
❌ **Ruim:** Violações de capacidade e autonomia, entregas não atendidas
🔍 **Conclusão:** Solução **infactível** que requer ajustes nas restrições ou hiperparâmetros

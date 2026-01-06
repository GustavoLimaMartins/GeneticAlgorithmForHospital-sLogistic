# Pipeline de Otimização Logística - Execução End-to-End

## Visão Geral

O módulo `run.py` implementa o **pipeline completo** de otimização logística, coordenando múltiplas execuções do algoritmo genético com diferentes configurações de hiperparâmetros e selecionando as melhores soluções através de **dois critérios distintos**: fitness mínimo e score de métricas ponderadas. Este pipeline fornece uma abordagem sistemática para explorar o espaço de configurações e identificar soluções ótimas sob diferentes perspectivas.

## Objetivo

Executar busca heurística sobre o espaço de hiperparâmetros do algoritmo genético, avaliar múltiplas soluções candidatas, e selecionar as melhores através de:
1. **Fitness (função objetivo do GA):** Minimização de custo + penalidades
2. **Métricas de negócio:** Balanceamento entre utilização, custo e priorização

Após seleção, gerar visualizações geográficas das rotas ótimas.

## Arquitetura do Pipeline

### Componentes Principais

```
┌────────────────────────────────────────────────────────┐
│                  Classe Solution                       │
│  Coordenador Central do Pipeline                       │
└────────────────────┬───────────────────────────────────┘
                     │
        ┌────────────┴────────────┐
        │                         │
        ▼                         ▼
┌───────────────┐         ┌──────────────┐
│ heuristic_loop│         │best_solution │
│ (Execução GA) │         │  (Seleção)   │
└───────┬───────┘         └──────┬───────┘
        │                        │
        │                        │
        ▼                        ▼
┌────────────────┐      ┌─────────────────┐
│ GeneticAlgorithm│      │ RouteEvaluator │
│ (Otimização)   │      │ (Avaliação)    │
└────────────────┘      └─────────────────┘
```

### Classe Solution

```python
class Solution:
    def __init__(self, total_iterations: int):
        self.total_iterations = total_iterations
        self.solutions = {}                    # Armazena todas as soluções
        self.ga_metadata = None                # Metadados do GA
        self.vehicle_data = None               # Dados dos veículos
        self.delivery_data = None              # Dados das entregas
        self.depot_coords = None               # Coordenadas do centro
        self.best_solution_by_fitness = None   # Melhor por fitness
        self.best_solution_by_metrics = None   # Melhor por métricas
```

**Atributos:**
- `total_iterations`: Número de configurações diferentes a testar
- `solutions`: Dicionário com todas as soluções geradas
- `ga_metadata`: Metadados da última execução do GA
- `vehicle_data`, `delivery_data`, `depot_coords`: Dados do problema
- `best_solution_by_fitness`: Melhor solução segundo fitness do GA
- `best_solution_by_metrics`: Melhor solução segundo métricas de negócio

## Fluxo de Execução End-to-End

### Fase 1: Inicialização

```python
# Passo 1.1: Criar instância do coordenador
solutions = Solution(total_iterations=5)

# Passo 1.2: Definir espaço de busca de hiperparâmetros
configurations = {
    'population_length': (100, 50, 100, 50, 80),
    'max_generations': (50, 150, 250, 350, 450),
    'ratio_elitism': (0.1, 0.2, 0.05, 0.03, 0.15),
    'ratio_mutation': (0.05, 0.25, 0.5, 0.3, 0.1),
    'tournament_k': (2, 5, 3, 3, 2)
}
```

**Configuração:**
```
┌──────────┬──────┬──────┬──────┬──────┬──────┐
│ Iteração │  1   │  2   │  3   │  4   │  5   │
├──────────┼──────┼──────┼──────┼──────┼──────┤
│ pop_size │ 100  │  50  │ 100  │  50  │  80  │
│ max_gen  │  50  │ 150  │ 250  │ 350  │ 450  │
│ elitism  │ 0.10 │ 0.20 │ 0.05 │ 0.03 │ 0.15 │
│ mutation │ 0.05 │ 0.25 │ 0.50 │ 0.30 │ 0.10 │
│ tourn_k  │  2   │  5   │  3   │  3   │  2   │
└──────────┴──────┴──────┴──────┴──────┴──────┘
```

### Fase 2: Loop Heurístico (Exploração do Espaço)

```python
solutions.heuristic_loop(
    city_code="SP",
    population_length=(100, 50, 100, 50, 80),
    max_generations=(50, 150, 250, 350, 450),
    ratio_elitism=(0.1, 0.2, 0.05, 0.03, 0.15),
    ratio_mutation=(0.05, 0.25, 0.5, 0.3, 0.1),
    tournament_k=(2, 5, 3, 3, 2)
)
```

#### Algoritmo do heuristic_loop

```
FUNÇÃO heuristic_loop(city_code, hiperparâmetros):
    
    1. VALIDAÇÃO
       SE comprimento das tuplas ≠ total_iterations:
           LANÇAR erro
    
    2. PARA CADA índice DE 0 ATÉ total_iterations:
       
       2.1. INSTANCIAR ALGORITMO GENÉTICO
            ga = GeneticAlgorithm(
                city_code = city_code,
                population_length = population_length[índice],
                max_generations = max_generations[índice],
                ratio_elitism = ratio_elitism[índice],
                ratio_mutation = ratio_mutation[índice],
                tournament_k = tournament_k[índice]
            )
       
       2.2. EXECUTAR OTIMIZAÇÃO
            ga_metadata = ga.run()
            # Retorna: {
            #   'generation': número_final,
            #   'fitness': fitness_melhor_solução,
            #   'routes_metadata': rotas_solução
            # }
       
       2.3. EXTRAIR DADOS DO PROBLEMA
            vehicle_data = ga.vehicles
            delivery_data = ga.deliveries
            depot_coords = ga.depot
       
       2.4. AVALIAR MÉTRICAS DE NEGÓCIO
            evaluator = RouteEvaluator(
                routes_metadata = ga_metadata['routes_metadata'],
                vehicle_data = vehicle_data,
                delivery_data = delivery_data
            )
            metrics = evaluator.metric_summary()
            # Retorna: {
            #   'capacity_utilization_metric_positive': float,
            #   'travel_costs_metric_negative': float,
            #   'critical_delivery_metric_positive': float
            # }
       
       2.5. CONSOLIDAR SOLUÇÃO
            solution = {
                'iteration': índice + 1,
                'generation': ga_metadata['generation'],
                'fitness': ga_metadata['fitness'],
                'routes_metadata': ga_metadata['routes_metadata'],
                'metrics': metrics
            }
       
       2.6. ARMAZENAR SOLUÇÃO
            self.solutions[índice] = solution
       
       2.7. LOG DE PROGRESSO
            IMPRIMIR "Completed iteration {índice+1}/{total_iterations}"
    
    3. RETORNAR (implícito - dados em self.solutions)
```

#### Exemplo de Execução

**Iteração 1:**
```python
# Configuração
pop_size=100, max_gen=50, elite=0.1, mutation=0.05, k=2

# Execução GA
GA.run() → {
    'generation': 50,
    'fitness': 1285.45,
    'routes_metadata': {...}
}

# Avaliação
evaluator.metric_summary() → {
    'capacity_utilization_metric_positive': 0.87,
    'travel_costs_metric_negative': 246.65,
    'critical_delivery_metric_positive': 4.7
}

# Solução armazenada
solutions[0] = {
    'iteration': 1,
    'generation': 50,
    'fitness': 1285.45,
    'routes_metadata': {...},
    'metrics': {...}
}
```

**Iteração 2:**
```python
# Configuração diferente
pop_size=50, max_gen=150, elite=0.2, mutation=0.25, k=5

# Execução GA
GA.run() → {
    'generation': 150,
    'fitness': 1198.32,  # Melhor fitness!
    'routes_metadata': {...}
}

# Avaliação
evaluator.metric_summary() → {
    'capacity_utilization_metric_positive': 0.92,
    'travel_costs_metric_negative': 235.80,
    'critical_delivery_metric_positive': 5.1
}

# Solução armazenada
solutions[1] = {
    'iteration': 2,
    'generation': 150,
    'fitness': 1198.32,
    'routes_metadata': {...},
    'metrics': {...}
}
```

### Fase 3: Seleção das Melhores Soluções

```python
best_solutions = solutions.best_solution(
    capacity_weight=0.2,
    travel_weight=0.4,
    critical_weight=0.4
)

best_by_fitness = best_solutions['best_by_fitness']
best_by_metrics = best_solutions['best_by_metrics']
```

#### Algoritmo de Seleção Dual

```
FUNÇÃO best_solution(capacity_weight, travel_weight, critical_weight):
    
    ╔═══════════════════════════════════════════════════════╗
    ║ CRITÉRIO 1: MELHOR POR FITNESS (Função Objetivo GA)  ║
    ╚═══════════════════════════════════════════════════════╝
    
    best_index_fitness = None
    best_fitness = +∞
    
    PARA CADA índice, solução EM solutions:
        SE solução['fitness'] < best_fitness:
            best_fitness = solução['fitness']
            best_index_fitness = índice
    
    best_solution_by_fitness = solutions[best_index_fitness]
    
    
    ╔═══════════════════════════════════════════════════════╗
    ║ CRITÉRIO 2: MELHOR POR MÉTRICAS (Score Ponderado)    ║
    ╚═══════════════════════════════════════════════════════╝
    
    best_index_metrics = None
    best_metric_score = -∞
    
    PARA CADA índice, solução EM solutions:
        metrics = solução['metrics']
        
        metric_score = (
            metrics['capacity_utilization_metric_positive'] × capacity_weight -
            metrics['travel_costs_metric_negative'] × travel_weight +
            metrics['critical_delivery_metric_positive'] × critical_weight
        )
        
        SE metric_score > best_metric_score:
            best_metric_score = metric_score
            best_index_metrics = índice
    
    best_solution_by_metrics = solutions[best_index_metrics]
    
    
    RETORNAR {
        'best_by_fitness': best_solution_by_fitness,
        'best_by_metrics': best_solution_by_metrics
    }
```

#### Critério 1: Melhor por Fitness

**Modelo Matemático:**

$$\text{Melhor Fitness} = \arg\min_{i \in \text{Iterações}} F_i$$

Onde $F_i$ é o fitness da solução da iteração $i$.

**Exemplo:**
```python
solutions = {
    0: {'fitness': 1285.45, ...},
    1: {'fitness': 1198.32, ...},  # ← MENOR FITNESS
    2: {'fitness': 1320.78, ...},
    3: {'fitness': 1245.90, ...},
    4: {'fitness': 1210.15, ...}
}

# Melhor: Iteração 1 com fitness 1198.32
best_by_fitness = solutions[1]
```

**Interpretação:**
- Solução que **minimiza** função objetivo do GA
- Melhor segundo critério de **otimização pura**
- Balanceia custos, penalidades e restrições conforme pesos do GA

#### Critério 2: Melhor por Métricas

**Modelo Matemático:**

$$\text{Score}(i) = w_c \cdot U_i - w_t \cdot C_i + w_p \cdot P_i$$

Onde:
- $U_i$: Utilização de capacidade (positivo)
- $C_i$: Custo de viagem (negativo)
- $P_i$: Score de priorização (positivo)
- $w_c, w_t, w_p$: Pesos (padrão: 0.2, 0.4, 0.4)

$$\text{Melhor Métricas} = \arg\max_{i \in \text{Iterações}} \text{Score}(i)$$

**Exemplo:**
```python
# Pesos padrão
capacity_weight = 0.2
travel_weight = 0.4
critical_weight = 0.4

# Iteração 0
metrics_0 = {
    'capacity_utilization_metric_positive': 0.87,
    'travel_costs_metric_negative': 246.65,
    'critical_delivery_metric_positive': 4.7
}
score_0 = 0.87*0.2 - 246.65*0.4 + 4.7*0.4
        = 0.174 - 98.66 + 1.88
        = -96.606

# Iteração 1
metrics_1 = {
    'capacity_utilization_metric_positive': 0.92,
    'travel_costs_metric_negative': 235.80,
    'critical_delivery_metric_positive': 5.1
}
score_1 = 0.92*0.2 - 235.80*0.4 + 5.1*0.4
        = 0.184 - 94.32 + 2.04
        = -92.096  # ← MAIOR SCORE (menos negativo)

# Iteração 2
metrics_2 = {
    'capacity_utilization_metric_positive': 0.78,
    'travel_costs_metric_negative': 258.40,
    'critical_delivery_metric_positive': 4.2
}
score_2 = 0.78*0.2 - 258.40*0.4 + 4.2*0.4
        = 0.156 - 103.36 + 1.68
        = -101.524

# Melhor: Iteração 1 com score -92.096
best_by_metrics = solutions[1]
```

**Nota:** Scores são tipicamente negativos devido ao peso dominante dos custos. O **menos negativo** é o melhor.

#### Comparação: Fitness vs Métricas

**Por que dois critérios?**

| Aspecto | Fitness (GA) | Métricas (Negócio) |
|---------|--------------|-------------------|
| **Objetivo** | Minimizar função do GA | Maximizar score ponderado |
| **Foco** | Otimização pura | Balanceamento gerencial |
| **Componentes** | Custos + penalidades complexas | Métricas operacionais simples |
| **Pesos** | Fixos no código GA | Ajustáveis pelo usuário |
| **Uso** | Garantir viabilidade técnica | Alinhar com prioridades de negócio |

**Cenário Comum: Soluções Diferentes**

```python
# Solução com melhor fitness
best_by_fitness = {
    'fitness': 1198.32,  # Mínimo
    'metrics': {
        'capacity_utilization': 0.75,  # Razoável
        'travel_costs': 220.50,        # Muito baixo
        'critical_delivery': 3.8       # Baixo
    }
}
# Interpretação: Otimizada para custo, negligencia priorização

# Solução com melhores métricas
best_by_metrics = {
    'fitness': 1245.90,  # Não é mínimo
    'metrics': {
        'capacity_utilization': 0.92,  # Excelente
        'travel_costs': 235.80,        # Moderado
        'critical_delivery': 5.1       # Excelente
    }
}
# Interpretação: Balanceada, melhor operacionalmente
```

**Decisão Gerencial:**
- **Usar best_by_fitness:** Quando custo é prioridade absoluta
- **Usar best_by_metrics:** Quando balanceamento e SLA são importantes
- **Híbrido:** Analisar ambas e escolher baseado em contexto

### Fase 4: Visualização Geográfica

```python
# Preparar dados de visualização
gmaps_api = GoogleMapsAPI()
origin = solutions.depot_coords
destination = solutions.depot_coords

# Processar ambas as melhores soluções
metadata_solutions = (
    (best_by_fitness, SolutionMethod.FITNESS),
    (best_by_metrics, SolutionMethod.METRICS)
)

for solution, sol_method in metadata_solutions:
    for route in solution['routes_metadata'].keys():
        
        # 1. Extrair coordenadas das entregas
        solution_deliveries = []
        for delivery in solution['routes_metadata'][route]:
            delivery_id = int(delivery[0])
            coords = (
                solutions.delivery_data[delivery_id]['lat'],
                solutions.delivery_data[delivery_id]['lon']
            )
            solution_deliveries.append(coords)
        
        # 2. Obter direções via Google Maps API
        directions = gmaps_api.get_directions(
            origin, 
            destination, 
            solution_deliveries
        )
        
        # 3. Extrair polyline com cores
        poly_designer = PolylineDesigner(directions)
        coords, leg_starts = poly_designer.extract_coordinates_with_multicolors()
        
        # 4. Gerar mapa interativo Folium
        folium_path = FoliumPath(
            coords, 
            leg_starts, 
            iterator=solution['iteration'],
            generation=solution['generation'],
            route_id=route
        )
        folium_path.create_html_map(sol_method)
        
        # 5. Gerar mapa estático
        static_map = StaticMapRoute(
            coords, 
            leg_starts,
            iterator=solution['iteration'],
            generation=solution['generation'],
            route_id=route
        )
        static_map.create_static_map(sol_method)
```

#### Fluxo de Visualização

```
Para cada solução (fitness e métricas):
    Para cada rota na solução:
        
        ┌─────────────────────────────────────┐
        │ 1. Coletar Coordenadas das Entregas │
        └──────────────┬──────────────────────┘
                       │
                       ▼
        ┌─────────────────────────────────────┐
        │ 2. Solicitar Rotas Google Maps API  │
        │    (origem → waypoints → destino)   │
        └──────────────┬──────────────────────┘
                       │
                       ▼
        ┌─────────────────────────────────────┐
        │ 3. Decodificar Polylines            │
        │    (extrair coordenadas detalhadas) │
        └──────────────┬──────────────────────┘
                       │
                       ▼
        ┌─────────────────────────────────────┐
        │ 4. Gerar Mapa Interativo (Folium)   │
        │    - HTML navegável                 │
        │    - Rotas coloridas por segmento   │
        │    - Marcadores em entregas         │
        └──────────────┬──────────────────────┘
                       │
                       ▼
        ┌─────────────────────────────────────┐
        │ 5. Gerar Mapa Estático (PNG)        │
        │    - Imagem para relatórios         │
        │    - Visão geral da rota            │
        └─────────────────────────────────────┘
```

#### Estrutura de Arquivos Gerados

```
itinerary_routes/routes_maps/
├── fitness/
│   ├── i2_by_fitness_1route_map_150gen.html
│   ├── i2_by_fitness_2route_map_150gen.html
│   ├── i2_by_fitness_3route_map_150gen.html
│   ├── i2_by_fitness_4route_map_150gen.html
│   ├── i2_by_fitness_5route_map_150gen.html
│   ├── i2_by_fitness_1route_map_150gen.png
│   └── ...
└── metrics/
    ├── i4_by_metrics_1route_map_350gen.html
    ├── i4_by_metrics_2route_map_350gen.html
    ├── i4_by_metrics_3route_map_350gen.html
    ├── i4_by_metrics_4route_map_350gen.html
    ├── i4_by_metrics_5route_map_350gen.html
    ├── i4_by_metrics_1route_map_350gen.png
    └── ...
```

**Nomenclatura:**
```
i{iteration}_by_{method}_{route_id}route_map_{generation}gen.{ext}

Exemplo:
i2_by_fitness_3route_map_150gen.html
│  │         │         │        │
│  │         │         │        └─ Geração final do GA
│  │         │         └───────── Rota 3
│  │         └─────────────────── Método de seleção
│  └───────────────────────────── Iteração 2
└──────────────────────────────── Prefixo "iteration"
```

## Pipeline Completo Resumido

### Diagrama de Sequência

```
┌────────┐   ┌──────────────┐   ┌────────────┐   ┌──────────────┐
│ Main   │   │  Solution    │   │ GeneticAlg │   │RouteEvaluator│
└───┬────┘   └──────┬───────┘   └─────┬──────┘   └──────┬───────┘
    │               │                  │                  │
    │ new(5)        │                  │                  │
    ├──────────────>│                  │                  │
    │               │                  │                  │
    │heuristic_loop()│                 │                  │
    ├──────────────>│                  │                  │
    │               │                  │                  │
    │               │ PARA i=0..4      │                  │
    │               │ ┌──────────────┐ │                  │
    │               │ │              │ │                  │
    │               ├─┼> new(params) │ │                  │
    │               │ │              │ │                  │
    │               │ ├──> run()     │ │                  │
    │               │ │              <─┤                  │
    │               │ │ ga_metadata  │                    │
    │               │ │              │                    │
    │               ├─┼──────────────┼──> new(routes)    │
    │               │ │              │                    │
    │               │ │              │  metric_summary() <┤
    │               │ │              │ <─────────────────┤
    │               │ │              │      metrics       │
    │               │ │              │                    │
    │               │ │ store_solution()                  │
    │               │ └──────────────┘                    │
    │               │                                     │
    │best_solution()│                                     │
    ├──────────────>│                                     │
    │<──────────────┤                                     │
    │ {best_fitness,                                      │
    │  best_metrics}                                      │
    │               │                                     │
    │ generate_maps()                                     │
    └───────────────┘                                     │
```

### Pseudocódigo End-to-End

```
PROGRAMA Pipeline_Otimização_Logística:

1. INICIALIZAÇÃO
   ════════════════
   total_iter = 5
   sol = Solution(total_iter)
   
2. CONFIGURAÇÃO
   ═════════════════
   configs = [
       (pop=100, gen=50,  elite=0.1, mut=0.05, k=2),
       (pop=50,  gen=150, elite=0.2, mut=0.25, k=5),
       (pop=100, gen=250, elite=0.05, mut=0.5, k=3),
       (pop=50,  gen=350, elite=0.03, mut=0.3, k=3),
       (pop=80,  gen=450, elite=0.15, mut=0.1, k=2)
   ]
   
3. EXPLORAÇÃO (Loop Heurístico)
   ═══════════════════════════════
   PARA CADA config EM configs:
       
       3.1. Executar GA
            ga = GeneticAlgorithm(config)
            metadata = ga.run()
       
       3.2. Avaliar Métricas
            evaluator = RouteEvaluator(metadata.routes)
            metrics = evaluator.metric_summary()
       
       3.3. Armazenar
            sol.solutions[i] = {
                fitness: metadata.fitness,
                routes: metadata.routes,
                metrics: metrics
            }
   
4. SELEÇÃO (Dual Criteria)
   ═════════════════════════
   4.1. Melhor por Fitness
        best_fit = MIN(sol.fitness for sol in solutions)
   
   4.2. Melhor por Métricas
        best_met = MAX(score(sol.metrics) for sol in solutions)
        onde score = 0.2*util - 0.4*cost + 0.4*priority
   
5. VISUALIZAÇÃO
   ═══════════════
   PARA CADA solution EM [best_fit, best_met]:
       PARA CADA route EM solution.routes:
           
           5.1. Obter Direções Google Maps
           5.2. Decodificar Polylines
           5.3. Gerar HTML Interativo
           5.4. Gerar PNG Estático
   
6. SAÍDA
   ════════
   - 2 Soluções Selecionadas
   - N Mapas HTML (rotas × 2 soluções)
   - N Mapas PNG (rotas × 2 soluções)
   - Logs de Execução
```

## Exemplo Prático Completo

### Configuração e Execução

```python
from run import Solution

# 1. Criar pipeline com 3 iterações
pipeline = Solution(total_iterations=3)

# 2. Definir espaço de busca
pipeline.heuristic_loop(
    city_code="SP",
    population_length=(50, 100, 75),
    max_generations=(100, 200, 150),
    ratio_elitism=(0.05, 0.10, 0.08),
    ratio_mutation=(0.10, 0.20, 0.15),
    tournament_k=(2, 3, 2)
)

# Output durante execução:
# Completed iteration 1/3
# Completed iteration 2/3
# Completed iteration 3/3

# 3. Selecionar melhores
best = pipeline.best_solution(
    capacity_weight=0.3,
    travel_weight=0.4,
    critical_weight=0.3
)

# 4. Inspecionar resultados
print("=" * 60)
print("MELHOR SOLUÇÃO POR FITNESS")
print("=" * 60)
print(f"Iteração: {best['best_by_fitness']['iteration']}")
print(f"Geração: {best['best_by_fitness']['generation']}")
print(f"Fitness: {best['best_by_fitness']['fitness']:.2f}")
print(f"Métricas:")
for k, v in best['best_by_fitness']['metrics'].items():
    print(f"  {k}: {v}")

print("\n" + "=" * 60)
print("MELHOR SOLUÇÃO POR MÉTRICAS")
print("=" * 60)
print(f"Iteração: {best['best_by_metrics']['iteration']}")
print(f"Geração: {best['best_by_metrics']['generation']}")
print(f"Fitness: {best['best_by_metrics']['fitness']:.2f}")
print(f"Métricas:")
for k, v in best['best_by_metrics']['metrics'].items():
    print(f"  {k}: {v}")
```

### Saída Esperada

```
Completed iteration 1/3
Completed iteration 2/3
Completed iteration 3/3

============================================================
MELHOR SOLUÇÃO POR FITNESS
============================================================
Iteração: 2
Geração: 200
Fitness: 1178.25
Métricas:
  capacity_utilization_metric_positive: 0.82
  travel_costs_metric_negative: 228.40
  critical_delivery_metric_positive: 4.5

============================================================
MELHOR SOLUÇÃO POR MÉTRICAS
============================================================
Iteração: 3
Geração: 150
Fitness: 1215.80
Métricas:
  capacity_utilization_metric_positive: 0.91
  travel_costs_metric_negative: 240.50
  critical_delivery_metric_positive: 5.2
```

**Análise:**
- **Fitness:** Iteração 2 otimizou função objetivo (1178.25 < 1215.80)
- **Métricas:** Iteração 3 balanceou melhor as métricas de negócio
  - Maior utilização: 0.91 vs 0.82
  - Melhor priorização: 5.2 vs 4.5
  - Custo ligeiramente maior: 240.50 vs 228.40

## Ajuste de Pesos das Métricas

### Cenários de Negócio

#### Cenário 1: Prioridade em Custo

```python
# Empresa com margem apertada
best = pipeline.best_solution(
    capacity_weight=0.1,   # Baixo
    travel_weight=0.7,     # Alto
    critical_weight=0.2    # Baixo
)
# Resultado: Solução com menor custo operacional
```

#### Cenário 2: Prioridade em SLA

```python
# Empresa com contratos rigorosos
best = pipeline.best_solution(
    capacity_weight=0.2,   # Baixo
    travel_weight=0.2,     # Baixo
    critical_weight=0.6    # Alto
)
# Resultado: Entregas críticas priorizadas
```

#### Cenário 3: Eficiência de Frota

```python
# Empresa focada em consolidação
best = pipeline.best_solution(
    capacity_weight=0.6,   # Alto
    travel_weight=0.3,     # Médio
    critical_weight=0.1    # Baixo
)
# Resultado: Máxima utilização de capacidade
```

#### Cenário 4: Balanceado

```python
# Abordagem equilibrada
best = pipeline.best_solution(
    capacity_weight=0.33,
    travel_weight=0.33,
    critical_weight=0.34
)
# Resultado: Trade-off entre todos os objetivos
```

## Análise de Convergência

### Monitoramento Durante Execução

```python
import matplotlib.pyplot as plt

def plot_convergence_analysis(solutions):
    """
    Visualiza evolução das métricas ao longo das iterações
    """
    iterations = []
    fitness_values = []
    capacity_values = []
    cost_values = []
    priority_values = []
    
    for idx, sol in solutions.solutions.items():
        iterations.append(sol['iteration'])
        fitness_values.append(sol['fitness'])
        capacity_values.append(sol['metrics']['capacity_utilization_metric_positive'])
        cost_values.append(sol['metrics']['travel_costs_metric_negative'])
        priority_values.append(sol['metrics']['critical_delivery_metric_positive'])
    
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    
    # Fitness
    axes[0, 0].plot(iterations, fitness_values, 'o-', color='blue')
    axes[0, 0].set_title('Fitness por Iteração')
    axes[0, 0].set_xlabel('Iteração')
    axes[0, 0].set_ylabel('Fitness')
    axes[0, 0].grid(True)
    
    # Utilização
    axes[0, 1].plot(iterations, capacity_values, 'o-', color='green')
    axes[0, 1].set_title('Utilização de Capacidade')
    axes[0, 1].set_xlabel('Iteração')
    axes[0, 1].set_ylabel('Utilização')
    axes[0, 1].grid(True)
    
    # Custo
    axes[1, 0].plot(iterations, cost_values, 'o-', color='red')
    axes[1, 0].set_title('Custo de Viagem')
    axes[1, 0].set_xlabel('Iteração')
    axes[1, 0].set_ylabel('Custo (R$)')
    axes[1, 0].grid(True)
    
    # Priorização
    axes[1, 1].plot(iterations, priority_values, 'o-', color='purple')
    axes[1, 1].set_title('Score de Priorização')
    axes[1, 1].set_xlabel('Iteração')
    axes[1, 1].set_ylabel('Score')
    axes[1, 1].grid(True)
    
    plt.tight_layout()
    plt.savefig('convergence_analysis.png', dpi=300)
    plt.show()

# Uso após execução
plot_convergence_analysis(pipeline)
```

## Otimizações e Melhorias

### 1. Grid Search Sistemático

```python
def grid_search_hyperparameters():
    """
    Busca exaustiva no espaço de hiperparâmetros
    """
    pop_sizes = [50, 100, 150]
    generations = [100, 200, 300]
    elitisms = [0.05, 0.10, 0.15]
    mutations = [0.1, 0.2, 0.3]
    tournament_ks = [2, 3, 5]
    
    total_combinations = (
        len(pop_sizes) * len(generations) * 
        len(elitisms) * len(mutations) * len(tournament_ks)
    )
    # Total: 3 × 3 × 3 × 3 × 3 = 243 combinações
    
    configs = []
    for pop in pop_sizes:
        for gen in generations:
            for elite in elitisms:
                for mut in mutations:
                    for k in tournament_ks:
                        configs.append((pop, gen, elite, mut, k))
    
    pipeline = Solution(total_iterations=len(configs))
    # ... executar todas as configurações
    
    return pipeline.best_solution()
```

### 2. Random Search (Mais Eficiente)

```python
import random

def random_search_hyperparameters(n_iterations=20):
    """
    Busca aleatória (mais eficiente que grid search)
    """
    configs = []
    for _ in range(n_iterations):
        pop = random.choice([50, 75, 100, 125, 150])
        gen = random.choice([100, 150, 200, 250, 300])
        elite = random.uniform(0.03, 0.20)
        mut = random.uniform(0.05, 0.40)
        k = random.choice([2, 3, 4, 5])
        configs.append((pop, gen, elite, mut, k))
    
    pipeline = Solution(total_iterations=n_iterations)
    # ... executar configurações aleatórias
    
    return pipeline.best_solution()
```

### 3. Bayesian Optimization

```python
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF

def bayesian_optimization_hyperparameters(n_iterations=30):
    """
    Otimização Bayesiana de hiperparâmetros
    """
    # Espaço de busca
    space = {
        'population_length': (50, 150),
        'max_generations': (100, 400),
        'ratio_elitism': (0.03, 0.20),
        'ratio_mutation': (0.05, 0.50),
        'tournament_k': (2, 5)
    }
    
    # Modelo Gaussiano
    gp = GaussianProcessRegressor(kernel=RBF())
    
    # Iterações
    X_observed = []
    y_observed = []
    
    for iteration in range(n_iterations):
        # Selecionar próxima configuração via acquisition function
        next_config = select_next_sample(gp, space, X_observed)
        
        # Avaliar
        pipeline = Solution(total_iterations=1)
        # ... executar
        fitness = pipeline.solutions[0]['fitness']
        
        # Atualizar modelo
        X_observed.append(next_config)
        y_observed.append(fitness)
        gp.fit(X_observed, y_observed)
    
    # Retornar melhor encontrado
    best_idx = np.argmin(y_observed)
    return X_observed[best_idx]
```

### 4. Paralelização

```python
from multiprocessing import Pool

def parallel_heuristic_loop(configs, n_processes=4):
    """
    Executa múltiplas configurações em paralelo
    """
    def run_single_config(config):
        pop, gen, elite, mut, k = config
        ga = GeneticAlgorithm(
            city_code="SP",
            population_length=pop,
            max_generations=gen,
            ratio_elitism=elite,
            ratio_mutation=mut,
            tournament_k=k
        )
        metadata = ga.run()
        evaluator = RouteEvaluator(...)
        metrics = evaluator.metric_summary()
        return {'fitness': metadata['fitness'], 'metrics': metrics}
    
    with Pool(n_processes) as pool:
        results = pool.map(run_single_config, configs)
    
    return results
```

## Palavras-chave para Busca

- Pipeline de otimização
- Execução end-to-end
- Busca heurística
- Espaço de hiperparâmetros
- Seleção dual criteria
- Best by fitness
- Best by metrics
- Score ponderado
- Grid search
- Random search
- Bayesian optimization
- Visualização de rotas
- Google Maps API
- Folium mapas interativos
- Análise de convergência
- Trade-off multiobjetivo
- Exploração vs explotação
- Pipeline logística

## Resumo Executivo

### Fluxo em 3 Etapas

1. **EXPLORAÇÃO (heuristic_loop)**
   - Testa múltiplas configurações do GA
   - Armazena todas as soluções com fitness e métricas

2. **SELEÇÃO (best_solution)**
   - Critério 1: Menor fitness (otimização pura)
   - Critério 2: Maior score de métricas (balanceamento)

3. **VISUALIZAÇÃO (maps generation)**
   - Gera mapas interativos e estáticos
   - Documenta rotas das melhores soluções

### Saídas Principais

```
Pipeline Output:
├── Soluções Armazenadas: solutions.solutions[0..n]
├── Melhor por Fitness: best_by_fitness
├── Melhor por Métricas: best_by_metrics
└── Visualizações:
    ├── HTML Maps: routes_maps/fitness/*.html
    │               routes_maps/metrics/*.html
    └── PNG Maps:  routes_maps/fitness/*.png
                   routes_maps/metrics/*.png
```

### Complexidade Total

**Tempo:** O(I × (P × G × E)) onde:
- I: Número de iterações
- P: População média
- G: Gerações médias
- E: Entregas

**Exemplo:** 5 iterações × 75 pop × 250 gen × 25 entregas ≈ 2.3M avaliações

### Recomendações de Uso

**Desenvolvimento/Teste:**
```python
Solution(total_iterations=3)
# Poucos testes, gerações baixas (50-100)
```

**Produção/Otimização:**
```python
Solution(total_iterations=10-20)
# Muitos testes, gerações altas (200-500)
```

**Pesquisa/Benchmark:**
```python
Solution(total_iterations=50-100)
# Grid/Random search completo
```

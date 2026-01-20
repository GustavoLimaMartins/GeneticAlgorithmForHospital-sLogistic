# 🏥 Sistema de Otimização Logística Hospitalar - Hospital Albert Einstein

## 📋 Sumário

- [Visão Geral](#-visão-geral)
- [Contexto do Problema](#-contexto-do-problema)
- [Modelagem Matemática](#-modelagem-matemática)
- [Arquitetura do Sistema](#-arquitetura-do-sistema)
- [Algoritmo Genético](#-algoritmo-genético)
- [Módulos do Sistema](#-módulos-do-sistema)
- [Instalação e Execução](#-instalação-e-execução)
- [Resultados e Visualizações](#-resultados-e-visualizações)
- [Sistema LLM/RAG](#-sistema-llmrag---assistente-inteligente)
- [Tecnologias Utilizadas](#-tecnologias-utilizadas)

---

## 🎯 Visão Geral

Este projeto implementa um **sistema inteligente de otimização de rotas** para logística hospitalar utilizando **Algoritmos Genéticos**. O sistema foi desenvolvido para otimizar a distribuição de suprimentos médicos entre unidades do Hospital Albert Einstein na região metropolitana de São Paulo.

### Objetivos Principais

1. **Minimizar custos operacionais** de transporte
2. **Otimizar capacidade** de utilização da frota
3. **Priorizar entregas críticas** (medicamentos, materiais cirúrgicos)
4. **Respeitar restrições** de capacidade e autonomia dos veículos
5. **Gerar visualizações** georreferenciadas das rotas otimizadas
6. **Assistente inteligente** com LLM para consultas sobre logística e soluções

---

## 🏥 Contexto do Problema

### Cenário Real

O Hospital Albert Einstein opera uma rede de **25 unidades** distribuídas pela cidade de São Paulo, incluindo:

- Hospitais principais (Morumbi, Alphaville, Ibirapuera)
- Clínicas especializadas (Oncologia, Reabilitação)
- Centros de diagnóstico (Anália Franco, Jardins, Perdizes)

### Desafios Logísticos

O sistema de distribuição enfrenta múltiplos desafios:

#### 1. **Restrições de Veículos**
- 5 tipos de veículos com diferentes capacidades (6 a 45 unidades)
- Autonomia limitada (medida em distância Manhattan)
- Custos operacionais variados por tipo de veículo

#### 2. **Prioridades de Entrega**
- **Prioridade 3 (Crítica)**: Medicamentos controlados, materiais cirúrgicos
- **Prioridade 2 (Alta)**: Insumos hospitalares, equipamentos
- **Prioridade 1 (Normal)**: Suprimentos gerais, administrativos

#### 3. **Complexidade Combinatória**
- 25 pontos de entrega
- 5 veículos diferentes
- Múltiplas rotas possíveis por veículo
- Espaço de busca: $25! \times 5^{25} \approx 10^{60}$ combinações possíveis

---

## 📐 Modelagem Matemática

### Função Fitness

A função de aptidão (fitness) do algoritmo genético é composta por múltiplos componentes que avaliam a qualidade de uma solução:

$$
F_{total} = C_{viagem} + P_{capacidade} + P_{autonomia} + P_{eficiência} + P_{prioridade}
$$

Onde:

#### 1. **Custo de Viagem** ($C_{viagem}$)

$$
C_{viagem} = \sum_{r=1}^{R} D_M^{(r)} \times c_v^{(r)}
$$

- $D_M^{(r)}$: Distância Manhattan da rota $r$
- $c_v^{(r)}$: Custo por unidade Manhattan do veículo usado na rota $r$
- $R$: Número total de rotas

#### 2. **Penalidade de Capacidade** ($P_{capacidade}$)

$$
P_{capacidade} = \sum_{r=1}^{R} \begin{cases} 
100 \times (L^{(r)} - C_v^{(r)}) & \text{se } L^{(r)} > C_v^{(r)} \\
0 & \text{caso contrário}
\end{cases}
$$

- $L^{(r)}$: Carga total na rota $r$
- $C_v^{(r)}$: Capacidade do veículo na rota $r$
- **Peso**: 100 (constraint soft - permite leve sobrecarga)

#### 3. **Penalidade de Autonomia** ($P_{autonomia}$)

$$
P_{autonomia} = \sum_{r=1}^{R} \begin{cases} 
200 \times (D_M^{(r)} - A_v^{(r)}) & \text{se } D_M^{(r)} > A_v^{(r)} \\
0 & \text{caso contrário}
\end{cases}
$$

- $A_v^{(r)}$: Autonomia máxima do veículo (distância Manhattan)
- **Peso**: 200 (constraint hard - violação crítica de segurança)

#### 4. **Penalidade de Eficiência** ($P_{eficiência}$)

$$
P_{eficiência} = \sum_{r=1}^{R} \begin{cases} 
5 \times \left(\frac{C_{viagem}^{(r)}}{n_e^{(r)}} - \theta\right) & \text{se } \frac{C_{viagem}^{(r)}}{n_e^{(r)}} > \theta \\
0 & \text{caso contrário}
\end{cases}
$$

- $n_e^{(r)}$: Número de entregas na rota $r$
- $\theta = 5.0$: Limiar de eficiência (custo por entrega)
- **Peso**: 5 (penaliza rotas com poucos pontos de entrega)

#### 5. **Penalidade de Prioridade** ($P_{prioridade}$)

A penalidade de prioridade considera duas dimensões: a posição da rota e a posição da entrega dentro da rota.

$$
P_{prioridade} = P_{crítica} + P_{alta}
$$

##### Entregas Críticas (Prioridade 3):

$$
P_{crítica} = \sum_{r=1}^{R} \sum_{i \in E_3^{(r)}} \left[ (r \times 12 + p_i \times 1.5) + (r^2 \times 2.0) \right]
$$

- $E_3^{(r)}$: Conjunto de entregas críticas na rota $r$
- $p_i$: Posição da entrega $i$ dentro da rota
- **Componente linear**: $r \times 12 + p_i \times 1.5$
- **Componente quadrático**: $r^2 \times 2.0$ (crescimento exponencial)

##### Entregas de Alta Prioridade (Prioridade 2):

$$
P_{alta} = \sum_{r=1}^{R} \sum_{j \in E_2^{(r)}} (r \times 3 + p_j \times 0.6)
$$

- $E_2^{(r)}$: Conjunto de entregas de alta prioridade na rota $r$
- **Componente linear moderado**

### Distância Manhattan

O projeto utiliza a métrica de distância Manhattan para cálculo de rotas:

$$
d_M((x_1, y_1), (x_2, y_2)) = |x_1 - x_2| + |y_1 - y_2|
$$

**Vantagens**:
- Modelagem mais realista do tráfego urbano (grid de ruas)
- Computacionalmente eficiente
- Adequada para áreas metropolitanas

### Cálculo de Distância de Rota

Para uma rota com $n$ pontos de entrega e depósito central $C$:

$$
D_{rota} = d_M(C, p_1) + \sum_{i=1}^{n-1} d_M(p_i, p_{i+1}) + d_M(p_n, C)
$$

- $C$: Coordenadas do centro de distribuição
- $p_i$: Coordenadas do ponto de entrega $i$

---

## 🏗️ Arquitetura do Sistema

### Visão Geral da Arquitetura

```
┌─────────────────────────────────────────────────────────────┐
│                         run.py                              │
│                  (Orquestrador Principal)                   │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   genetic_algorithm.py                      │
│              (Motor do Algoritmo Genético)                  │
└─────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
┌───────────────┐   ┌──────────────────┐   ┌──────────────┐
│  População    │   │   Avaliação      │   │  Evolução    │
│               │   │                  │   │              │
│ • generate    │   │ • fitness        │   │ • selection  │
│ • encode      │   │ • decode         │   │ • crossover  │
│ • decode      │   │ • distance       │   │ • mutation   │
└───────────────┘   └──────────────────┘   └──────────────┘
        │                     │                     │
        └─────────────────────┴─────────────────────┘
                              ▼
                 ┌──────────────────────┐
                 │  Visualização Stats  │
                 │                      │
                 │ • plot_fitness_      │
                 │   evolution          │
                 │ • fitness_history    │
                 └──────────────────────┘
                              │
        ┌─────────────────────┴─────────────────────┐
        ▼                                           ▼
┌──────────────────┐                    ┌──────────────────┐
│ routes_evaluation│                    │ itinerary_routes │
│                  │                    │                  │
│ • Métricas       │                    │ • Google Maps    │
│ • Capacidade     │                    │ • Polyline       │
│ • Custos         │                    │ • Folium         │
│ • Prioridades    │                    │ • Static Maps    │
└──────────────────┘                    └──────────────────┘
        │                                           │
        ▼                                           ▼
┌──────────────────┐                    ┌──────────────────┐
│ delivery_setup   │                    │ address_routes   │
│                  │                    │                  │
│ • deliveries.py  │                    │ • einstein_units │
│ • vehicles.py    │                    │ • distribution   │
└──────────────────┘                    └──────────────────┘
```

### Estrutura de Diretórios

```
Desafio Fase 2/
│
├── run.py                          # 🎯 Orquestrador principal
├── genetic_algorithm.py            # 🧬 Motor do AG
├── routes_evaluation.py            # 📊 Avaliação de métricas
│
├── a_generate_population.py        # 👥 Geração de população
├── b_manhattan_distance.py         # 📏 Cálculo de distâncias
├── c_fitness.py                    # ⚡ Função de aptidão
├── d_crossover.py                  # 🔀 Operadores de cruzamento
├── e_mutation.py                   # 🧪 Operadores de mutação
├── f_selection.py                  # 🎯 Seleção de indivíduos
├── _encode_decode.py               # 🔄 Codificação cromossômica
│
├── delivery_setup/                 # 📦 Configuração de entregas
│   ├── deliveries.py              # 📍 Dados das entregas
│   └── vehicles.py                # 🚛 Dados dos veículos
│
├── address_routes/                 # 🗺️ Dados geográficos
│   ├── einstein_units.py          # 🏥 Unidades do Einstein
│   ├── distribute_center.py       # 🏢 Centro de distribuição
│   └── unify_coordinates.py       # 📐 Unificação de coordenadas
│
├── itinerary_routes/              # 🛣️ Visualização de rotas
│   ├── a_google_maps.py           # 🌍 API Google Maps
│   ├── b_polyline_designer.py     # ✏️ Desenho de polylines
│   ├── c_folium_path.py           # 🗺️ Mapas interativos
│   ├── d_static_map.py            # 📸 Mapas estáticos
│   └── _solution_type.py          # 🏷️ Enums de solução
│
└── llm/                           # 🤖 Assistente Inteligente (RAG)
    ├── interface.py               # 💬 Interface Streamlit
    ├── langchain_setup.py         # 🔗 Cliente LangChain
    ├── openai_setup.py            # 🧠 Cliente OpenAI
    ├── chroma_db.py               # 💾 Vector Store (Chroma)
    ├── solutions_data.json        # 📊 Dados das soluções
    ├── chroma/                    # 📦 Banco vetorial
    └── logistic_infos_docs/       # 📚 Documentação RAG
        ├── pipeline.md            # Pipeline do AG
        ├── deliveries.md          # Dados de entregas
        ├── vehicles.md            # Dados de veículos
        └── solution_explanation.md # Estrutura de soluções
```

---

## 🧬 Algoritmo Genético

### Representação Cromossômica

#### Indivíduo (Solução)

Um indivíduo representa uma solução completa para o problema de roteamento:

```python
# Representação decodificada (fenotípica)
individual = [
    ("V1", (1, 4, 9)),      # Veículo V1 entrega nos pontos 1, 4, 9
    ("V2", (2, 7, 12)),     # Veículo V2 entrega nos pontos 2, 7, 12
    ("V3", (3, 8, 15)),     # ...
    # ...
]

# Representação codificada (genotípica - cromossomo)
chromosome = [1, 4, 9, 2, 7, 12, 3, 8, 15, ...]  # Sequência linear
```

#### Processo de Codificação/Decodificação

**Codificação** (`encode_individual`):
- Transforma rotas atribuídas a veículos em sequência linear
- Facilita operações genéticas (crossover, mutação)

**Decodificação** (`decode_chromosome`):
- Reconstrói rotas respeitando capacidades
- Atribui entregas a veículos de forma gulosa
- Permite múltiplas viagens por veículo

### Fluxo do Algoritmo

```
1. INICIALIZAÇÃO
   ├─ Gerar população aleatória (N indivíduos)
   ├─ Codificar cada indivíduo como cromossomo
   └─ Avaliar fitness inicial
   
2. LOOP EVOLUTIVO (G gerações)
   │
   ├─ AVALIAÇÃO
   │  ├─ Decodificar cromossomos em rotas
   │  ├─ Calcular fitness de cada indivíduo
   │  ├─ Registrar estatísticas (melhor, média, pior)
   │  └─ Atualizar fitness_history
   │
   ├─ SELEÇÃO
   │  ├─ Elitismo: preservar melhores (ratio_elitism)
   │  └─ Torneio: selecionar pais (tournament_k)
   │
   ├─ REPRODUÇÃO
   │  ├─ Crossover: gerar filhos (RBX ou BCRC)
   │  └─ Mutação: diversificar (swap/relocate)
   │
   └─ SUBSTITUIÇÃO
      └─ Nova geração substitui anterior
      
3. FINALIZAÇÃO
   ├─ Retornar melhor solução encontrada
   ├─ Decodificar em rotas finais
   ├─ Gerar gráfico de evolução (fitness x gerações)
   └─ Gerar visualizações de rotas
```

### Parâmetros do Algoritmo

| Parâmetro | Descrição | Valores Típicos | Impacto |
|-----------|-----------|-----------------|---------|
| `population_length` | Tamanho da população | 50-100 | ↑ Diversidade, ↑ Tempo |
| `max_generations` | Número de gerações | 50-450 | ↑ Convergência, ↑ Qualidade |
| `ratio_elitism` | Taxa de elitismo | 0.03-0.20 | Preservação dos melhores |
| `ratio_mutation` | Taxa de mutação | 0.05-0.50 | ↑ Exploração |
| `tournament_k` | Tamanho do torneio | 2-5 | Pressão seletiva |

### Operadores Genéticos

#### 1. **Crossover RBX (Route-Based Crossover)**

Herda uma rota completa de um pai e complementa com genes do outro:

```python
Pai 1: V1:[1,4,9] V2:[2,7] V3:[3,8,15]
Pai 2: V1:[2,3,8] V2:[1,9] V3:[4,7,15]

Seleciona rota: V2 do Pai 1 → [2,7]
Complementa com Pai 2: [2,7] + [3,8,1,9,4,15] = [2,7,3,8,1,9,4,15]
```

**Características**:
- Preserva estrutura de rotas
- Probabilidade padrão: 50%

#### 2. **Crossover BCRC (Best Cost Route Combination)**

Extrai sub-rota de um pai e insere na melhor posição do outro:

```python
Pai 1: [1, 4, 9, 2, 7, 12]
Pai 2: [3, 8, 15, 5, 11, 6]

Sub-rota: [4, 9, 2] (posições 1-3 do Pai 1)
Base: [3, 8, 15, 5, 11, 6] (Pai 2)

Testa inserções:
  [4,9,2] + [3,8,15,5,11,6]  → Custo: 234
  [3] + [4,9,2] + [8,15,5,11,6]  → Custo: 198 ✓ MELHOR
  [3,8] + [4,9,2] + [15,5,11,6]  → Custo: 245
  ...
```

**Características**:
- Busca local durante crossover
- Otimiza distância Manhattan
- Probabilidade padrão: 50%

#### 3. **Mutação Swap**

Troca posição de dois genes aleatórios:

```python
Original: [1, 4, 9, 2, 7, 12]
            ↑        ↑
Mutante:  [1, 7, 9, 2, 4, 12]
```

#### 4. **Mutação Relocate**

Remove um gene e reinsere em outra posição:

```python
Original: [1, 4, 9, 2, 7, 12]
            remove 9 ─┘  ↑
                         └─ insere aqui
Mutante:  [1, 4, 2, 9, 7, 12]
```

#### 5. **Seleção por Torneio**

```python
População: [Ind1(f=100), Ind2(f=85), Ind3(f=120), Ind4(f=95), ...]

Torneio k=3:
  Competidores: [Ind1(f=100), Ind5(f=110), Ind8(f=92)]
  Vencedor: Ind8 (menor fitness) ✓
```

---

## 📦 Módulos do Sistema

### 1. Core do Algoritmo Genético

#### `genetic_algorithm.py`
**Classe Principal**: `GeneticAlgorithm`

**Responsabilidades**:
- Orquestração do processo evolutivo
- Gerenciamento de população
- Loop de gerações
- Coleta de estatísticas
- Visualização de evolução

**Métodos Principais**:
```python
def __init__(city_code, max_generations, population_length, 
             ratio_elitism, ratio_mutation, tournament_k)
def run(iterator) -> dict[str, any]  # Executa AG completo
def routes_summary() -> dict  # Sumariza rotas finais
def plot_fitness_evolution(save_path) -> None  # Gera gráfico de evolução
```

**Rastreamento de Evolução**:
```python
# Estrutura fitness_history
self.fitness_history = {
    'generation': [],  # Número da geração
    'best': [],        # Melhor fitness da geração
    'avg': [],         # Fitness médio da geração
    'worst': []        # Pior fitness da geração
}
```

**Gráfico de Evolução**:
O método `plot_fitness_evolution()` gera automaticamente um gráfico PNG mostrando:
- **Linha verde**: Evolução do melhor fitness (best)
- **Linha azul tracejada**: Evolução do fitness médio (avg)
- **Linha vermelha semi-transparente**: Evolução do pior fitness (worst)
- **Anotação amarela**: Destaca o melhor valor global encontrado
- **Dimensões**: 12x6 polegadas, resolução 300 DPI
- **Salvo em**: `fitness_balance/i{iterator}_fitness_evolution.png`

#### `c_fitness.py`
**Função Principal**: `calculate_fitness(solution, city) -> float`

**Componentes Avaliados**:
- ✅ Custos de viagem
- ⚠️ Penalidades de capacidade
- 🚨 Penalidades de autonomia
- 📊 Penalidades de eficiência
- 🔴 Penalidades de prioridade

**Pesos Configuráveis**:
```python
CAPACITY_PENALTY = 100        # Soft constraint
AUTONOMY_PENALTY = 200        # Hard constraint
CRITICAL_WEIGHT = 12          # Alta prioridade crítica
HIGH_PRIORITY_WEIGHT = 3      # Média-alta prioridade
COST_EFFICIENCY_WEIGHT = 5    # Penalidade de eficiência
```

### 2. Operadores Genéticos

#### `a_generate_population.py`
- Geração de população inicial aleatória
- Distribuição uniforme de entregas entre veículos

#### `d_crossover.py`
- **RBX**: Route-Based Crossover
- **BCRC**: Best Cost Route Combination
- Probabilidades ajustáveis

#### `e_mutation.py`
- **Swap**: Troca de posições
- **Relocate**: Relocação de gene
- **Light Mutation**: Combinação balanceada

#### `f_selection.py`
- **Elitismo**: Preservação dos melhores
- **Torneio**: Seleção competitiva
- Pressão seletiva configurável

### 3. Utilitários

#### `b_manhattan_distance.py`
```python
def cartesian_to_manhattan(coord1, coord2) -> float
def route_distance(population, center_coords) -> float
```

**Cálculos**:
- Distância Manhattan entre pontos
- Distância total de rota (ida + percurso + retorno)

#### `_encode_decode.py`
```python
def encode_individual(vehicle_routes) -> list[int]
def decode_chromosome(chromosome, deliveries, vehicles) -> list[tuple]
```

**Conversões**:
- Fenótipo (rotas) ↔ Genótipo (cromossomo)
- Decodificação com respeito a capacidades

### 4. Dados e Configuração

#### `delivery_setup/deliveries.py`
**25 Pontos de Entrega**:
```python
{
    1: {"lat": -23.xxx, "lon": -46.xxx, "demand": 8, "priority": 3},
    2: {"lat": -23.xxx, "lon": -46.xxx, "demand": 12, "priority": 2},
    # ...
}
```

**Atributos**:
- `lat`, `lon`: Coordenadas geográficas
- `demand`: Unidades de carga (0-15)
- `priority`: 1 (Normal), 2 (Alta), 3 (Crítica)

#### `delivery_setup/vehicles.py`
**5 Tipos de Veículos**:

| Veículo | Capacidade | Autonomia (M) | Custo/M |
|---------|------------|---------------|---------|
| V1 | 45 unidades | 0.065 | R$ 180 |
| V2 | 30 unidades | 0.045 | R$ 120 |
| V3 | 20 unidades | 0.030 | R$ 85 |
| V4 | 12 unidades | 0.020 | R$ 60 |
| V5 | 6 unidades | 0.012 | R$ 35 |

### 5. Avaliação de Métricas

#### `routes_evaluation.py`
**Classe**: `RouteEvaluator`

**Métricas Calculadas**:

1. **Utilização de Capacidade** (0.0 - 1.0):
   $$\text{Capacity Util} = \frac{\text{Carga Total}}{\text{Capacidade Veículo}}$$

2. **Custos de Viagem** (R$):
   $$\text{Travel Cost} = \text{Distância}_M \times \text{Custo}_M$$

3. **Entregas Críticas** (Pontuação Ponderada):
   $$\text{Critical Score} = \sum_{i} c_i \times (1 - 0.1 \times \text{posição}_i)$$

**Método**:
```python
def metric_summary() -> dict[str, float]:
    return {
        "capacity_utilization_metric_positive": float,
        "travel_costs_metric_negative": float,
        "critical_delivery_metric_positive": float
    }
```

### 6. Visualização de Rotas

#### `itinerary_routes/a_google_maps.py`
**API Google Maps Directions**:
- Cálculo de rotas reais
- Waypoints intermediários (até 23)
- Retorno com polylines codificadas

#### `itinerary_routes/b_polyline_designer.py`
**Decodificação de Polylines**:
- `extract_coordinates()`: Rota única
- `extract_coordinates_by_legs()`: Segmentos coloridos
- Pontos iniciais de cada segmento

#### `itinerary_routes/c_folium_path.py`
**Mapas Interativos HTML**:
```python
class FoliumPath:
    def create_html_map(solution_method: SolutionMethod)
```

**Recursos**:
- Rotas coloridas por segmento
- Marcadores em pontos de entrega
- Zoom e pan interativo
- Exportação HTML

#### `itinerary_routes/d_static_map.py`
**Mapas Estáticos PNG**:
```python
class StaticMapRoute:
    def create_static_map(solution_method: SolutionMethod)
```

**Recursos**:
- Imagens PNG de alta resolução (1200x800)
- Linhas coloridas por segmento
- Marcadores circulares coloridos
- Sem dependência de navegador

#### `itinerary_routes/_solution_type.py`
**Enum de Tipos de Solução**:
```python
class SolutionMethod(Enum):
    FITNESS = "fitness"
    METRICS = "metrics"
```

**Organização de Saídas**:
```
routes_maps/
├── fitness/
│   └── i1_by_fitness_1route_map_45gen.html
└── metrics/
    └── i2_by_metrics_3route_map_150gen.html
```

---

## 🚀 Instalação e Execução

### Pré-requisitos

- Python 3.11+
- Google Maps API Key
- Docker (opcional)

### Instalação Local

```bash
# 1. Clone o repositório
git clone <repository-url>
cd "Desafio Fase 2"

# 2. Crie ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
.\venv\Scripts\Activate.ps1  # Windows

# 3. Instale dependências
pip install -r requirements.txt

# 4. Configure API Keys
# Crie arquivo .env na raiz:
echo "GOOGLE_MAPS_API_KEY=sua_chave_google_aqui" > .env
echo "OPENAI_API_KEY=sua_chave_openai_aqui" >> .env

# 5. Execute o Algoritmo Genético
python run.py

# 6. Execute a Interface LLM (em outro terminal)
cd llm
streamlit run interface.py
```

### Execução com Docker

## Execução com Docker

```bash
# 1. Pull da imagem oficial
docker pull gulimamartins/genetic_algorithm:hospitallogistic

# 2. Criar o container
docker create --name genetic_algorithm -p 8000:8000 gulimamartins/genetic_algorithm:hospitallogistic

# 3. Iniciar o container
docker start genetic_algorithm

# 4. Acompanhar logs (opcional)
docker logs -f genetic_algorithm

# 5. Parar o container
docker stop genetic_algorithm

# 6. Remover o container (opcional)
docker rm genetic_algorithm
```

### Configuração de Parâmetros

Edite `run.py` para ajustar parâmetros:

```python
solutions = Solution(total_iterations=20)

solutions.heuristic_loop(
    city_code="SP",
    # População: varia de 100 a 400 indivíduos
    population_length=(120, 150, 180, 200, 220, 250, 280, 300, 320, 350,
                      100, 140, 170, 210, 240, 270, 310, 340, 380, 400),
    
    # Gerações: fixado em 2000 para garantir convergência
    max_generations=(2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000,
                    2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000),
    
    # Elitismo: 2% a 8% da população
    ratio_elitism=(0.02, 0.03, 0.03, 0.04, 0.04, 0.05, 0.05, 0.06, 0.06, 0.08,
                  0.03, 0.04, 0.05, 0.05, 0.06, 0.04, 0.05, 0.06, 0.07, 0.08),
    
    # Mutação: 5% a 15% de probabilidade
    ratio_mutation=(0.12, 0.10, 0.08, 0.10, 0.08, 0.10, 0.08, 0.10, 0.12, 0.15,
                   0.05, 0.06, 0.08, 0.10, 0.12, 0.07, 0.09, 0.11, 0.13, 0.15),
    
    # Torneio: 2 a 4 competidores
    tournament_k=(2, 2, 3, 3, 3, 3, 3, 4, 4, 4,
                 2, 3, 3, 3, 4, 2, 3, 3, 4, 4)
)
```

**Experimento Sistemático de Hiperparâmetros**:
- ✅ **20 configurações distintas** para análise comparativa robusta
- ✅ **Exploração balanceada**: varia população, elitismo, mutação e pressão seletiva
- ✅ **Convergência garantida**: 2000 gerações asseguram exploração completa
- ✅ **Cada tupla** deve ter tamanho igual a `total_iterations`
- ✅ **Design experimental**: permite identificar configuração ótima para o problema Einstein

### Fluxo de Execução Completo

```
1. PREPARAÇÃO
   ├─ Carregar dados (entregas, veículos, coordenadas)
   └─ Configurar 20 arranjos de parâmetros do AG

2. OTIMIZAÇÃO (run.py) - Algoritmo Genético
   ├─ Executar 20 iterações com configurações distintas
   │  ├─ Cada iteração: 2000 gerações de evolução
   │  ├─ Variação sistemática de hiperparâmetros
   │  └─ População: 100-400, Elitismo: 2-8%, Mutação: 5-15%
   │
   ├─ Selecionar melhores soluções
   │  ├─ best_by_fitness: minimiza função objetivo
   │  └─ best_by_metrics: maximiza KPIs ponderados
   │
   ├─ Gerar visualizações georreferenciadas
   │  ├─ Rotas reais via Google Maps API
   │  ├─ Mapas interativos HTML (Folium)
   │  └─ Mapas estáticos PNG (1200x800px)
   │
   ├─ Gerar Base de Conhecimento (RAG)
   │  ├─ Processar 11 documentos .md (~15k palavras)
   │  ├─ Chunking: 450 caracteres, overlap 100
   │  ├─ Embeddings: OpenAI text-embedding-ada-002
   │  └─ Vector Store: Chroma DB persistente
   │
   └─ Salvar solutions_data.json
      ├─ best_solutions: {best_by_fitness, best_by_metrics}
      ├─ all_solutions: todas as 20 iterações
      ├─ routes_sequences: sequências com nomes de hospitais
      └─ metadata: {vehicle_data, delivery_data, depot_coords}

3. INTERFACE LLM (llm/interface.py) - Assistente Conversacional
   ├─ Auto-load: solutions_data.json
   ├─ Inicializar clientes
   │  ├─ LangChainClient: RAG + Similarity Search (k=4)
   │  └─ OpenAIClient: GPT-4o-mini (temp=0.2)
   │
   ├─ Conectar Vector Store: Chroma DB
   ├─ Interface Web: Streamlit (http://localhost:8501)
   └─ Chat History: Session State persistente

4. LOOP CONVERSACIONAL
   ├─ Usuário: pergunta em linguagem natural
   │
   ├─ Sistema RAG:
   │  ├─ Embedding da query
   │  ├─ Similarity search no Chroma (top-4 docs)
   │  ├─ Recuperar contexto relevante
   │  └─ Injetar solutions_data.json
   │
   ├─ GPT-4o-mini:
   │  ├─ Processar: contexto + dados + pergunta
   │  ├─ Gerar resposta fundamentada
   │  └─ Limitar: 1500 tokens
   │
   └─ Output:
      ├─ Resposta contextualizada
      └─ Fontes: documentos .md usados
```

**Comandos de Execução**:

```bash
# ========================================
# FASE 1: OTIMIZAÇÃO (Tempo: ~2-8 horas)
# ========================================

# Ativar ambiente virtual
.\venv\Scripts\Activate.ps1  # Windows PowerShell
# ou
source venv/bin/activate     # Linux/Mac

# Executar algoritmo genético (20 iterações × 2000 gerações)
python run.py

# Outputs gerados:
# ✓ llm/solutions_data.json (dados das soluções)
# ✓ llm/chroma/ (vector database)
# ✓ itinerary_routes/routes_maps/fitness/*.html (mapas interativos)
# ✓ itinerary_routes/routes_maps/metrics/*.html
# ✓ itinerary_routes/routes_maps/fitness/*.png (mapas estáticos)
# ✓ itinerary_routes/routes_maps/metrics/*.png
# ✓ fitness_balance/i*_fitness_evolution.png (gráficos de evolução)

# ========================================
# FASE 2: INTERFACE LLM (Terminal separado)
# ========================================

cd llm
streamlit run interface.py

# Acesse no navegador:
# http://localhost:8501

# Interface disponibiliza:
# • Chat conversacional em português
# • Consultas sobre algoritmo genético
# • Análise das 20 soluções encontradas
# • Explicações de métricas e rotas
# • Comparação de configurações
```

**Exemplos Práticos de Consultas no Chat**:

1. **Análise de Resultados**:
   - "Qual foi a melhor solução entre as 20 iterações?"
   - "Compare o desempenho da iteração 5 vs iteração 12"
   - "Qual configuração de parâmetros teve melhor fitness?"
   - "Mostre estatísticas de utilização de capacidade"

2. **Entendimento do Algoritmo**:
   - "Como funciona o crossover BCRC?"
   - "Explique a função de fitness em detalhes"
   - "Qual a diferença entre RBX e BCRC?"
   - "Por que usar distância Manhattan ao invés de euclidiana?"

3. **Rastreabilidade de Rotas**:
   - "Mostre a sequência completa da rota 1"
   - "Quais hospitais foram visitados na rota 3?"
   - "Liste todas as entregas críticas e suas posições"
   - "Qual veículo fez mais viagens?"

4. **Otimização e Decisão**:
   - "Por que a solução por metrics é diferente da por fitness?"
   - "Quais entregas têm prioridade crítica?"
   - "Sugira melhorias na configuração de parâmetros"
   - "Explique o trade-off entre custo e prioridade"

5. **Dados Técnicos**:
   - "Quantas unidades de carga cada veículo suporta?"
   - "Liste todos os hospitais Einstein no sistema"
   - "Qual a autonomia do veículo V3?"
   - "Mostre a demanda total de todas as entregas"

---

## 🤖 Sistema LLM/RAG - Assistente Inteligente

### Visão Geral da Arquitetura

O sistema integra **Retrieval-Augmented Generation (RAG)** com **Large Language Models (LLM)** para criar um assistente conversacional especializado em logística hospitalar. Esta funcionalidade representa a **principal inovação da versão 2.0**.

```
┌─────────────────────────────────────────────────────────┐
│              STREAMLIT INTERFACE                        │
│         (interface.py - Frontend Web)                   │
└──────────────────────┬──────────────────────────────────┘
                       │
         ┌─────────────┴─────────────┐
         ▼                           ▼
┌──────────────────┐    ┌──────────────────┐
│  LangChain RAG   │    │   OpenAI GPT-4   │
│ (langchain_setup)│◄───┤  (openai_setup)  │
└────────┬─────────┘    └──────────────────┘
         │
         ▼
┌──────────────────────────────────────────┐
│      CHROMA VECTOR DATABASE              │
│  (chroma_db.py - Embeddings Storage)     │
└────────────┬─────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────┐
│        KNOWLEDGE BASE (logistic_infos_docs/)            │
├─────────────────────────────────────────────────────────┤
│ • pipeline.md - Fluxo completo do AG                    │
│ • generate_population.md - Geração de indivíduos        │
│ • manhattan_distance.md - Cálculo de distâncias         │
│ • fitness.md - Função de aptidão detalhada              │
│ • crossover.md - Operadores de cruzamento               │
│ • mutation.md - Operadores de mutação                   │
│ • selection.md - Métodos de seleção                     │
│ • routes_evaluation.md - Métricas de avaliação          │
│ • deliveries.md - 25 pontos de entrega                  │
│ • vehicles.md - 5 tipos de veículos                     │
│ • solution_explanation.md - Estrutura de soluções       │
└─────────────────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────┐
│         SOLUTIONS DATA (solutions_data.json)            │
├─────────────────────────────────────────────────────────┤
│ • best_by_fitness - Melhor solução por fitness          │
│ • best_by_metrics - Melhor solução por métricas         │
│ • all_solutions - Todas as 20 iterações                 │
│ • routes_sequences - Sequências com nomes reais         │
│ • metadata - Dados de veículos, entregas, depot         │
└─────────────────────────────────────────────────────────┘
```

### Componentes do Sistema LLM

#### 1. **Base de Conhecimento (11 documentos .md)**

A base de conhecimento foi **expandida significativamente na versão 2.0**, incluindo documentação detalhada de todos os módulos do algoritmo genético:

| Documento | Descrição | Conteúdo Principal |
|-----------|-----------|-------------------.|
| `pipeline.md` | Fluxo completo do AG | 7 fases do algoritmo, loop evolutivo, critérios de seleção |
| `generate_population.md` | Geração inicial | Distribuição aleatória, validação de restrições |
| `manhattan_distance.md` | Cálculo de distâncias | Métrica urbana, complexidade O(1), fórmulas |
| `fitness.md` | Função de aptidão | 5 componentes, pesos, penalidades, exemplos práticos |
| `crossover.md` | Cruzamento genético | RBX, BCRC, preservação de rotas, probabilidades |
| `mutation.md` | Mutação | Swap, Relocate, Light Mutation, diversificação |
| `selection.md` | Seleção | Elitismo, Torneio, pressão seletiva |
| `routes_evaluation.md` | Métricas | Capacidade, custos, prioridades críticas |
| `deliveries.md` | Dados de entregas | 25 pontos, demandas (230 unidades), prioridades |
| `vehicles.md` | Frota heterogênea | 5 tipos, capacidades (6-45 un), custos, autonomia |
| `solution_explanation.md` | Estrutura de soluções | Campos JSON, routes_sequences, exemplos de análise |

**Total**: ~15.000 palavras de documentação técnica otimizada para RAG.

#### 2. **Chroma Vector Database** (`chroma_db.py`)

**Responsabilidades**:
- 📦 **Carregamento**: Lê todos os arquivos .md da base de conhecimento
- ✂️ **Chunking**: Divide textos em fragmentos de 450 caracteres (overlap: 100)
- 🧮 **Embeddings**: Gera vetores usando OpenAI Embeddings (text-embedding-ada-002)
- 💾 **Persistência**: Armazena vetores no Chroma DB local
- 🔍 **Recuperação**: Similarity search com k=4 documentos mais relevantes

**Implementação**:
```python
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

# Configuração otimizada para contexto técnico
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=450,        # Tamanho ideal para conceitos técnicos
    chunk_overlap=100,     # Mantém contexto entre chunks
    length_function=len,
    is_separator_regex=False,
)
```

#### 3. **LangChain RAG Client** (`langchain_setup.py`)

**Fluxo RAG**:
1. 🔎 **Query**: Recebe pergunta do usuário
2. 🎯 **Similarity Search**: Busca top-4 documentos relevantes no Chroma
3. 📝 **Context Building**: Concatena documentos recuperados
4. 🤖 **Prompt Engineering**: Injeta contexto + soluções + pergunta
5. 💬 **GPT Response**: Envia para OpenAI e retorna resposta contextualizada
6. 📚 **Source Attribution**: Adiciona fontes dos documentos usados

**Template de Prompt**:
```python
prompt = f"""
Responda como um assistente especialista em logística e roteirização de veículos.
Seja objetivo e direto ao ponto, como numa conversa profissional.
Use as informações fornecidas no contexto para fundamentar suas respostas.

{context}  # Documentação técnica do Chroma

Soluções do algoritmo genético:
{solutions_metadata}  # JSON com resultados reais

Pergunta: {question}
"""
```

#### 4. **OpenAI GPT-4o-mini Client** (`openai_setup.py`)

**Configuração**:
- 🧠 **Modelo**: gpt-4o-mini (rápido, custo-efetivo)
- 🌡️ **Temperature**: 0.2 (respostas mais determinísticas)
- 📏 **Max Tokens**: 1500 (respostas detalhadas mas concisas)

#### 5. **Streamlit Interface** (`interface.py`)

**Funcionalidades**:
- 💬 **Chat interativo**: Interface conversacional estilo ChatGPT
- 📊 **Auto-loading**: Carrega `solutions_data.json` automaticamente
- 🧹 **Limpar histórico**: Botão para reiniciar conversa
- 💾 **Session state**: Mantém histórico durante a sessão
- 🎨 **UI responsiva**: Design limpo com streamlit-chat

**Exemplo de Uso**:
```bash
# Terminal 1: Gerar soluções e vector store
python run.py

# Terminal 2: Lançar interface
cd llm
streamlit run interface.py
# Acesse: http://localhost:8501
```

### Exemplos de Consultas Inteligentes

#### 1. **Análise de Soluções**
```
Usuário: "Qual foi a melhor solução encontrada pelo algoritmo?"

Assistente: "A melhor solução por fitness foi encontrada na iteração 5,
geração 1847, com fitness de 856.34. Esta solução utilizou 8 rotas
distribuídas entre 5 veículos, com utilização de capacidade de 87%
e custo total de viagem de R$ 1.234,56. A solução priorizou 4 entregas
críticas nas primeiras rotas."
```

#### 2. **Explicação Técnica**
```
Usuário: "Como funciona o operador de crossover BCRC?"

Assistente: "O BCRC (Best Cost Route Combination) extrai uma sub-rota
de um pai e testa todas as posições possíveis de inserção no outro pai,
selecionando a que resulta em menor distância Manhattan. Este operador
combina exploração (herança genética) com otimização local (busca da
melhor posição). É usado em 50% dos cruzamentos, alternando com RBX."
```

#### 3. **Rastreabilidade de Rotas**
```
Usuário: "Mostre a sequência da rota 1 da melhor solução"

Assistente: "Rota 1 (Veículo V1):
Centro de Distribuição → Einstein Alphaville (Entrega #23) → 
Einstein Morumbi (Entrega #5) → Einstein Ibirapuera (Entrega #12) →
Centro de Distribuição

Total: 3 entregas, 43 unidades de carga, distância: 45.3 km"
```

#### 4. **Comparação de Estratégias**
```
Usuário: "Qual a diferença entre best_by_fitness e best_by_metrics?"

Assistente: "best_by_fitness minimiza a função objetivo completa
(custo + penalidades), focando em viabilidade operacional. 
best_by_metrics otimiza uma pontuação ponderada de 3 KPIs:
utilização de capacidade (20%), custos de viagem (40%) e
entregas críticas (40%). Use fitness para operação diária
e metrics para planejamento estratégico."
```

### Integração com Algoritmo Genético

**Geração Automática do Vector Store**:

O `run.py` executa automaticamente a geração do vector store após otimização:

```python
from llm.chroma_db import main as generate_data_store

print("Generating vector store for RAG system...")
generate_data_store()  # Processa todos os .md e cria embeddings

# Salva soluções com routes_sequences
solutions_output = {
    'best_solutions': best_solutions_converted,
    'all_solutions': solutions.solutions,
    'metadata': {...}
}

with open('llm/solutions_data.json', 'w') as f:
    json.dump(solutions_output, f, indent=4, ensure_ascii=False)
```

**Routes Sequences com Nomes Reais**:

Nova funcionalidade que mapeia coordenadas para nomes de hospitais:

```python
def get_unit_name(delivery_id, delivery_data):
    """Busca nome real do hospital usando einstein_units"""
    coords = (delivery_data[delivery_id]['lat'], 
              delivery_data[delivery_id]['lon'])
    return hospitalar_units_lat_lon.get(coords, f"Entrega #{delivery_id}")

def create_route_sequences(solution, delivery_data):
    """Gera sequências legíveis: Centro -> Hospital A -> Hospital B -> Centro"""
    return {
        route_id: f"Centro de Distribuição -> " + 
                  " -> ".join([f"{get_unit_name(did, delivery_data)} (Entrega #{did})" 
                              for did, _ in route_deliveries]) + 
                  " -> Centro de Distribuição"
        for route_id, route_deliveries in solution['routes_metadata'].items()
    }
```

### Benefícios da Versão 2.0

#### ✨ **Transparência**
- Usuários entendem **como** e **por que** o algoritmo tomou decisões
- Explicações baseadas em documentação técnica real
- Rastreabilidade completa com nomes de hospitais

#### 🚀 **Produtividade**
- Sem necessidade de ler código-fonte
- Respostas instantâneas sobre qualquer aspecto do sistema
- Interface conversacional natural

#### 📊 **Análise de Resultados**
- Comparação automática entre 20 configurações
- Identificação de melhores estratégias
- Insights sobre trade-offs (custo vs prioridade vs capacidade)

#### 🧠 **Tomada de Decisão**
- Recomendações contextualizadas
- Explicação de métricas complexas
- Sugestões de melhorias baseadas em dados reais

---

## 📊 Resultados e Visualizações

### Saídas do Sistema

#### 1. **Console Output**

```
============================================================
Iniciando Algoritmo Genético - Cidade: SP
População: 100 | Gerações: 250
============================================================

Geração 1   | Melhor: 1234.56 | Média: 1567.89 | Pior: 2345.67
Geração 2   | Melhor: 1198.23 | Média: 1445.12 | Pior: 2123.45
...
Geração 250 | Melhor: 856.34 | Média: 923.45 | Pior: 1234.56

============================================================
Evolução Concluída!
============================================================
Melhor solução encontrada na geração 187
Fitness: 856.34

Decodificando melhor solução...
Total de entregas: 25
Entregas atribuídas: 25
Número de rotas: 8

Distribuição por veículo:
  Veículo V1: 2 viagens, 10 entregas
  Veículo V2: 2 viagens, 7 entregas
  Veículo V3: 2 viagens, 5 entregas
  Veículo V4: 1 viagem, 2 entregas
  Veículo V5: 1 viagem, 1 entrega

Detalhes das rotas:
  Rota 1 (Veículo V1): 5 entregas | Carga total: 43
    Entregas (ID): [1, 4, 6, 9, 15]
  ...
```

#### 2. **Estrutura Completa da Solução**

```python
{
    "iteration": 3,
    "generation": 241,
    "fitness": 923.44,
    "routes_metadata": {
        1: [(23, 'V1'), (2, 'V1'), (15, 'V1')],
        # ...
    },
    "routes_sequences": {
        1: "Centro de Distribuição -> Einstein Alphaville (Entrega #23) -> Einstein Alphaville (Entrega #2) -> Einstein Alphaville (Entrega #15) -> Centro de Distribuição",
        # ...
    },
    "metrics": {
        "capacity_utilization_metric_positive": 0.87,
        "travel_costs_metric_negative": 1234.56,
        "critical_delivery_metric_positive": 8.4
    }
}
```

**Campo `routes_sequences`**:
- ✅ Rastreabilidade automática com nomes de hospitais
- ✅ Formato legível para humanos
- ✅ Gerado usando `address_routes.einstein_units`
- ✅ Validação rápida da lógica geográfica

#### 3. **Mapas Interativos (HTML)**

- 📍 **Marcadores** nos pontos de entrega
- 🎨 **Linhas coloridas** por segmento
- 🔍 **Zoom e pan** interativos
- 📝 **Popups** com informações

**Exemplo de Arquivo**:
```
itinerary_routes/routes_maps/fitness/i5_by_fitness_1route_map_450gen.html
```

#### 4. **Mapas Estáticos (PNG)**

- 📸 Alta resolução (1200x800px)
- 🎨 Cores distintas por segmento
- 🔴 Marcadores circulares coloridos
- 📊 Ideal para relatórios

**Exemplo de Arquivo**:
```
itinerary_routes/routes_maps/fitness/i5_by_fitness_1route_map_450gen.png
```

#### 5. **Gráficos de Evolução do Fitness (PNG)**

- 📈 **Visualização da convergência** do algoritmo genético
- 📊 **Três curvas simultâneas**:
  - **Best Fitness** (verde, sólida): Melhor solução de cada geração
  - **Average Fitness** (azul, tracejada): Qualidade média da população
  - **Worst Fitness** (vermelho, semi-transparente): Pior indivíduo
- 🎯 **Anotação automática**: Destaca melhor valor global (geração + fitness)
- 📐 **Alta resolução**: 300 DPI, 12x6 polegadas (3600x1800 pixels)
- 🔍 **Grade**: Auxilia leitura precisa dos valores
- 📁 **Salvo em**: `fitness_balance/i{iterator}_fitness_evolution.png`

**Utilidade**:
- Verificar **convergência** do algoritmo (platô na curva best)
- Identificar **estagnação prematura** (convergência antes de 2000 gerações)
- Avaliar **diversidade populacional** (distância entre best e worst)
- Comparar **eficácia de hiperparâmetros** entre iterações
- Detectar **overfitting** (best melhora mas avg piora)

**Exemplo de Arquivo**:
```
fitness_balance/i5_fitness_evolution.png
fitness_balance/i12_fitness_evolution.png
```

**Interpretação**:
- **Curva descendente suave**: Convergência saudável
- **Platô precoce**: Pode indicar necessidade de mais mutação
- **Oscilações**: Diversidade preservada, boa exploração
- **Best e Avg próximos**: População homogênea (fim da evolução)
- **Best muito abaixo de Avg**: Elitismo funcionando bem

### Interpretação de Resultados

#### Comparação: Fitness vs Metrics

O sistema gera duas soluções:

1. **Melhor por Fitness**:
   - Minimiza função objetivo (custo + penalidades)
   - Foco em viabilidade e custo operacional
   - Pode não ser ótimo em métricas específicas

2. **Melhor por Métricas**:
   - Pontuação ponderada de capacidade, custo e prioridade
   - Ajustável via pesos: `capacity_weight`, `travel_weight`, `critical_weight`
   - Foco em equilíbrio de KPIs

**Quando usar cada uma**:
- **Fitness**: Operação do dia-a-dia, minimizar custos
- **Metrics**: Planejamento estratégico, balanceamento de objetivos

#### Análise dos Gráficos de Evolução do Fitness

Os gráficos gerados pelo sistema (`fitness_balance/i*_fitness_evolution.png`) são ferramentas cruciais para avaliar o desempenho do algoritmo genético:

**Padrões Saudáveis de Convergência**:
1. **Curva Best (verde) descendente suave**: Indica convergência progressiva sem estagnação
2. **Platô após 1500+ gerações**: Algoritmo explorou suficientemente o espaço de busca
3. **Best e Average (azul) convergindo**: População está se homogeneizando ao redor de boas soluções
4. **Gap entre Best e Worst (vermelho)**: Mostra diversidade populacional mantida

**Sinais de Alerta**:
1. **Platô antes de 500 gerações**: Possível convergência prematura
   - Solução: Aumentar `ratio_mutation` ou reduzir `ratio_elitism`
2. **Best muito distante de Average**: População não está evoluindo uniformemente
   - Solução: Aumentar `tournament_k` para pressão seletiva maior
3. **Oscilações bruscas em Best**: Instabilidade no processo evolutivo
   - Solução: Reduzir `ratio_mutation` ou aumentar `ratio_elitism`
4. **Average estagnado mas Best melhorando**: Elitismo excessivo
   - Solução: Reduzir `ratio_elitism`

**Comparação entre Iterações**:
- Compare os 20 gráficos gerados para identificar qual configuração teve:
  - **Melhor convergência**: Menor fitness final
  - **Convergência mais rápida**: Platô em menos gerações
  - **Maior estabilidade**: Curvas mais suaves
  - **Melhor exploração**: Diversidade mantida por mais tempo

**Uso Prático**:
```python
# Exemplo: Analisar se iteração 5 convergiu bem
# Observar: fitness_balance/i5_fitness_evolution.png
# - Best fitness final: ~856.34 (bom)
# - Convergência em: ~1847 gerações (ótimo)
# - Gap Best-Worst ao final: pequeno (população homogênea)
# Conclusão: Configuração eficaz para o problema
```

---

## 🛠️ Tecnologias Utilizadas

### Core

| Tecnologia | Versão | Uso |
|------------|--------|-----|
| Python | 3.11 | Linguagem principal |
| NumPy | 2.4.0 | Operações numéricas |

### APIs e Geolocalização

| Tecnologia | Versão | Uso |
|------------|--------|-----|
| Google Maps API | - | Rotas reais e geocoding |
| googlemaps | 4.10.0 | Cliente Python Google Maps |
| polyline | 2.0.4 | Codificação/decodificação polylines |

### Visualização e Geolocalização

| Tecnologia | Versão | Uso |
|------------|--------|-----|
| Folium | 0.20.0 | Mapas interativos HTML (Leaflet.js) |
| staticmap | 0.5.7 | Mapas estáticos PNG (alta resolução) |
| matplotlib | 3.9.+ | Gráficos de evolução do fitness |
| Pillow | 12.1.0 | Processamento e manipulação de imagens |
| xyzservices | 2025.11.0 | Provedores de tiles para mapas base |

### LLM e RAG

| Tecnologia | Versão | Uso |
|------------|--------|-----|
| OpenAI API | - | GPT-4o-mini para respostas |
| LangChain | 0.3.16 | Framework RAG |
| langchain-community | 0.3.16 | Integrações LangChain |
| langchain-openai | 0.3.0 | Cliente OpenAI |
| langchain-chroma | 0.2.1 | Vector store Chroma |
| Chroma | 0.6.4 | Banco de dados vetorial |
| Streamlit | 1.42.0 | Interface web |
| streamlit-chat | 0.2.0 | Componente de chat |

### Infraestrutura

| Tecnologia | Versão | Uso |
|------------|--------|-----|
| Docker | - | Containerização |
| python-dotenv | 1.2.1 | Variáveis de ambiente |

### Estrutura Completa de Dependências

```
# Core
attrs==25.4.0              # Classes e decorators
numpy==2.4.0               # Operações numéricas
python-dotenv==1.2.1       # Variáveis de ambiente

# LLM e RAG
openai==1.59.7             # Cliente OpenAI
langchain==0.3.16          # Framework RAG
langchain-community==0.3.16  # Integrações
langchain-openai==0.3.0    # Cliente OpenAI LangChain
langchain-chroma==0.2.1    # Vector store
langchain-core==0.3.28     # Core LangChain
langchain-text-splitters==0.3.4  # Divisão de textos
chroma==0.2.0              # Vector DB (compat)
chromadb==0.6.4            # Vector database
streamlit==1.42.0          # Interface web
streamlit-chat==0.2.0      # Chat UI

# Visualização
branca==0.8.2              # Templating para Folium
certifi==2025.11.12        # Certificados SSL
cffi==2.0.0                # Interface C para Python
charset-normalizer==3.4.4  # Detecção de encoding
folium==0.20.0             # Mapas interativos
googlemaps==4.10.0         # API Google Maps
h11==0.16.0                # HTTP/1.1 client
idna==3.11                 # Suporte a domínios internacionais
Jinja2==3.1.6              # Template engine
MarkupSafe==3.0.3          # Escape de strings HTML
matplotlib==3.9.3          # Gráficos de evolução do fitness
numpy==2.4.0               # Operações numéricas
outcome==1.3.0.post0       # Resultados assíncronos
packaging==25.0            # Parsing de versões
pillow==12.1.0             # Processamento de imagens
polyline==2.0.4            # Codificação polylines
pycparser==2.23            # Parser C
PySocks==1.7.1             # Cliente SOCKS
python-dotenv==1.2.1       # Variáveis de ambiente
requests==2.32.5           # Cliente HTTP
sniffio==1.3.1             # Detecção async
sortedcontainers==2.4.0    # Containers ordenados
staticmap==0.5.7           # Mapas estáticos
trio==0.32.0               # Async I/O
trio-websocket==0.12.2     # WebSocket para Trio
typing_extensions==4.15.0  # Extensões de tipos
urllib3==2.6.2             # Cliente HTTP low-level
websocket-client==1.9.0    # Cliente WebSocket
wsproto==1.3.2             # Protocolo WebSocket
xyzservices==2025.11.0     # Provedores de tiles
```

---

## 📈 Análise de Complexidade

### Complexidade Computacional

#### Algoritmo Genético

- **População**: $N$ indivíduos
- **Gerações**: $G$ iterações
- **Entregas**: $D$ pontos (25)
- **Veículos**: $V$ tipos (5)

**Complexidade Total**:
$$O(N \times G \times D^2)$$

**Detalhamento**:
- **Avaliação de fitness**: $O(D^2)$ por indivíduo (distâncias)
- **Seleção por torneio**: $O(N \times k)$
- **Crossover BCRC**: $O(D^2)$ (busca de melhor posição)
- **Decodificação**: $O(D \times V)$

### Escalabilidade

| Cenário | Entregas | Veículos | Tempo Estimado* |
|---------|----------|----------|-----------------|
| **Pequeno** | 10-15 | 3 | ~30s |
| **Médio** | 20-30 | 5 | ~2-5min |
| **Grande** | 40-50 | 7 | ~10-20min |
| **Muito Grande** | 100+ | 10+ | ~1-3h |

*Para 100 gerações, população de 50

### Otimizações Implementadas

1. **Distância Manhattan**: $O(1)$ vs $O(\sqrt{n})$ Euclidiana
2. **Codificação linear**: Facilita crossover e mutação
3. **Elitismo**: Preserva convergência
4. **Decodificação gulosa**: $O(D \times V)$ ao invés de exaustiva

---

## 🎓 Conceitos Teóricos

### Problema de Roteamento de Veículos (VRP)

Este projeto aborda uma variante complexa do VRP clássico:

**Características**:
- **CVRP**: Capacitated VRP (restrição de capacidade)
- **VRPTW**: VRP with Time Windows (prioridades implícitas)
- **HFVRP**: Heterogeneous Fleet VRP (frota mista)
- **MDVRP**: Multiple Depot VRP (depot central + retorno)

**Complexidade NP-Hard**:
- Espaço de busca cresce fatorialmente: $O(n!)$
- Número de soluções viáveis: Exponencial
- Algoritmos exatos inviáveis para $n > 20$

### Por que Algoritmos Genéticos?

**Vantagens**:
- ✅ Escalam bem para problemas grandes
- ✅ Flexibilidade na função objetivo
- ✅ Não exigem gradiente (fitness arbitrário)
- ✅ Exploração global do espaço de busca
- ✅ Facilmente paralelizáveis

**Desvantagens**:
- ⚠️ Não garantem solução ótima
- ⚠️ Sensíveis a hiperparâmetros
- ⚠️ Necessitam tuning cuidadoso

### Inspiração Biológica

| Conceito Biológico | Análogo Computacional |
|--------------------|------------------------|
| População | Conjunto de soluções |
| Indivíduo | Uma solução candidata |
| Cromossomo | Codificação da solução |
| Gene | Componente da solução (entrega) |
| Fitness | Qualidade da solução |
| Seleção Natural | Escolha dos melhores |
| Reprodução | Crossover |
| Mutação | Perturbação aleatória |
| Geração | Iteração do algoritmo |

---

## 🔬 Trabalhos Futuros

### Melhorias Potenciais

1. **Otimizações de Algoritmo**:
   - Implementar AG híbrido com busca local (Memetic Algorithm)
   - Adicionar operador de mutação adaptativo
   - Paralelização da avaliação de fitness (multiprocessing)

2. **Modelagem mais Realista**:
   - Integrar janelas de tempo reais (horários de funcionamento)
   - Considerar tráfego em tempo real (Google Maps Traffic API)
   - Modelar tempo de carga/descarga
   - Restrições de tipo de veículo por entrega

3. **Melhorias no Sistema LLM/RAG**:
   - Fine-tuning de modelo para domínio logístico
   - Expansão da base de conhecimento (documentação)
   - Suporte a multi-idiomas
   - Histórico persistente de conversas
   - Geração automática de relatórios
   - Sugestões proativas de otimizações

4. **Expansão do Sistema LLM**:
   - Fine-tuning de modelo GPT para domínio logístico hospitalar
   - Suporte multilíngue (inglês, espanhol)
   - Histórico persistente de conversas em banco de dados
   - Geração automática de relatórios PDF/Excel
   - Sugestões proativas de otimizações
   - Análise comparativa automática das 20 configurações
   - Alertas inteligentes para violações de restrições

5. **Visualizações Avançadas**:
   - Dashboard interativo com métricas em tempo real (Plotly/Dash)
   - Animações de evolução do AG (gerações 1→2000)
   - ✅ **Gráficos de convergência (fitness vs gerações) - IMPLEMENTADO**
   - Análise comparativa visual entre as 20 configurações testadas
   - Heatmaps de utilização de veículos
   - Comparação lado-a-lado de soluções (fitness vs metrics)
   - Integração de mapas na interface do chat Streamlit
   - Timeline interativo de entregas por rota
   - Gráficos de Pareto (trade-off custo vs prioridades)

6. **Machine Learning**:
   - Aprendizado de hiperparâmetros via Bayesian Optimization
   - Predição de fitness via regressão (acelerar avaliação)
   - Reinforcement Learning para guiar busca

7. **Extensões de Negócio**:
   - Multi-objetivo explícito (Pareto frontier)
   - Planejamento multi-dia
   - Incerteza nas demandas (modelo estocástico)
   - Integração com sistemas de gestão (ERP)

---

## 📚 Referências

### Artigos Acadêmicos

1. Goldberg, D. E. (1989). *Genetic Algorithms in Search, Optimization, and Machine Learning*. Addison-Wesley.

2. Laporte, G. (2009). Fifty years of vehicle routing. *Transportation Science*, 43(4), 408-416.

3. Potvin, J. Y. (1996). Genetic algorithms for the traveling salesman problem. *Annals of Operations Research*, 63(3), 337-370.

4. Prins, C. (2004). A simple and effective evolutionary algorithm for the vehicle routing problem. *Computers & Operations Research*, 31(12), 1985-2002.

### Recursos Online

- [Google Maps Directions API Documentation](https://developers.google.com/maps/documentation/directions)
- [Folium Documentation](https://python-visualization.github.io/folium/)
- [CVRPLIB - Benchmark Instances](http://vrp.galgos.inf.puc-rio.br/index.php/en/)

---

## 👥 Equipe

Desenvolvido como parte do projeto de Pós-Graduação em Inteligência Artificial - FIAP.

**Instituição**: Hospital Albert Einstein (Caso de Estudo)

---

## 📄 Licença

Este projeto é desenvolvido para fins educacionais e de pesquisa.

<div align="center">

**🧬 Desenvolvido com Algoritmos Genéticos e ❤️ para Logística Hospitalar**

</div>

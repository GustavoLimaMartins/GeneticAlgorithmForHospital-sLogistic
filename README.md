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
   │  └─ Registrar melhor solução
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
   └─ Gerar visualizações
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

**Métodos Principais**:
```python
def __init__(city_code, max_generations, population_length, 
             ratio_elitism, ratio_mutation, tournament_k)
def run() -> dict[str, any]  # Executa AG completo
def routes_summary() -> dict  # Sumariza rotas finais
```

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

```bash
# 1. Build da imagem
docker build -t einstein_logistic_fiap_fase2 .

# 2. Execute o container
docker run --name genetic_algorithm \
  -v $(pwd)/itinerary_routes/routes_maps:/app/itinerary_routes/routes_maps \
  einstein_logistic_fiap_fase2
```

### Configuração de Parâmetros

Edite `run.py` para ajustar parâmetros:

```python
solutions = Solution(total_iterations=5)

solutions.heuristic_loop(
    city_code="SP",
    population_length=(100, 50, 100, 50, 80),
    max_generations=(50, 150, 250, 350, 450),
    ratio_elitism=(0.1, 0.2, 0.05, 0.03, 0.15),
    ratio_mutation=(0.05, 0.25, 0.5, 0.3, 0.1),
    tournament_k=(2, 5, 3, 3, 2)
)
```

**Múltiplas Iterações**:
- Testa diferentes combinações de parâmetros
- Cada tupla deve ter tamanho igual a `total_iterations`
- Permite exploração do espaço de hiperparâmetros

### Fluxo de Execução Completo

```
1. PREPARAÇÃO
   ├─ Carregar dados (entregas, veículos, coordenadas)
   └─ Configurar parâmetros do AG

2. OTIMIZAÇÃO (run.py)
   ├─ Executar 5 iterações do AG
   ├─ Selecionar melhores soluções (fitness vs metrics)
   ├─ Gerar mapas das rotas (Google Maps + Folium)
   ├─ Criar vector store (Chroma DB)
   └─ Salvar solutions_data.json

3. INTERFACE LLM (llm/interface.py)
   ├─ Carregar solutions_data.json
   ├─ Inicializar LangChain + OpenAI
   ├─ Conectar ao Chroma DB
   └─ Abrir chat interativo (Streamlit)

4. CONSULTAS
   ├─ Usuário faz pergunta
   ├─ Sistema busca contexto relevante (RAG)
   ├─ GPT gera resposta contextualizada
   └─ Exibe resposta com fontes
```

**Comandos Sequenciais**:
```bash
# Terminal 1: Executar otimização
python run.py
# Output: solutions_data.json + mapas + vector store

# Terminal 2: Iniciar interface
cd llm
streamlit run interface.py
# Acesse: http://localhost:8501
```

**Exemplo de Consultas no Chat**:
- "Qual a melhor solução encontrada?"
- "Quantas entregas críticas foram priorizadas?"
- "Explique a diferença entre fitness e metrics"
- "Qual veículo teve maior utilização?"
- "Mostre a sequência da rota 1"

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

### Visualização

| Tecnologia | Versão | Uso |
|------------|--------|-----|
| Folium | 0.20.0 | Mapas interativos (Leaflet.js) |
| staticmap | 0.5.7 | Mapas estáticos PNG |
| Pillow | 12.1.0 | Manipulação de imagens |

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

4. **Visualizações Avançadas**:
   - Dashboard interativo com métricas em tempo real
   - Animações de evolução do AG
   - Gráficos de convergência
   - Comparação visual de soluções
   - Integração de mapas na interface do chat

4. **Machine Learning**:
   - Aprendizado de hiperparâmetros via Bayesian Optimization
   - Predição de fitness via regressão (acelerar avaliação)
   - Reinforcement Learning para guiar busca

5. **Extensões de Negócio**:
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

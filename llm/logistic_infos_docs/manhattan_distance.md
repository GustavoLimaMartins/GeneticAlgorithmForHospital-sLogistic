# Módulo de Cálculo de Distância Manhattan - Otimização de Rotas Logísticas

## Visão Geral

O módulo `b_manhattan_distance.py` implementa o cálculo de distâncias utilizando a métrica de Manhattan (também conhecida como distância L1, distância do taxista ou norma Manhattan). Este módulo é fundamental para avaliar o custo total de deslocamento em rotas de entrega, servindo como base para a função de fitness do algoritmo genético.

## Objetivo

Calcular a distância total percorrida por veículos em rotas de entrega, utilizando a métrica de Manhattan, que é especialmente adequada para movimentos em malhas urbanas onde os deslocamentos seguem ruas perpendiculares (como em grades retilíneas típicas de cidades planejadas).

## Fundamento Matemático

### Distância de Manhattan

A distância de Manhattan entre dois pontos em um espaço bidimensional é definida matematicamente como:

$$d_{Manhattan}(P_1, P_2) = |x_1 - x_2| + |y_1 - y_2|$$

Onde:
- $P_1 = (x_1, y_1)$ representa o primeiro ponto (coordenadas cartesianas)
- $P_2 = (x_2, y_2)$ representa o segundo ponto (coordenadas cartesianas)
- $|x_1 - x_2|$ é o valor absoluto da diferença nas coordenadas x
- $|y_1 - y_2|$ é o valor absoluto da diferença nas coordenadas y

### Por Que Manhattan ao Invés de Euclidiana?

**Distância Euclidiana (linha reta):**
$$d_{Euclidiana}(P_1, P_2) = \sqrt{(x_1 - x_2)^2 + (y_1 - y_2)^2}$$

**Vantagens da Distância Manhattan para Logística Urbana:**

1. **Realismo urbano:** Representa melhor o deslocamento em malhas viárias ortogonais
2. **Eficiência computacional:** Sem operações de potenciação ou raiz quadrada
3. **Aproximação válida:** Em cidades com ruas em grade, a distância real se aproxima da Manhattan
4. **Simplicidade:** Mais fácil de interpretar e debugar

### Exemplo Visual

```
Ponto A (1, 2) → Ponto B (4, 6)

Distância Manhattan = |4 - 1| + |6 - 2| = 3 + 4 = 7 unidades

Em uma grade urbana:
- Deslocamento horizontal: 3 quadras
- Deslocamento vertical: 4 quadras
- Total: 7 quadras
```

## Funções Principais

### 1. `cartesian_to_manhattan(coord1: tuple[float, float], coord2: tuple[float, float]) -> float`

**Descrição:** Calcula a distância de Manhattan entre dois pontos em coordenadas cartesianas.

**Parâmetros:**
- `coord1` (tuple[float, float]): Primeira coordenada no formato (x1, y1)
- `coord2` (tuple[float, float]): Segunda coordenada no formato (x2, y2)

**Retorno:**
- `float`: Distância de Manhattan entre os dois pontos

**Implementação Matemática:**
```python
distancia = abs(x1 - x2) + abs(y1 - y2)
```

**Propriedades Matemáticas:**
- **Simetria:** $d(A, B) = d(B, A)$
- **Não-negatividade:** $d(A, B) \geq 0$
- **Identidade:** $d(A, A) = 0$
- **Desigualdade triangular:** $d(A, C) \leq d(A, B) + d(B, C)$

**Exemplo de Uso:**
```python
from b_manhattan_distance import cartesian_to_manhattan

# Centro de distribuição
centro = (0, 0)

# Ponto de entrega
entrega = (3, 4)

# Calcula distância
distancia = cartesian_to_manhattan(centro, entrega)
print(f"Distância: {distancia}")  # Output: 7.0
```

**Casos de Teste:**
```python
# Mesmo ponto
cartesian_to_manhattan((0, 0), (0, 0))  # Retorna: 0.0

# Movimento apenas horizontal
cartesian_to_manhattan((0, 0), (5, 0))  # Retorna: 5.0

# Movimento apenas vertical
cartesian_to_manhattan((0, 0), (0, 3))  # Retorna: 3.0

# Movimento diagonal
cartesian_to_manhattan((1, 1), (4, 5))  # Retorna: 7.0

# Coordenadas negativas
cartesian_to_manhattan((-2, -3), (1, 2))  # Retorna: 8.0
```

### 2. `route_distance(population: list[tuple[float, float]], center_coords: list[float, float]) -> float`

**Descrição:** Calcula a distância total de uma rota completa, incluindo ida do centro de distribuição até o primeiro ponto, percurso entre todos os pontos de entrega, e retorno ao centro.

**Parâmetros:**
- `population` (list[tuple[float, float]]): Lista ordenada de coordenadas dos pontos de entrega
- `center_coords` (list[float, float]): Coordenadas do centro de distribuição (depot)

**Retorno:**
- `float`: Distância total da rota em unidades Manhattan

**Modelo Matemático da Rota:**

Para uma rota com $n$ pontos de entrega $P_1, P_2, ..., P_n$ e centro de distribuição $C$:

$$D_{total} = d(C, P_1) + \sum_{i=1}^{n-1} d(P_i, P_{i+1}) + d(P_n, C)$$

Onde:
- $d(C, P_1)$: Distância do centro ao primeiro ponto
- $\sum_{i=1}^{n-1} d(P_i, P_{i+1})$: Soma das distâncias entre pontos consecutivos
- $d(P_n, C)$: Distância do último ponto de volta ao centro

**Componentes do Cálculo:**

1. **Saída do Centro (Depot):**
   ```python
   distance += cartesian_to_manhattan(center_coords, population[0])
   ```
   - Representa o deslocamento inicial do veículo

2. **Trajeto entre Pontos de Entrega:**
   ```python
   for i in range(len(population) - 1):
       distance += cartesian_to_manhattan(population[i], population[i + 1])
   ```
   - Acumula distâncias entre todos os pontos consecutivos

3. **Retorno ao Centro:**
   ```python
   distance += cartesian_to_manhattan(population[-1], center_coords)
   ```
   - Completa o ciclo voltando ao ponto de partida

**Exemplo Completo:**

```python
from b_manhattan_distance import route_distance

# Centro de distribuição Einstein
centro = (0, 0)

# Rota com 5 entregas
rota = [
    (1, 2),   # Entrega 1
    (4, 6),   # Entrega 2
    (7, 8),   # Entrega 3
    (5, 3),   # Entrega 4
    (2, 1)    # Entrega 5
]

# Calcula distância total
distancia_total = route_distance(rota, centro)
print(f"Distância total da rota: {distancia_total}")
```

**Cálculo Passo a Passo:**

```
Centro (0,0) → (1,2):   |1-0| + |2-0| = 3
(1,2) → (4,6):          |4-1| + |6-2| = 7
(4,6) → (7,8):          |7-4| + |8-6| = 5
(7,8) → (5,3):          |5-7| + |3-8| = 7
(5,3) → (2,1):          |2-5| + |1-3| = 5
(2,1) → Centro (0,0):   |0-2| + |0-1| = 3
                        ─────────────────
Total:                  30 unidades
```

## Aplicação no Algoritmo Genético

### Integração com Fitness

A distância total calculada por este módulo é um dos principais componentes da função de fitness:

```python
# Pseudo-código de integração
def calcular_fitness(solucao):
    fitness_total = 0
    
    for veiculo_id, entregas in solucao:
        # Obtém coordenadas das entregas
        coordenadas = obter_coordenadas(entregas)
        
        # Calcula distância da rota usando Manhattan
        distancia = route_distance(coordenadas, centro_distribuicao)
        
        # Penaliza distâncias maiores (minimização)
        fitness_total += distancia
    
    return fitness_total
```

### Objetivo de Otimização

No contexto do algoritmo genético:
- **Objetivo:** Minimizar a distância total
- **Fitness menor = Solução melhor**
- A ordem dos pontos na rota afeta diretamente a distância total

### Comparação de Rotas

**Rota A (não otimizada):**
```
Centro → (10,10) → (1,1) → (9,9) → Centro
Distância: 20 + 18 + 16 + 18 = 72 unidades
```

**Rota B (otimizada):**
```
Centro → (1,1) → (9,9) → (10,10) → Centro
Distância: 2 + 16 + 2 + 20 = 40 unidades
```

A Rota B tem fitness melhor (menor distância).

## Complexidade Computacional

### `cartesian_to_manhattan()`
- **Tempo:** $O(1)$ - operações aritméticas constantes
- **Espaço:** $O(1)$ - sem estruturas auxiliares

### `route_distance()`
- **Tempo:** $O(n)$ onde $n$ é o número de pontos na rota
- **Espaço:** $O(1)$ - apenas variável acumuladora
- **Número de cálculos:** $n + 1$ chamadas a `cartesian_to_manhattan()`

### Eficiência no Contexto do Algoritmo Genético

Para uma população de $P$ indivíduos, cada um com $V$ veículos e média de $E$ entregas por veículo:

- **Cálculos por geração:** $P \times V \times (E + 1)$
- **Para 100 gerações com P=50, V=5, E=5:** $50 \times 5 \times 6 \times 100 = 150.000$ cálculos

Graças à eficiência $O(1)$ de cada cálculo Manhattan, isso é computacionalmente viável.

## Considerações Práticas

### Unidades de Medida

As coordenadas devem estar em um sistema consistente:
- **Latitude/Longitude convertidas:** Para coordenadas geográficas reais
- **Unidades arbitrárias:** Para problemas abstratos
- **Escala consistente:** Todas as coordenadas no mesmo sistema

### Precisão Numérica

- Utiliza `float` para coordenadas (precisão decimal)
- Acumulação de erros é mínima devido a operações simples
- Adequado para problemas de escala urbana (até centenas de quilômetros)

### Limitações

1. **Não considera obstáculos:** Assume movimento livre em grid
2. **Ruas não ortogonais:** Menos preciso em malhas irregulares
3. **Tráfego e velocidade:** Não modela tempo real, apenas distância
4. **Topografia:** Não considera elevação ou terreno

### Quando Usar Manhattan vs. Outras Métricas

**Use Manhattan quando:**
- Malha viária em grade (ex: Nova York, Buenos Aires)
- Movimento restrito a eixos perpendiculares
- Eficiência computacional é prioritária
- Aproximação de distância real é suficiente

**Use Euclidiana quando:**
- Movimento livre em qualquer direção (aviões, drones)
- Distância em linha reta é relevante
- Precisão geométrica é crítica

**Use Haversine quando:**
- Coordenadas geográficas (lat/lon)
- Distâncias longas (curvatura da Terra importa)
- Precisão máxima em navegação

## Integração com Outros Módulos

### Fluxo de Dados

```
a_generate_population.py
    ↓ (gera soluções)
b_manhattan_distance.py ← address_routes/ (coordenadas)
    ↓ (calcula distâncias)
c_fitness.py
    ↓ (avalia soluções)
genetic_algorithm.py
```

### Módulos Dependentes

1. **c_fitness.py:** Usa `route_distance()` para calcular fitness
2. **routes_evaluation.py:** Avalia qualidade de rotas finais
3. **itinerary_routes/:** Visualiza rotas com distâncias calculadas

### Dados de Entrada Necessários

- **Coordenadas de entrega:** De `address_routes/einstein_units.py`
- **Centro de distribuição:** De `address_routes/distribute_center.py`
- **Solução candidata:** De `a_generate_population.py`

## Validação e Testes

### Testes Unitários Recomendados

```python
def test_mesma_posicao():
    assert cartesian_to_manhattan((0, 0), (0, 0)) == 0

def test_simetria():
    d1 = cartesian_to_manhattan((1, 2), (3, 4))
    d2 = cartesian_to_manhattan((3, 4), (1, 2))
    assert d1 == d2

def test_desigualdade_triangular():
    a, b, c = (0, 0), (3, 4), (6, 8)
    d_ab = cartesian_to_manhattan(a, b)
    d_bc = cartesian_to_manhattan(b, c)
    d_ac = cartesian_to_manhattan(a, c)
    assert d_ac <= d_ab + d_bc

def test_rota_vazia():
    # Rota com apenas retorno ao centro
    assert route_distance([], (0, 0)) == 0

def test_rota_unico_ponto():
    # Ida e volta ao mesmo ponto
    dist = route_distance([(3, 4)], (0, 0))
    assert dist == 14  # 7 (ida) + 7 (volta)
```

## Exemplo Prático Completo

### Cenário: Rota de Entregas Einstein SP

```python
from b_manhattan_distance import route_distance, cartesian_to_manhattan

# Centro de Distribuição Einstein
centro_einstein = (0, 0)  # Origem normalizada

# 5 Unidades Einstein em São Paulo (coordenadas exemplo)
entregas_veiculo_1 = [
    (2.5, 3.1),   # Einstein Morumbi
    (5.2, 1.8),   # Einstein Ibirapuera
    (3.7, 4.5),   # Einstein Jardins
    (1.9, 2.3),   # Einstein Vila Mariana
    (4.1, 3.9)    # Einstein Itaim
]

# Calcula distância total da rota
distancia_total = route_distance(entregas_veiculo_1, centro_einstein)

print(f"Distância total: {distancia_total:.2f} unidades")
print(f"Número de entregas: {len(entregas_veiculo_1)}")
print(f"Distância média por entrega: {distancia_total/len(entregas_veiculo_1):.2f}")

# Análise detalhada
print("\n--- Análise Segmentada ---")
print(f"Centro → Primeira entrega: "
      f"{cartesian_to_manhattan(centro_einstein, entregas_veiculo_1[0]):.2f}")

for i in range(len(entregas_veiculo_1) - 1):
    dist_segmento = cartesian_to_manhattan(
        entregas_veiculo_1[i], 
        entregas_veiculo_1[i+1]
    )
    print(f"Entrega {i+1} → Entrega {i+2}: {dist_segmento:.2f}")

print(f"Última entrega → Centro: "
      f"{cartesian_to_manhattan(entregas_veiculo_1[-1], centro_einstein):.2f}")
```

## Otimizações Possíveis

### 1. Memoização de Distâncias
```python
# Cache de distâncias já calculadas
cache_distancias = {}

def cartesian_to_manhattan_cached(coord1, coord2):
    key = (coord1, coord2)
    if key not in cache_distancias:
        cache_distancias[key] = cartesian_to_manhattan(coord1, coord2)
    return cache_distancias[key]
```

### 2. Matriz de Distâncias Pré-calculada
```python
# Para n pontos fixos, calcular matriz n×n uma única vez
def criar_matriz_distancias(pontos):
    n = len(pontos)
    matriz = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            dist = cartesian_to_manhattan(pontos[i], pontos[j])
            matriz[i][j] = matriz[j][i] = dist
    return matriz
```

### 3. Vetorização com NumPy
```python
import numpy as np

def manhattan_vectorized(coords1, coords2):
    return np.sum(np.abs(np.array(coords1) - np.array(coords2)))
```

## Palavras-chave para Busca

- Distância Manhattan
- Métrica L1
- Distância do taxista
- Cálculo de rota
- Otimização logística
- TSP (Traveling Salesman Problem)
- VRP (Vehicle Routing Problem)
- Fitness de rota
- Algoritmo genético distância
- Coordenadas cartesianas
- Norma Manhattan
- Minimização de percurso
- Centro de distribuição
- Trajeto de entrega
- Custo de deslocamento

## Referências Matemáticas

- **Norma $L_1$ (Manhattan):** $||x||_1 = \sum_{i=1}^n |x_i|$
- **Propriedade triangular:** $d(x,z) \leq d(x,y) + d(y,z)$
- **Espaço métrico:** $(X, d)$ onde $d$ satisfaz axiomas de métrica
- **Complexidade TSP:** Problema NP-completo, heurísticas necessárias

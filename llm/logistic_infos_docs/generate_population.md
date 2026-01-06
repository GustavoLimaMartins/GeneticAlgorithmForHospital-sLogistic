# Módulo de Geração de População - Algoritmo Genético para Otimização Logística

## Visão Geral

O módulo `a_generate_population.py` é responsável pela criação da população inicial do algoritmo genético aplicado ao problema de otimização de rotas de entrega. Este módulo implementa a geração aleatória de soluções candidatas que servem como ponto de partida para o processo evolutivo.

## Objetivo

Gerar uma população inicial diversificada de soluções candidatas para o problema de roteamento de veículos (VRP - Vehicle Routing Problem), onde cada solução representa uma possível alocação de entregas aos veículos disponíveis.

## Funções Principais

### 1. `generate_population_coordinates(city: str, pop_size: int) -> list[tuple[float, float]]`

**Descrição:** Gera uma população de soluções candidatas com tamanho definido pelo usuário.

**Parâmetros:**
- `city` (str): Código da cidade para a qual as rotas serão geradas. Atualmente suporta "SP" (São Paulo)
- `pop_size` (int): Tamanho da população, ou seja, número de soluções candidatas a serem geradas

**Retorno:**
- Lista de soluções, onde cada solução é representada como uma lista de tuplas
- Cada tupla contém: (identificador_do_veículo, tupla_de_entregas)

**Funcionamento:**
1. Obtém um candidato de solução base através da função `deliveries_solution_candidate()`
2. Cria embaralhamentos aleatórios das entregas e dos veículos
3. Gera `pop_size` soluções combinando veículos e entregas aleatoriamente
4. Garante diversidade na população inicial através de múltiplos embaralhamentos

**Exemplo de Uso:**
```python
population = generate_population_coordinates("SP", 50)
# Gera 50 soluções candidatas diferentes para São Paulo
```

### 2. `deliveries_solution_candidate(city: str) -> dict[str, tuple[int, ...]]`

**Descrição:** Cria um único candidato de solução base com distribuição aleatória de entregas entre veículos.

**Parâmetros:**
- `city` (str): Código da cidade ("SP" para São Paulo)

**Retorno:**
- Dicionário onde:
  - Chave: Identificador do veículo (string no formato "V1", "V2", etc.)
  - Valor: Tupla contendo IDs das entregas atribuídas ao veículo

**Estrutura para São Paulo (SP):**
- **Total de entregas:** 25 (IDs de 1 a 25)
- **Número de veículos:** 5 (V1 a V5)
- **Entregas por veículo:** 5 entregas
- **Distribuição:** Aleatória e balanceada

**Exemplo de Retorno:**
```python
{
    "V1": (3, 15, 7, 22, 11),
    "V2": (18, 4, 25, 9, 13),
    "V3": (1, 19, 6, 14, 21),
    "V4": (8, 16, 2, 23, 10),
    "V5": (12, 5, 20, 17, 24)
}
```

## Características do Problema

### Configuração de São Paulo (SP)

- **Entregas totais:** 25 unidades Einstein
- **Frota de veículos:** 5 veículos
- **Capacidade por veículo:** 5 entregas
- **IDs de entregas:** Números inteiros de 1 a 25
- **Identificadores de veículos:** V1, V2, V3, V4, V5

### Restrições Implícitas

1. Cada entrega é atribuída a exatamente um veículo
2. Todos os veículos recebem exatamente 5 entregas
3. Não há entregas duplicadas ou omitidas
4. A distribuição inicial é completamente aleatória

## Representação da Solução

Cada solução (cromossomo) na população é representada como:
```python
[
    ("V1", (3, 15, 7, 22, 11)),
    ("V2", (18, 4, 25, 9, 13)),
    ("V3", (1, 19, 6, 14, 21)),
    ("V4", (8, 16, 2, 23, 10)),
    ("V5", (12, 5, 20, 17, 24))
]
```

Onde:
- A ordem externa representa a sequência de veículos
- Cada tupla interna representa as entregas atribuídas ao veículo
- A ordem das entregas dentro da tupla representa a sequência de visitação

## Processo de Geração

1. **Criação do Pool de Entregas:**
   - Gera lista de IDs de 1 a 25
   - Embaralha aleatoriamente usando `random.shuffle()`

2. **Distribuição Equitativa:**
   - Divide as 25 entregas em 5 grupos de 5
   - Atribui cada grupo a um veículo específico

3. **Diversificação da População:**
   - Cria múltiplas variações através de embaralhamentos
   - Combina diferentes ordens de veículos e entregas
   - Gera `pop_size` soluções únicas

## Importância na Otimização

A qualidade da população inicial é crucial para o desempenho do algoritmo genético:

- **Diversidade:** Múltiplas soluções aleatórias garantem exploração ampla do espaço de busca
- **Aleatoriedade:** Evita viés inicial e pontos de convergência prematura
- **Distribuição balanceada:** Garante que todos os veículos tenham carga similar
- **Validade:** Todas as soluções geradas são válidas (respeitam restrições do problema)

## Integração com Outros Módulos

Este módulo fornece a entrada para:
- **b_manhattan_distance.py:** Cálculo de distâncias entre pontos de entrega
- **c_fitness.py:** Avaliação da qualidade de cada solução
- **d_crossover.py:** Operação de cruzamento entre soluções
- **e_mutation.py:** Operação de mutação para gerar variações
- **f_selection.py:** Seleção das melhores soluções para próxima geração

## Considerações Técnicas

### Complexidade
- Complexidade de tempo: O(pop_size × n) onde n é o número de entregas
- Complexidade de espaço: O(pop_size × m) onde m é o número de veículos

### Escalabilidade
Para adicionar novas cidades, basta estender o if-else na função `deliveries_solution_candidate`:
```python
def deliveries_solution_candidate(city: str) -> dict[str, tuple[int, ...]]:
    if city == "SP":
        # Configuração para São Paulo
        ...
    elif city == "RJ":
        # Configuração para Rio de Janeiro
        ...
```

## Exemplo Completo de Execução

```python
from a_generate_population import generate_population_coordinates

# Gera população inicial com 100 indivíduos
population = generate_population_coordinates("SP", 100)

# Cada indivíduo é uma solução completa
first_solution = population[0]
print(f"Primeira solução: {first_solution}")

# Número total de soluções geradas
print(f"Tamanho da população: {len(population)}")

# Verificar estrutura de uma solução
for vehicle_id, deliveries in first_solution:
    print(f"Veículo {vehicle_id}: {len(deliveries)} entregas - {deliveries}")
```

## Perguntas Frequentes

**Q: Por que usar 5 entregas por veículo?**
A: A distribuição atual (25 entregas ÷ 5 veículos = 5 entregas/veículo) representa um balanceamento ideal para o problema de São Paulo, garantindo carga equitativa.

**Q: Como é garantida a aleatoriedade?**
A: Usa-se `random.shuffle()` e `random.sample()` do módulo random do Python, que implementam aleatoriedade pseudoaleatória de alta qualidade.

**Q: As soluções iniciais podem ser duplicadas?**
A: Sim, devido à natureza aleatória, é possível (mas improvável) que duas soluções sejam idênticas. Isso não afeta negativamente o algoritmo.

**Q: Qual o tamanho ideal de população?**
A: Depende do problema, mas valores entre 50-200 são comuns. Populações maiores oferecem mais diversidade, mas aumentam o custo computacional.

## Palavras-chave para Busca

- Geração de população inicial
- Algoritmo genético logística
- VRP (Vehicle Routing Problem)
- Otimização de rotas
- Distribuição de entregas
- Alocação de veículos
- Cromossomo inicial
- Solução candidata
- População diversificada
- Embaralhamento aleatório

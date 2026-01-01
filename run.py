from _encode_decode import encode_individual, decode_chromosome
from a_generate_population import generate_population_coordinates
from c_fitness import calculate_fitness
from d_crossover import crossover
from f_selection import select_next_generation, tournament_selection
from e_mutation import light_mutation
from address_routes.distribute_center import get_center_coordinates as depot
from delivery_setup.deliveries import load_deliveries_info as deliveries
from delivery_setup.vehicles import load_vehicles_info as vehicles

city_code = "SP"
initial_population = generate_population_coordinates(city_code, 50)
max_generations = 100

population = [
    {"chromosome": encode_individual(ind), "fitness": None}
    for ind in initial_population
]

vehicles = vehicles(city_code)
deliveries = deliveries(city_code)
depot = depot(city_code)

print(f"\n{'='*60}")
print(f"Iniciando Algoritmo Genético - Cidade: {city_code}")
print(f"População: {len(population)} | Gerações: {max_generations}")
print(f"{'='*60}\n")

best_overall = None

for generation in range(max_generations):

    # Evaluate fitness
    for ind in population:
        routes = decode_chromosome(ind["chromosome"], deliveries, vehicles)
        ind["fitness"] = calculate_fitness(routes, city_code)

    # Statistics
    fitness_values = [ind["fitness"] for ind in population]
    best_fitness = min(fitness_values)
    avg_fitness = sum(fitness_values) / len(fitness_values)
    worst_fitness = max(fitness_values)
    
    best_individual = min(population, key=lambda x: x["fitness"])
    
    if best_overall is None or best_fitness < best_overall["fitness"]:
        best_overall = {
            "generation": generation,
            "fitness": best_fitness,
            "chromosome": best_individual["chromosome"]
        }
    
    # Display progress
    if generation % 10 == 0 or generation == max_generations - 1:
        print(f"Geração {generation:3d} | Melhor: {best_fitness:.2f} | Média: {avg_fitness:.2f} | Pior: {worst_fitness:.2f}")

    # Selection
    selected = select_next_generation(
        population,
        pop_size=len(population),
        elite_ratio=0.035,
        tournament_k=2
    )

    # Reproduction
    offspring = []

    while len(offspring) < len(population):
        p1 = tournament_selection(selected)
        p2 = tournament_selection(selected)

        child_chrom = crossover(p1["chromosome"], p2["chromosome"], deliveries, vehicles, depot)
        child_chrom = light_mutation(child_chrom)

        offspring.append({"chromosome": child_chrom, "fitness": None})

    population = offspring

print(f"\n{'='*60}")
print(f"Evolução Concluída!")
print(f"{'='*60}")
print(f"Melhor solução encontrada na geração {best_overall['generation']}")
print(f"Fitness: {best_overall['fitness']:.2f}")
print(f"\nDecodificando melhor solução...")
best_routes = decode_chromosome(best_overall['chromosome'], deliveries, vehicles)
total_deliveries = sum(len(route_deliveries) for _, route_deliveries in best_routes)
print(f"Total de entregas: {len(best_overall['chromosome'])}")
print(f"Entregas atribuídas: {total_deliveries}")
print(f"Número de rotas: {len(best_routes)}")

# Group routes by vehicle
vehicle_route_count = {}
for vehicle_id, route_deliveries in best_routes:
    if vehicle_id not in vehicle_route_count:
        vehicle_route_count[vehicle_id] = []
    vehicle_route_count[vehicle_id].append(route_deliveries)

print(f"\nDistribuição por veículo:")
for vehicle_id, routes_list in vehicle_route_count.items():
    total_del = sum(len(r) for r in routes_list)
    print(f"  Veículo {vehicle_id}: {len(routes_list)} viagens, {total_del} entregas")

print(f"\nDetalhes das rotas:")
for i, (vehicle_id, route_deliveries) in enumerate(best_routes, 1):
    delivery_details = [(del_id, deliveries[del_id]["demand"]) for del_id in route_deliveries]
    total_load = sum(demand for _, demand in delivery_details)
    print(f"  Rota {i} (Veículo {vehicle_id}): {len(route_deliveries)} entregas | Carga total: {total_load}")
    print(f"    Entregas (ID, Demanda): {delivery_details}")
print(f"{'='*60}\n")

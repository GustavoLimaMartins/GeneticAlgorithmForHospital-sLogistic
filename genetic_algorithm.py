from _encode_decode import encode_individual, decode_chromosome
from a_generate_population import generate_population_coordinates
from c_fitness import calculate_fitness
from d_crossover import crossover
from f_selection import select_next_generation, tournament_selection
from e_mutation import light_mutation
from address_routes.distribute_center import get_center_coordinates as depot_coords
from delivery_setup.deliveries import load_deliveries_info as d_info
from delivery_setup.vehicles import load_vehicles_info as v_info
import matplotlib.pyplot as plt

class GeneticAlgorithm:
    def __init__(self, city_code: str, max_generations: int, population_length: int, ratio_elitism: float, ratio_mutation: float, tournament_k: int):
        self.city_code = city_code
        self.max_generations = max_generations
        self.population_length = population_length
        self.ratio_elitism = ratio_elitism
        self.ratio_mutation = ratio_mutation
        self.tournament_k = tournament_k
        self.vehicles = v_info(self.city_code)
        self.deliveries = d_info(self.city_code)
        self.depot = depot_coords(self.city_code)

    def initial_message(self):
        print(f"\n{'='*60}")
        print(f"Iniciando Algoritmo Genético - Cidade: {self.city_code}")
        print(f"População: {self.population_length} | Gerações: {self.max_generations}")
        print(f"{'='*60}\n")

    def final_message(self) -> list[tuple[str, tuple[int]]]:
        print(f"\n{'='*60}")
        print(f"Evolução Concluída!")
        print(f"{'='*60}")
        print(f"Melhor solução encontrada na geração {self.best_overall['generation']}")
        print(f"Fitness: {self.best_overall['fitness']:.2f}")
        print(f"\nDecodificando melhor solução...")
        self.best_routes = decode_chromosome(self.best_overall['chromosome'], self.deliveries, self.vehicles)
        total_deliveries = sum(len(route_deliveries) for _, route_deliveries in self.best_routes)
        print(f"Total de entregas: {len(self.best_overall['chromosome'])}")
        print(f"Entregas atribuídas: {total_deliveries}")
        print(f"Número de rotas: {len(self.best_routes)}")
    
    def routes_summary(self) -> dict[str, any]:
        # Group routes by vehicle
        vehicle_route_count = {}
        for vehicle_id, route_deliveries in self.best_routes:
            if vehicle_id not in vehicle_route_count:
                vehicle_route_count[vehicle_id] = []
            vehicle_route_count[vehicle_id].append(route_deliveries)

        print(f"\nDistribuição por veículo:")
        for vehicle_id, routes_list in vehicle_route_count.items():
            total_del = sum(len(r) for r in routes_list)
            print(f"  Veículo {vehicle_id}: {len(routes_list)} viagens, {total_del} entregas")

        print(f"\nDetalhes das rotas:")
        routes_metadata = dict()
        for i, (vehicle_id, route_deliveries) in enumerate(self.best_routes, 1):
            demand_values = [self.deliveries[del_id]["demand"] for del_id in route_deliveries]
            total_load = sum(demand_values)
            delivery_details = [((del_id, vehicle_id)) for del_id in route_deliveries]
            print(f"  Rota {i} (Veículo {vehicle_id}): {len(route_deliveries)} entregas | Carga total: {total_load}")
            print(f"    Entregas (ID): {route_deliveries}")
            routes_metadata[i] = delivery_details
        
        print(f"{'='*60}\n")
        
        return {
            'generation': self.best_overall['generation'],
            'fitness': self.best_overall['fitness'],
            'routes_metadata': routes_metadata
        }
    
    def plot_fitness_evolution(self, save_path: str = None):
        """
        Plot a evolution of fitness values over generations.
        
        Args:
            save_path: Optional path to save the plot. If None, just displays it.
        """
        plt.figure(figsize=(12, 6))
        
        plt.plot(self.fitness_history['generation'], self.fitness_history['best'], 
                label='Best Fitness', linewidth=2, color='green')
        plt.plot(self.fitness_history['generation'], self.fitness_history['avg'], 
                label='Average Fitness', linewidth=2, color='blue', linestyle='--')
        plt.plot(self.fitness_history['generation'], self.fitness_history['worst'], 
                label='Worst Fitness', linewidth=1, color='red', alpha=0.5)
        
        plt.xlabel('Generation', fontsize=12)
        plt.ylabel('Fitness', fontsize=12)
        plt.title(f'Genetic Algorithm Evolution - City: {self.city_code}', fontsize=14, fontweight='bold')
        plt.legend(loc='best', fontsize=10)
        plt.grid(True, alpha=0.3)
        
        # Add annotation for the best value
        best_gen = self.best_overall['generation']
        best_fit = self.best_overall['fitness']
        plt.annotate(f'Best: {best_fit:.2f}\n(Gen {best_gen})',
                    xy=(best_gen, best_fit),
                    xytext=(10, 20), textcoords='offset points',
                    bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.7),
                    arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Graph saved at: {save_path}")
        #plt.show()

    def run(self, iterator: int) -> dict[str, any]:
        initial_population = generate_population_coordinates(self.city_code, self.population_length)

        population = [
            {"chromosome": encode_individual(ind), "fitness": None}
            for ind in initial_population
        ]

        self.initial_message()
        self.best_overall = None
        
        # Track fitness evolution
        self.fitness_history = {
            'generation': [],
            'best': [],
            'avg': [],
            'worst': []
        }

        for generation in range(self.max_generations):

            # Evaluate fitness
            for ind in population:
                routes = decode_chromosome(ind["chromosome"], self.deliveries, self.vehicles)
                ind["fitness"] = calculate_fitness(routes, self.city_code)

            # Statistics
            fitness_values = [ind["fitness"] for ind in population]
            best_fitness = min(fitness_values)
            avg_fitness = sum(fitness_values) / len(fitness_values)
            worst_fitness = max(fitness_values)
            
            # Save fitness history
            self.fitness_history['generation'].append(generation)
            self.fitness_history['best'].append(best_fitness)
            self.fitness_history['avg'].append(avg_fitness)
            self.fitness_history['worst'].append(worst_fitness)
            
            best_individual = min(population, key=lambda x: x["fitness"])
            
            if self.best_overall is None or best_fitness < self.best_overall["fitness"]:
                self.best_overall = {
                    "generation": generation,
                    "fitness": best_fitness,
                    "chromosome": best_individual["chromosome"]
                }
            
            # Display progress
            if generation % 100 == 0 or generation == self.max_generations - 1:
                print(f"Geração {generation:3d} | Melhor: {best_fitness:.2f} | Média: {avg_fitness:.2f} | Pior: {worst_fitness:.2f}")

            # Selection
            selected = select_next_generation(
                population,
                pop_size=len(population),
                elite_ratio=self.ratio_elitism,
                tournament_k=self.tournament_k
            )

            # Reproduction
            offspring = []

            while len(offspring) < len(population):
                p1 = tournament_selection(selected)
                p2 = tournament_selection(selected)

                child_chrom = crossover(p1["chromosome"], p2["chromosome"], self.deliveries, self.vehicles, self.depot)
                child_chrom = light_mutation(child_chrom, self.ratio_mutation)

                offspring.append({"chromosome": child_chrom, "fitness": None})

            population = offspring

        self.final_message()
        result = self.routes_summary()
        
        # Plot fitness evolution
        self.plot_fitness_evolution(save_path=f'fitness_balance/i{iterator}_fitness_evolution.png')
        
        return result


if __name__ == "__main__":

    ga = GeneticAlgorithm(
        city_code='SP',
        max_generations=100,
        population_length=50,
        ratio_elitism=0.1,
        ratio_mutation=0.5,
        tournament_k=3
    )
    routes_metadata = ga.run(iterator=1)
    print(routes_metadata)


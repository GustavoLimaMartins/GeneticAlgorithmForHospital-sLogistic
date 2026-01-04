#TODO Orquestration file to run the genetic algorithm, considerer create a dictionary with index, for route evaluations and map generations
from genetic_algorithm import GeneticAlgorithm
from routes_evaluation import RouteEvaluator

solutions = {}
best_solution_by_fitness = None
best_solution_by_metrics = None

def heuristic_loop(iterations: int,
                   city_code: str, 
                   population_length: int, 
                   max_generations: int, 
                   ratio_elitism: float, 
                   ratio_mutation: float, 
                   tournament_k: int
                   ):
    for index in range(iterations):
        ga = GeneticAlgorithm(
            city_code=city_code,
            population_length=population_length,
            max_generations=max_generations,
            ratio_elitism=ratio_elitism,
            ratio_mutation=ratio_mutation,
            tournament_k=tournament_k
        )
        ga_metadata = ga.run()
        vehicle_data = ga.vehicles
        delivery_data = ga.deliveries

        evaluator = RouteEvaluator(
            routes_metadata=ga_metadata['routes_metadata'],
            vehicle_data=vehicle_data,
            delivery_data=delivery_data
        )
        metrics = evaluator.metric_summary()

        solution = {
            'generation': ga_metadata['generation'],
            'fitness': ga_metadata['fitness'],
            'routes_metadata': ga_metadata['routes_metadata'],
            'metrics': metrics
        }

        solutions[index] = solution
        print(f"Completed iteration {index + 1}/{iterations}")

def best_solution(capacity_weight: float = 0.4, travel_weight: float = 0.1, critical_weight: float = 0.5) -> dict[str, any]:
    best_index = None
    best_fitness = float('inf')

    "The function to get the best solution, by fitness value, from the solutions dictionary"
    for index, solution in solutions.items():
        if solution['fitness'] < best_fitness:
            best_fitness = solution['fitness']
            best_index = index

    best_solution_by_fitness = solutions[best_index]
    
    "The function to get the best solution, by priority metrics performance ranking (capacity, travel, critical items), from the solutions dictionary"
    best_metric_score = float('-inf')
    for index, solution in solutions.items():
        metrics = solution['metrics']
        metric_score = (
            metrics['capacity_utilization_metric_positive'] * capacity_weight -
            metrics['travel_costs_metric_negative'] * travel_weight +
            metrics['critical_delivery_metric_positive'] * critical_weight
        )
        if metric_score > best_metric_score:
            best_metric_score = metric_score
            best_index = index

    best_solution_by_metrics = solutions[best_index]

    return {
        'best_by_fitness': best_solution_by_fitness,
        'best_by_metrics': best_solution_by_metrics
    }

if __name__ == "__main__":
    heuristic_loop(
        iterations=5,
        city_code="SP",
        population_length=50,
        max_generations=100,
        ratio_elitism=0.1,
        ratio_mutation=0.3,
        tournament_k=2
    )

    best_solutions = best_solution()
    print("Best solution by general fitness:", best_solutions['best_by_fitness'])
    print("Best solution by priority metrics:", best_solutions['best_by_metrics'])

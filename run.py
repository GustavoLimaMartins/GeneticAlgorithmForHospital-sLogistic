from genetic_algorithm import GeneticAlgorithm
from routes_evaluation import RouteEvaluator

class Solution:
    def __init__(self, total_iterations: int):
        self.total_iterations = total_iterations
        self.solutions = {}
        self.ga_metadata = None
        self.vehicle_data = None
        self.delivery_data = None
        self.depot_coords = None
        self.best_solution_by_fitness = None
        self.best_solution_by_metrics = None
    
    def heuristic_loop(self, city_code: str, population_length: tuple[int], max_generations: tuple[int], ratio_elitism: tuple[float], ratio_mutation: tuple[float], tournament_k: tuple[int]):
        if not (len(population_length) == len(max_generations) == len(ratio_elitism) == len(ratio_mutation) == len(tournament_k) == self.total_iterations):
            raise ValueError("All parameter tuples must have the same length as total_iterations.")
        
        for index in range(self.total_iterations):
            ga = GeneticAlgorithm(
                city_code=city_code,
                population_length=population_length[index],
                max_generations=max_generations[index],
                ratio_elitism=ratio_elitism[index],
                ratio_mutation=ratio_mutation[index],
                tournament_k=tournament_k[index]
            )
            self.ga_metadata = ga.run()
            self.vehicle_data = ga.vehicles
            self.delivery_data = ga.deliveries
            self.depot_coords = ga.depot

            evaluator = RouteEvaluator(
                routes_metadata=self.ga_metadata['routes_metadata'],
                vehicle_data=self.vehicle_data,
                delivery_data=self.delivery_data
            )
            metrics = evaluator.metric_summary()

            solution = {
                'iteration': index+1,
                'generation': self.ga_metadata['generation'],
                'fitness': self.ga_metadata['fitness'],
                'routes_metadata': self.ga_metadata['routes_metadata'],
                'metrics': metrics
            }

            self.solutions[index] = solution
            print(f"Completed iteration {index + 1}/{self.total_iterations}")

    def best_solution(self, capacity_weight: float = 0.2, travel_weight: float = 0.4, critical_weight: float = 0.4) -> dict[str, any]:
        best_index = None
        best_fitness = float('inf')

        "The function to get the best solution, by fitness value, from the solutions dictionary"
        for index, solution in self.solutions.items():
            if solution['fitness'] < best_fitness:
                best_fitness = solution['fitness']
                best_index = index

        best_solution_by_fitness = self.solutions[best_index]
        
        "The function to get the best solution, by priority metrics performance ranking (capacity, travel, critical items), from the solutions dictionary"
        best_metric_score = float('-inf')
        for index, solution in self.solutions.items():
            metrics = solution['metrics']
            metric_score = (
                metrics['capacity_utilization_metric_positive'] * capacity_weight -
                metrics['travel_costs_metric_negative'] * travel_weight +
                metrics['critical_delivery_metric_positive'] * critical_weight
            )
            if metric_score > best_metric_score:
                best_metric_score = metric_score
                best_index = index

        best_solution_by_metrics = self.solutions[best_index]

        return {
            'best_by_fitness': best_solution_by_fitness,
            'best_by_metrics': best_solution_by_metrics
        }

if __name__ == "__main__":
    solutions = Solution(total_iterations=20)
    city_code = "SP"

    solutions.heuristic_loop(
        city_code=city_code,
        population_length=(80, 150, 50, 60, 200, 30, 100, 120, 120, 70, 180, 90, 100, 250, 100, 100, 80, 80, 150, 100),
        max_generations=(200, 150, 250, 100, 400, 500, 200, 300, 300, 200, 180, 150, 250, 200, 500, 250, 200, 200, 300, 350),
        ratio_elitism=(0.05, 0.02, 0.15, 0.10, 0.05, 0.03, 0.07, 0.05, 0.10, 0.20, 0.04, 0.30, 0.08, 0.05, 0.06, 0.10, 0.12, 0.08, 0.10, 0.05),
        ratio_mutation=(0.3, 0.25, 0.1, 0.5, 0.4, 0.12, 0.02, 0.2, 0.10, 0.2, 0.2, 0.5, 0.35, 0.3, 0.1, 0.5, 0.4, 0.4, 0.6, 0.8),
        tournament_k=(3, 2, 5, 4, 3, 2, 3, 4, 4, 6, 2, 5, 4, 3, 5, 3, 7, 2, 4, 5)
    )

    best_solutions = solutions.best_solution()
    best_by_fitness = best_solutions['best_by_fitness']
    best_by_metrics = best_solutions['best_by_metrics']
    print("Best Solution by Fitness:", best_by_fitness)
    print("Best Solution by Metrics:", best_by_metrics)

    from itinerary_routes.a_google_maps import GoogleMapsAPI
    from itinerary_routes.b_polyline_designer import PolylineDesigner
    from itinerary_routes.c_folium_path import FoliumPath
    from itinerary_routes.d_static_map import StaticMapRoute
    from itinerary_routes._solution_type import SolutionMethod

    gmaps_api = GoogleMapsAPI()
    origin = solutions.depot_coords  # Output from depot
    destination = solutions.depot_coords  # Return to depot
    metadata_solutions = ((best_by_fitness, SolutionMethod.FITNESS), (best_by_metrics, SolutionMethod.METRICS))

    solution_deliveries = []
    for solution, sol_method in metadata_solutions:
        for route in solution['routes_metadata'].keys():
            for delivery in solution['routes_metadata'][route]:
                delivery_id = int(delivery[0])
                delivery_coords = (solutions.delivery_data[delivery_id]['lat'], solutions.delivery_data[delivery_id]['lon'])
                solution_deliveries.append(delivery_coords)

            solution_waypoints = solution_deliveries # Hospitals from delivery points

            directions = gmaps_api.get_directions(origin, destination, solution_waypoints)
            poly_designer = PolylineDesigner(directions)
            coords, leg_starts = poly_designer.extract_coordinates_with_multicolors()

            folium_path = FoliumPath(coords, leg_starts, iterator=solution['iteration'], generation=solution['generation'], route_id=route)
            folium_path.create_html_map(sol_method)
            static_map_route = StaticMapRoute(coords, leg_starts, iterator=solution['iteration'], generation=solution['generation'], route_id=route)
            static_map_route.create_static_map(sol_method)
            solution_deliveries = []  # Reset for next route

    from llm.chroma_db import main as generate_data_store
    from address_routes.einstein_units import hospitalar_units_lat_lon
    import json
    import numpy as np

    def convert_numpy_types(obj):
        """
        Recursively convert numpy types to native Python types for JSON serialization
        """
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, dict):
            return {key: convert_numpy_types(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [convert_numpy_types(item) for item in obj]
        elif isinstance(obj, tuple):
            return tuple(convert_numpy_types(item) for item in obj)
        else:
            return obj

    # Generate the vector store with documentation
    print("\n" + "="*70)
    print("Generating vector store for RAG system...")
    print("="*70)
    generate_data_store()
    
    def get_unit_name(did, dd, cc: str = city_code):
        d = dd[did]
        return next((n for n, (rlat, rlon) in hospitalar_units_lat_lon.get(cc, {}).items() 
                    if abs(d['lat']-rlat)<0.0001 and abs(d['lon']-rlon)<0.0001), f"Unidade Einstein (Entrega #{did})")
    
    def create_route_sequences(sol, dd, dn="Centro de Distribuição"):
        return {rid: f"{dn} -> " + " -> ".join([f"{get_unit_name(did, dd)} (Entrega #{did})" 
                for did, _ in rd]) + f" -> {dn}" for rid, rd in sol['routes_metadata'].items()}
    
    # Convert numpy types to native Python types before saving
    best_solutions_converted = convert_numpy_types(best_solutions)
    
    # Add route sequences with hospital names to both best solutions
    for key in ['best_by_fitness', 'best_by_metrics']:
        best_solutions_converted[key]['routes_sequences'] = create_route_sequences(
            best_solutions_converted[key], solutions.delivery_data)
    
    solutions_output = {
        'best_solutions': best_solutions_converted,
        'all_solutions': convert_numpy_types(solutions.solutions),
        'metadata': {
            'vehicle_data': convert_numpy_types(solutions.vehicle_data),
            'delivery_data': convert_numpy_types(solutions.delivery_data),
            'depot_coords': convert_numpy_types(solutions.depot_coords)
        }
    }
    
    solutions_file = 'llm/solutions_data.json'
    with open(solutions_file, 'w', encoding='utf-8') as f:
        json.dump(solutions_output, f, indent=4, ensure_ascii=False)
    
    print("\n" + "="*70)
    print(f"Solutions saved to: {solutions_file}")
    print("="*70)
    print("\nTo launch the Streamlit interface, run:")
    print("  cd llm")
    print("  streamlit run interface.py")
    print("="*70)

from address_routes.unify_coordinates import get_unified_coordinates_by_city
import random

def generate_population_coordinates(city: str) -> list[tuple[float, float]]:
    return random.sample(get_unified_coordinates_by_city(city), len(get_unified_coordinates_by_city(city)))

def deliveries_solution_candidate(city: str) -> list[int]:
    if city == "SP":
        return {
            "V1": [1, 5, 4, 13, 20],
            "V2": [2, 3, 19, 21, 14],
            "V3": [6, 7, 8, 9, 15],
            "V4": [10, 22, 16, 17, 18],
            "V5": [12, 11, 23, 24, 25]
        }
    else:
        return

if __name__ == "__main__":
    population_coords = generate_population_coordinates("SP")
    print(population_coords)
    candidate_solution = deliveries_solution_candidate("SP")
    print(candidate_solution)
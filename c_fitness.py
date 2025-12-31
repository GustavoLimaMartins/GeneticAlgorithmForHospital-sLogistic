from address_routes.distribute_center import get_center_coordinates
from a_generate_population import generate_population_coordinates
from b_manhattan_distance import route_distance
from delivery_setup.deliveries import load_deliveries_info as ldi
from delivery_setup.vehicles import load_vehicles_info as lvi

BIG_M = 1e6 # Severe penalty

def fitness(solution: dict[str, list[str]], city: str) -> float:
    deliveries = ldi(city)  # Cities info
    vehicles = lvi(city)    # Vehicles info
    total_cost = 0
    penalty = 0

    for vehicle_id, route in solution:
        vehicle = vehicles[vehicle_id]

        # 1. Capacity
        load = sum(deliveries[d]["demand"] for d in route)
        if load > vehicle["capacity"]:
            penalty += BIG_M * (load - vehicle["capacity"])

        # 2. Manhattan distance of the route
        list_coords = []
        for dlv_id in route:
            list_coords.append((deliveries[dlv_id]['lat'], deliveries[dlv_id]['lon']))

        dist_M = route_distance(list_coords, center_coords=get_center_coordinates(city))

        # 3. Autonomy
        if dist_M > vehicle["max_range_M"]:
            penalty += BIG_M * (dist_M - vehicle["max_range_M"])

        # 4. Travel cost
        travel_cost = dist_M * vehicle["cost_M"]

        # 5. Penalty for delay of critical items
        for pos, d_id in enumerate(route):
            priority = deliveries[d_id]["priority"]
            penalty += pos * priority * 50

        total_cost += travel_cost

    return total_cost + penalty

if __name__ == "__main__":
    candidates_individuals = generate_population_coordinates("SP", 10)
    print(candidates_individuals[0])
    fit_value = fitness(candidates_individuals[0], "SP")
    print(f"Fitness Value: {fit_value}")

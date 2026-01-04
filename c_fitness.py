from address_routes.distribute_center import get_center_coordinates
from a_generate_population import generate_population_coordinates
from b_manhattan_distance import route_distance
from delivery_setup.deliveries import load_deliveries_info as ldi
from delivery_setup.vehicles import load_vehicles_info as lvi

# Weight factors for balanced optimization
CAPACITY_PENALTY = 100      # Reduced from 200 (soft constraint)
AUTONOMY_PENALTY = 200      # Keep high (hard constraint - safety)
CRITICAL_WEIGHT = 12        # Increased from 6 (high priority deliveries)
HIGH_PRIORITY_WEIGHT = 3    # Increased from 1.5 (medium priority)
CRITICAL_POS_WEIGHT = 1.5   # Increased from 0.8 (position penalty)
HIGH_PRIORITY_POS_WEIGHT = 0.6  # Increased from 0.3 (position penalty)
COST_EFFICIENCY_THRESHOLD = 5.0  # Cost per delivery threshold (recalibrated)
COST_EFFICIENCY_WEIGHT = 5  # Penalty weight for inefficient routes (balanced)

def calculate_fitness(solution: dict[str, list[str]], city: str) -> float:
    deliveries = ldi(city)  # Cities info
    vehicles = lvi(city)    # Vehicles info
    total_cost = 0
    penalty = 0

    for route_index, (vehicle_id, route) in enumerate(solution):
        vehicle = vehicles[vehicle_id]

        # 1. Capacity (softer constraint - allows slight overload)
        load = sum(deliveries[d]["demand"] for d in route)
        if load > vehicle["capacity"]:
            penalty += CAPACITY_PENALTY * (load - vehicle["capacity"])

        # 2. Manhattan distance of the route
        list_coords = []
        for dlv_id in route:
            list_coords.append((deliveries[dlv_id]['lat'], deliveries[dlv_id]['lon']))

        dist_M = route_distance(list_coords, center_coords=get_center_coordinates(city))

        # 3. Autonomy (hard constraint - cannot exceed)
        if dist_M > vehicle["max_range_M"]:
            penalty += AUTONOMY_PENALTY * (dist_M - vehicle["max_range_M"])

        # 4. Travel cost (higher weight in total fitness)
        travel_cost = dist_M * vehicle["cost_M"]

        # 5. Cost efficiency penalty (penalizes inefficient routes)
        num_deliveries = len(route)
        if num_deliveries > 0:
            cost_per_delivery = travel_cost / num_deliveries
            if cost_per_delivery > COST_EFFICIENCY_THRESHOLD:
                inefficiency = cost_per_delivery - COST_EFFICIENCY_THRESHOLD
                penalty += inefficiency * COST_EFFICIENCY_WEIGHT

        # 6. Critical delivery penalties (hybrid: linear + quadratic)
        for pos, d_id in enumerate(route):
            priority = deliveries[d_id]["priority"]
            if priority == 3:
                # Critical: linear penalty + quadratic penalty for late routes
                linear_penalty = route_index * CRITICAL_WEIGHT + pos * CRITICAL_POS_WEIGHT
                quadratic_penalty = (route_index ** 2) * 2.0  # Balanced exponential growth
                penalty += linear_penalty + quadratic_penalty
            elif priority == 2:
                # High priority: moderate linear penalty
                penalty += route_index * HIGH_PRIORITY_WEIGHT + pos * HIGH_PRIORITY_POS_WEIGHT

        total_cost += travel_cost

    return total_cost + penalty

if __name__ == "__main__":
    candidates_individuals = generate_population_coordinates("SP", 10)
    print(candidates_individuals[0])
    fit_value = calculate_fitness(candidates_individuals[0], "SP")
    print(f"Fitness Value: {fit_value}")

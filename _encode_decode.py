def encode_individual(vehicle_routes: list[tuple[str, tuple[int]]]) -> list[int]:
    chromosome = []

    for _, deliveries in vehicle_routes:
        chromosome.extend(deliveries)

    return chromosome

def decode_chromosome(chromosome, deliveries, vehicles) -> list[tuple[str, tuple[int]]]:
    all_routes = []
    vehicle_trips = {v: 0 for v in vehicles}
    
    # Create a list to track which deliveries haven't been assigned yet
    remaining_deliveries = list(chromosome)
    
    while remaining_deliveries:
        # Try to create routes for all vehicles in this round
        routes_created = False
        
        for v, info in vehicles.items():
            if not remaining_deliveries:
                break
                
            current_route = []
            current_load = 0
            
            # Build a route for this vehicle
            deliveries_to_remove = []
            
            for gene in remaining_deliveries:
                demand = deliveries[gene]["demand"]
                
                # Check capacity constraint
                if current_load + demand <= info["capacity"]:
                    current_route.append(gene)
                    current_load += demand
                    deliveries_to_remove.append(gene)
            
            # Remove assigned deliveries from remaining list
            for gene in deliveries_to_remove:
                remaining_deliveries.remove(gene)
            
            # Add route if it has deliveries
            if current_route:
                all_routes.append((v, tuple(current_route)))
                vehicle_trips[v] += 1
                routes_created = True
        
        # If no routes were created in this iteration, break to avoid infinite loop
        if not routes_created:
            break
    
    return all_routes

def validate_chromosome(chromosome: list[int], n_deliveries: int):
    assert len(chromosome) == n_deliveries
    assert len(set(chromosome)) == n_deliveries

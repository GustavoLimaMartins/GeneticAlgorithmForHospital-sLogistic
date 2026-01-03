"""
Análise de desbalanceamento entre as variáveis da função fitness
"""
import sys
from pathlib import Path

# Adiciona o diretório pai ao path para importar os módulos
sys.path.insert(0, str(Path(__file__).parent.parent))

from address_routes.distribute_center import get_center_coordinates
from a_generate_population import generate_population_coordinates
from b_manhattan_distance import route_distance
from delivery_setup.deliveries import load_deliveries_info as ldi
from delivery_setup.vehicles import load_vehicles_info as lvi

BIG_M = 200  # Updated to match new balanced value

def analyze_fitness_components(solution: dict[str, list[str]], city: str) -> dict:
    deliveries = ldi(city)
    vehicles = lvi(city)
    
    components = {
        'travel_cost': 0,
        'capacity_penalty': 0,
        'autonomy_penalty': 0,
        'priority_3_penalty': 0,
        'priority_2_penalty': 0
    }
    
    for route_index, (vehicle_id, route) in enumerate(solution):
        vehicle = vehicles[vehicle_id]
        
        # 1. Capacity
        load = sum(deliveries[d]["demand"] for d in route)
        if load > vehicle["capacity"]:
            penalty = BIG_M * (load - vehicle["capacity"])
            components['capacity_penalty'] += penalty
            print(f"  Route {route_index} (V{vehicle_id}): Capacity violation: {load} > {vehicle['capacity']}, Penalty: {penalty:,.0f}")
        
        # 2. Manhattan distance
        list_coords = []
        for dlv_id in route:
            list_coords.append((deliveries[dlv_id]['lat'], deliveries[dlv_id]['lon']))
        
        dist_M = route_distance(list_coords, center_coords=get_center_coordinates(city))
        
        # 3. Autonomy
        if dist_M > vehicle["max_range_M"]:
            penalty = BIG_M * (dist_M - vehicle["max_range_M"])
            components['autonomy_penalty'] += penalty
            print(f"  Route {route_index} (V{vehicle_id}): Autonomy violation: {dist_M:.6f} > {vehicle['max_range_M']:.6f}, Penalty: {penalty:,.0f}")
        
        # 4. Travel cost
        travel_cost = dist_M * vehicle["cost_M"]
        components['travel_cost'] += travel_cost
        print(f"  Route {route_index} (V{vehicle_id}): Distance: {dist_M:.6f}, Cost/unit: {vehicle['cost_M']:.2f}, Travel cost: {travel_cost:.2f}")
        
        # 5. Priority penalties
        for pos, d_id in enumerate(route):
            priority = deliveries[d_id]["priority"]
            if priority == 3:
                penalty = route_index * 6 + pos * 0.8
                components['priority_3_penalty'] += penalty
                print(f"    Delivery {d_id} (P3): route_idx={route_index}, pos={pos}, Penalty: {penalty:,.2f}")
            elif priority == 2:
                penalty = route_index * 1.5 + pos * 0.3
                components['priority_2_penalty'] += penalty
    
    return components

if __name__ == "__main__":
    print("=== ANÁLISE DE DESBALANCEAMENTO DA FUNÇÃO FITNESS ===\n")
    
    # Generate sample population
    candidates = generate_population_coordinates("SP", 5)
    
    for idx, candidate in enumerate(candidates[:3]):  # Analyze first 3
        print(f"\n--- Candidate {idx + 1} ---")
        print(f"Solution: {candidate}\n")
        
        components = analyze_fitness_components(candidate, "SP")
        
        print("\n=== RESUMO DOS COMPONENTES ===")
        total = sum(components.values())
        for name, value in components.items():
            percentage = (value / total * 100) if total > 0 else 0
            print(f"{name:25s}: {value:15,.2f} ({percentage:6.2f}%)")
        print(f"{'TOTAL':25s}: {total:15,.2f}")
        print("\n" + "="*70)

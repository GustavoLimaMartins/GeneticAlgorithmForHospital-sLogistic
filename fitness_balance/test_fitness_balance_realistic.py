"""
Análise de desbalanceamento com soluções mais realistas
"""
import sys
from pathlib import Path

# Adiciona o diretório pai ao path para importar os módulos
sys.path.insert(0, str(Path(__file__).parent.parent))

from b_manhattan_distance import route_distance
from delivery_setup.deliveries import load_deliveries_info as ldi
from delivery_setup.vehicles import load_vehicles_info as lvi
from address_routes.distribute_center import get_center_coordinates

BIG_M = 200  # Updated to match new balanced value

def analyze_realistic_scenarios(city: str):
    deliveries = ldi(city)
    vehicles = lvi(city)
    center = get_center_coordinates(city)
    
    # Cenário 1: Solução viável (sem violações)
    print("=== CENÁRIO 1: SOLUÇÃO VIÁVEL (SEM VIOLAÇÕES) ===\n")
    solution1 = [
        ('V1', [1, 2, 3]),      # 8+12+15=35 <= 45 (OK)
        ('V2', [4, 5]),         # 10+6=16 <= 30 (OK)
        ('V3', [7, 8]),         # 12+15=27 > 20 (VIOLA)
        ('V4', [9, 10]),        # 10+6=16 > 12 (VIOLA)
        ('V5', [6])             # 8 > 6 (VIOLA)
    ]
    
    # Ajustando para não violar
    solution1 = [
        ('V1', [1, 2, 3, 4]),   # 8+12+15+10=45 <= 45 (OK)
        ('V2', [5, 7, 11]),     # 6+12+6=24 <= 30 (OK)
        ('V3', [8, 10]),        # 15+6=21 > 20 (viola 1)
        ('V4', [9]),            # 10 <= 12 (OK)
        ('V5', [6])             # 8 > 6 (viola 2)
    ]
    
    total_cost = 0
    penalty = 0
    
    for route_index, (vehicle_id, route) in enumerate(solution1):
        vehicle = vehicles[vehicle_id]
        
        # Capacity
        load = sum(deliveries[d]["demand"] for d in route)
        if load > vehicle["capacity"]:
            cap_penalty = BIG_M * (load - vehicle["capacity"])
            penalty += cap_penalty
            print(f"Route {route_index} ({vehicle_id}): CAPACIDADE VIOLADA - {load}/{vehicle['capacity']} - Penalidade: {cap_penalty:,.0f}")
        else:
            print(f"Route {route_index} ({vehicle_id}): Capacidade OK - {load}/{vehicle['capacity']}")
        
        # Distance
        list_coords = [(deliveries[d]['lat'], deliveries[d]['lon']) for d in route]
        dist_M = route_distance(list_coords, center)
        
        # Autonomy
        if dist_M > vehicle["max_range_M"]:
            aut_penalty = BIG_M * (dist_M - vehicle["max_range_M"])
            penalty += aut_penalty
            print(f"  AUTONOMIA VIOLADA - {dist_M:.6f}/{vehicle['max_range_M']:.6f} - Penalidade: {aut_penalty:,.0f}")
        else:
            print(f"  Autonomia OK - {dist_M:.6f}/{vehicle['max_range_M']:.6f}")
        
        # Travel cost
        travel_cost = dist_M * vehicle["cost_M"]
        total_cost += travel_cost
        print(f"  Custo de viagem: {travel_cost:.2f}")
        
        # Priority penalties
        for pos, d_id in enumerate(route):
            priority = deliveries[d_id]["priority"]
            if priority == 3:
                p_penalty = route_index * 6 + pos * 0.8
                penalty += p_penalty
                print(f"    Entrega {d_id} (CRÍTICA): pos={pos}, idx={route_index} - Penalidade: {p_penalty:,.2f}")
            elif priority == 2:
                p_penalty = route_index * 1.5 + pos * 0.3
                penalty += p_penalty
        print()
    
    print(f"\nCusto de viagem total: {total_cost:,.2f}")
    print(f"Penalidades totais: {penalty:,.2f}")
    print(f"Fitness total: {total_cost + penalty:,.2f}")
    print(f"\nProporção: Custo={total_cost/(total_cost+penalty)*100:.2f}% vs Penalidades={penalty/(total_cost+penalty)*100:.2f}%")
    
    # Cenário 2: Calculando apenas custos típicos de uma solução viável
    print("\n\n=== CENÁRIO 2: ESTIMATIVA DE ORDENS DE GRANDEZA ===\n")
    print("Assumindo uma solução completamente viável (sem violações):")
    print()
    
    # Custo de viagem típico
    avg_distance = 0.03  # distância média Manhattan típica
    avg_cost_per_unit = 100  # custo médio por unidade
    num_routes = 5
    estimated_travel_cost = avg_distance * avg_cost_per_unit * num_routes
    print(f"Custo de viagem estimado: {estimated_travel_cost:.2f}")
    
    # Penalidades de prioridade (assumindo distribuição típica)
    # Suponha 8 entregas críticas (prioridade 3) distribuídas nas 5 rotas
    priority_penalty = 0
    for route_idx in range(5):
        # Assumindo 1-2 entregas críticas por rota
        for pos in [0, 1]:
            priority_penalty += route_idx * 6 + pos * 0.8
    
    print(f"Penalidades de prioridade estimadas: {priority_penalty:,.2f}")
    print()
    print(f"Total estimado (viável): {estimated_travel_cost + priority_penalty:,.2f}")
    print(f"  Custo: {estimated_travel_cost/(estimated_travel_cost+priority_penalty)*100:.2f}%")
    print(f"  Prioridade: {priority_penalty/(estimated_travel_cost+priority_penalty)*100:.2f}%")
    
    # Comparação com uma única violação pequena
    print("\n\n=== CENÁRIO 3: IMPACTO DE UMA VIOLAÇÃO MÍNIMA ===\n")
    single_violation = BIG_M * 1  # Violação de 1 unidade (ex: 1 kg acima da capacidade)
    print(f"Custo de viagem: {estimated_travel_cost:.2f}")
    print(f"Penalidades de prioridade: {priority_penalty:,.0f}")
    print(f"UMA violação de 1 unidade: {single_violation:,.0f}")
    print()
    total_with_violation = estimated_travel_cost + priority_penalty + single_violation
    print(f"Total: {total_with_violation:,.2f}")
    print(f"  Custo: {estimated_travel_cost/total_with_violation*100:.4f}%")
    print(f"  Prioridade: {priority_penalty/total_with_violation*100:.2f}%")
    print(f"  Violação: {single_violation/total_with_violation*100:.2f}%")

if __name__ == "__main__":
    analyze_realistic_scenarios("SP")

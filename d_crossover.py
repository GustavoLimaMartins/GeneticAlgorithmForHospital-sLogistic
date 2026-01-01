from b_manhattan_distance import cartesian_to_manhattan as manhattan
from _encode_decode import decode_chromosome
import random

def RBX(parent1, parent2, deliveries, vehicles, center):
    routes_p1 = dict(decode_chromosome(parent1, deliveries, vehicles))

    selected_vehicle = random.choice(list(routes_p1.keys()))
    inherited_route = list(routes_p1[selected_vehicle])

    child = inherited_route.copy()

    for gene in parent2:
        if gene not in child:
            child.append(gene)

    return child

def BCRC(parent1, parent2, deliveries):
    i, j = sorted(random.sample(range(len(parent1)), 2))
    subroute = parent1[i:j]

    base = [g for g in parent2 if g not in subroute]

    best_pos = 0
    best_cost = float("inf")

    for pos in range(len(base) + 1):
        candidate = base[:pos] + subroute + base[pos:]
        cost = 0

        for k in range(len(candidate) - 1):
            a = candidate[k]
            b = candidate[k + 1]
            cost += manhattan(
                (deliveries[a]["lat"], deliveries[a]["lon"]),
                (deliveries[b]["lat"], deliveries[b]["lon"])
            )

        if cost < best_cost:
            best_cost = cost
            best_pos = pos

    return base[:best_pos] + subroute + base[best_pos:]

def crossover(parent1, parent2, deliveries, vehicles, center,
    p_rbx=0.5):

    if random.random() < p_rbx:
        return RBX(parent1, parent2, deliveries, vehicles, center)
    else:
        return BCRC(parent1, parent2, deliveries)

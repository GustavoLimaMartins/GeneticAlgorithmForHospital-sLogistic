import random

def tournament_selection(population: list[dict], k: int = 2) -> dict:
    contenders = random.sample(population, k)
    return min(contenders, key=lambda ind: ind["fitness"])

def get_elite(population: list[dict], elite_ratio: float = 0.035) -> list[dict]:
    elite_size = max(1, int(len(population) * elite_ratio))
    return sorted(population, key=lambda ind: ind["fitness"])[:elite_size]

def select_next_generation(
    population: list[dict],
    pop_size: int,
    elite_ratio: float = 0.035,
    tournament_k: int = 2
    ) -> list[dict]:

    # 1. Elite selection
    elite = get_elite(population, elite_ratio)
    selected = elite[:]

    # 2. Fill the rest via tournament
    while len(selected) < pop_size:
        parent = tournament_selection(population, k=tournament_k)
        selected.append(parent)

    return selected

import random

def generate_population_coordinates(city: str, pop_size: int) -> list[tuple[float, float]]:
    dev_setup = deliveries_solution_candidate(city)
    dev_shuffle = random.sample(sorted(dev_setup.values()), len(dev_setup))
    print(dev_shuffle)
    vei_shuffle = random.sample(sorted(dev_setup.keys()), len(dev_setup))
    
    return [list(zip(vei_shuffle, dev_shuffle)) for _ in range(pop_size)]

def deliveries_solution_candidate(city: str) -> dict[str, tuple[int, ...]]:
    if city == "SP":
        # Pool de IDs únicos de entregas (1 a 25)
        delivery_ids = list(range(1, 26))
        random.shuffle(delivery_ids)
        
        # Distribui aleatoriamente em 5 veículos com 5 entregas cada
        return {
            "V1": tuple(delivery_ids[0:5]),
            "V2": tuple(delivery_ids[5:10]),
            "V3": tuple(delivery_ids[10:15]),
            "V4": tuple(delivery_ids[15:20]),
            "V5": tuple(delivery_ids[20:25])
        }
    else:
        return {}

if __name__ == "__main__":
    population_coords = generate_population_coordinates("SP", 5)
    print(population_coords)

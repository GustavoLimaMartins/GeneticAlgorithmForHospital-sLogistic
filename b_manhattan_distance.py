def cartesian_to_manhattan(coord1: tuple[float, float], coord2: tuple[float, float]) -> float:
    """
    Calculate the Manhattan distance between two Cartesian coordinates.

    Parameters:
    coord1 (tuple[float, float]): The first coordinate (x1, y1).
    coord2 (tuple[float, float]): The second coordinate (x2, y2).

    Returns:
    float: The Manhattan distance between the two coordinates.
    """
    return abs(coord1[0] - coord2[0]) + abs(coord1[1] - coord2[1])

def route_distance(population: list[tuple[float, float]], center_coords: list[float, float]) -> float:
    distance = 0
    
    #print("Center Coordinates:", center_coords)
    #print("Population Coordinates:", population)

    # Intial point
    distance += cartesian_to_manhattan(center_coords, population[0])
    # Intermediate points
    for i in range(len(population) - 1):
        distance += cartesian_to_manhattan(population[i], population[i + 1])
    # Return to depot
    distance += cartesian_to_manhattan(population[-1], center_coords)

    return distance

from address_routes.unify_coordinates import get_unified_coordinates_by_city
from numpy import median

def get_center_coordinates(city: str) -> tuple[float, float]:
    coordinates = get_unified_coordinates_by_city(city)
    center = median(coordinates, axis=0)
    return center

if __name__ == "__main__":
    center_coords = get_center_coordinates("SP")
    print(center_coords)
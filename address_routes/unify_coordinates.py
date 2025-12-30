from address_routes.einstein_units import hospitalar_units_lat_lon

def get_unified_coordinates_by_city(city: str) -> list[tuple[float, float]]:
    unified_coordinates = []
    for key in hospitalar_units_lat_lon[city].keys():
        lat, lon = hospitalar_units_lat_lon[city][key]
        unified_coordinates.append((lat, lon))

    return unified_coordinates

if __name__ == "__main__":
    coords = get_unified_coordinates_by_city("SP")
    print(coords)
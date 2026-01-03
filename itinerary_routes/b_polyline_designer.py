import polyline

class PolylineDesigner:
    def __init__(self, directions: dict):
        self.directions = directions

    def extract_coordinates(self):
        coords = []
        leg_start_points = []

        for leg in self.directions[0]['legs']:
            leg_start_points.append((
                leg['start_location']['lat'],
                leg['start_location']['lng']
            ))

            for step in leg['steps']:
                decoded = polyline.decode(step['polyline']['points'])

                if coords and decoded[0] == coords[-1]:
                    decoded = decoded[1:]

                coords.extend(decoded)

        # último ponto (fim)
        leg_start_points.append((
            self.directions[0]['legs'][-1]['end_location']['lat'],
            self.directions[0]['legs'][-1]['end_location']['lng']
        ))

        return coords, leg_start_points

if __name__ == "__main__":
    from a_google_maps import GoogleMapsAPI
    gmaps_api = GoogleMapsAPI()
    origin = (-23.55052, -46.633308)  # São Paulo
    destination = (-23.559616, -46.658481)  # Another point in São Paulo
    waypoints = [(-23.555, -46.64), (-23.557, -46.65)]

    directions = gmaps_api.get_directions(origin, destination, waypoints)
    poly_designer = PolylineDesigner(directions)
    coords, leg_starts = poly_designer.extract_coordinates()
    print("Coordinates:", coords)
    print("Leg Start Points:", leg_starts)


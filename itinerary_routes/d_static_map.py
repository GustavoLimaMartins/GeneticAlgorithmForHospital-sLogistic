from itinerary_routes._solution_type import SolutionMethod
from staticmap import StaticMap, Line, CircleMarker
from pathlib import Path

class StaticMapRoute:
    def __init__(self, coords: list[tuple[float, float]] | list[list[tuple[float, float]]], leg_start_points: list[tuple[float, float]], iterator: int = 0, generation: int = 0, route_id: int = 0):
        self.coords = coords
        self.leg_start_points = leg_start_points
        self.iterator = iterator
        self.generation = generation
        self.route_id = route_id
        self.color_palette = ['red', 'orange', 'yellow', 'green', 'blue', 'purple', 'pink', 'brown', 'gray', 'black', 'cyan', 'magenta']

    def png_path(self, solution_method: SolutionMethod) -> str:
        if solution_method not in SolutionMethod:
            raise ValueError("Invalid solution method. Choose 'fitness' or 'metrics'.")
        elif solution_method == SolutionMethod.FITNESS:
            self.routes_dir = Path(__file__).parent / "routes_maps/fitness"
        elif solution_method == SolutionMethod.METRICS:
            self.routes_dir = Path(__file__).parent / "routes_maps/metrics"
        
        self.routes_dir.mkdir(parents=True, exist_ok=True)
        return str(self.routes_dir / f"i{self.iterator}_by_{solution_method.value}_{self.route_id}route_map_{self.generation}gen.png")
    
    def create_static_map(self, solution_method: SolutionMethod):
        png_path = self.png_path(solution_method)
        map_image = StaticMap(1200, 800, url_template='http://a.tile.osm.org/{z}/{x}/{y}.png')

        # Draw each segment with a different color
        if isinstance(self.coords[0], list):
            # Coords is a list of lists (one segment per leg)
            for i, leg_coords in enumerate(self.coords):
                color = self.color_palette[i % len(self.color_palette)]
                line_coords = [(lon, lat) for lat, lon in leg_coords]
                map_image.add_line(Line(line_coords, color, 3))
        else:
            # Coords is a single list (draw one line)
            line_coords = [(lon, lat) for lat, lon in self.coords]
            map_image.add_line(Line(line_coords, 'blue', 3))

        # Add markers for leg start points
        num_points = len(self.leg_start_points)
        color_palette = ['red', 'orange', 'yellow', 'green', 'blue', 'purple', 'pink', 'brown', 'gray', 'black']
        colors = [color_palette[i % len(color_palette)] for i in range(num_points)]
        
        for point, color in zip(self.leg_start_points, colors):
            lat, lon = point
            map_image.add_marker(CircleMarker((lon, lat), color, 10))

        image = map_image.render()
        image.save(png_path)

        print(f"PNG image saved at: {png_path}")

if __name__ == "__main__":
    from a_google_maps import GoogleMapsAPI
    from b_polyline_designer import PolylineDesigner
    gmaps_api = GoogleMapsAPI()
    origin = (-23.55052, -46.633308)  # São Paulo
    destination = (-23.559616, -46.658481)  # Another point in São Paulo
    waypoints = [(-23.555, -46.64), (-23.557, -46.65)]
    directions = gmaps_api.get_directions(origin, destination, waypoints)
    poly_designer = PolylineDesigner(directions)
    coords, leg_starts = poly_designer.extract_coordinates_with_onecolor()
    static_map_route = StaticMapRoute(coords, leg_starts, iterator=1, generation=1, route_id=1)
    static_map_route.create_static_map(SolutionMethod.FITNESS)

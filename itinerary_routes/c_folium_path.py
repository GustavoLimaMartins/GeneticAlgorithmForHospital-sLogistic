import folium
from pathlib import Path
from itinerary_routes._solution_type import SolutionMethod

class FoliumPath:
    def __init__(self, coords: list[tuple[float, float]] | list[list[tuple[float, float]]], leg_start_points: list[tuple[float, float]], iterator: int = 0, generation: int = 0, route_id: int = 0):
        self.coords = coords
        self.leg_start_points = leg_start_points
        self.iterator = iterator
        self.generation = generation
        self.route_id = route_id
        self.color_palette = ['red', 'blue', 'green', 'purple', 'orange', 'darkred', 'lightred', 'beige', 'darkblue', 'darkgreen', 'cadetblue', 'darkpurple', 'pink', 'lightblue', 'lightgreen', 'gray', 'black', 'lightgray']

    def html_path(self, solution_method: SolutionMethod) -> str:
        if solution_method not in SolutionMethod:
            raise ValueError("Invalid solution method. Choose 'fitness' or 'metrics'.")
        elif solution_method == SolutionMethod.FITNESS:
            self.routes_dir = Path(__file__).parent / "routes_maps/fitness"
        elif solution_method == SolutionMethod.METRICS:
            self.routes_dir = Path(__file__).parent / "routes_maps/metrics"
        
        self.routes_dir.mkdir(parents=True, exist_ok=True)
        return str(self.routes_dir / f"i{self.iterator}_by_{solution_method.value}_{self.route_id}route_map_{self.generation}gen.html")
    
    def create_html_map(self, solution_method: SolutionMethod):
        # Define initial location for centering the map
        if isinstance(self.coords[0], list):
            initial_location = self.coords[0][0]
        else:
            initial_location = self.coords[0]
        
        m = folium.Map(
            location=initial_location,
            zoom_start=14,
            tiles="OpenStreetMap"
        )

        # Draw each segment with a different color
        if isinstance(self.coords[0], list):
            # Coords is a list of lists (one segment per leg)
            for i, leg_coords in enumerate(self.coords):
                color = self.color_palette[i % len(self.color_palette)]
                folium.PolyLine(
                    leg_coords,
                    color=color,
                    weight=4,
                    opacity=0.9
                ).add_to(m)
        else:
            # Coords is a single list (draw one line)
            folium.PolyLine(
                self.coords,
                weight=4,
                opacity=0.9
            ).add_to(m)

        labels = []
        for point in self.leg_start_points:
            if point == self.leg_start_points[0]:
                labels.append("Distribute Center")
            elif point == self.leg_start_points[-1]:
                labels.append("Distribute Center")
            else:
                labels.append(f"Hospital {self.leg_start_points.index(point)}")

        for point, label in zip(self.leg_start_points, labels):
            folium.Marker(
                location=point,
                popup=label
            ).add_to(m)

        m.save(self.html_path(solution_method))

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
    folium_path = FoliumPath(coords, leg_starts, iterator=1, generation=1, route_id=1)
    folium_path.create_html_map(SolutionMethod.FITNESS)

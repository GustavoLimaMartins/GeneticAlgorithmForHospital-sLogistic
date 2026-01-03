from staticmap import StaticMap, Line, CircleMarker
from pathlib import Path

class StaticMapRoute:
    def __init__(self, coords: list[tuple[float, float]], leg_start_points: list[tuple[float, float]]):
        self.coords = coords
        self.leg_start_points = leg_start_points

    def png_path(self, index: int) -> str:
        # Create routes_maps directory if it doesn't exist
        routes_dir = Path(__file__).parent / "routes_maps"
        routes_dir.mkdir(exist_ok=True)
        return str(routes_dir / f"{index}_routes.png")
    
    def create_static_map(self, png_index: int):
        png_path = self.png_path(png_index)
        map_image = StaticMap(1200, 800, url_template='http://a.tile.osm.org/{z}/{x}/{y}.png')

        # Add route line
        line_coords = [(lon, lat) for lat, lon in self.coords]
        map_image.add_line(Line(line_coords, 'blue', 3))

        # Add markers for leg start points
        colors = ['red', 'orange', 'orange', 'green']
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
    coords, leg_starts = poly_designer.extract_coordinates()
    static_map_route = StaticMapRoute(coords, leg_starts)
    static_map_route.create_static_map(1)

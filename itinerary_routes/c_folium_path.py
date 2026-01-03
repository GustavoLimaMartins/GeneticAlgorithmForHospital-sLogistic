import folium

class FoliumPath:
    def __init__(self, coords: list[tuple[float, float]], leg_start_points: list[tuple[float, float]]):
        self.coords = coords
        self.leg_start_points = leg_start_points

    def html_path(self, index: int) -> str:
        return fr"routes_maps\{index}_route_map.html"
    
    def create_map(self, html_index: int):
        m = folium.Map(
            location=self.coords[0],
            zoom_start=14,
            tiles="OpenStreetMap"
        )

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

        m.save(self.html_path(html_index))

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
    folium_path = FoliumPath(coords, leg_starts)
    folium_path.create_map(1)

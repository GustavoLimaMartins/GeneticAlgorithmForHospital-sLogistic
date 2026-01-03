import googlemaps
import os
from dotenv import load_dotenv
load_dotenv()


class GoogleMapsAPI:
    def __init__(self):
        self.GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
        self.client = googlemaps.Client(key=self.GOOGLE_MAPS_API_KEY)

    def get_directions(self, origin: tuple[float, float], 
                       destination: tuple[float, float], 
                       waypoints: list[tuple[float, float]] = None, 
                       mode: str = "driving"
                       ) -> dict:
        
        directions = self.client.directions(
            origin=origin,
            destination=destination,
            waypoints=waypoints,
            mode=mode,
            optimize_waypoints=False,
            departure_time="now"
        )
        return directions


if __name__ == "__main__":
    gmaps_api = GoogleMapsAPI()
    origin = (-23.55052, -46.633308)  # São Paulo
    destination = (-23.559616, -46.658481)  # Another point in São Paulo
    waypoints = [(-23.555, -46.64), (-23.557, -46.65)]
    
    directions = gmaps_api.get_directions(origin, destination, waypoints)
    print(directions)


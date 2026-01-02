import googlemaps
import os
from dotenv import load_dotenv
load_dotenv()

#TODO Create a class to handle Google Maps API interactions
#TODO Object returns 'directions' variable with route information

GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)

origin = (-23.5505, -46.6333)

waypoints = [
    (-23.5629, -46.6544),  # ponto intermediário 1
    (-23.5893, -46.6740),  # ponto intermediário 2
]

destination = (-23.6824, -46.5165)


directions = gmaps.directions(
    origin=origin,
    destination=destination,
    waypoints=waypoints,
    mode="driving",
    optimize_waypoints=False,
    departure_time="now"
)

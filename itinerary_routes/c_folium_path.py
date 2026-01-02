from itinerary_routes.b_polyline_designer import coords, leg_start_points
import folium

#TODO Create a class to handle Folium map creation and route plotting
#TODO Desconsider 'coords' and 'leg_start_points' variables from b_polyline_designer.py

# Salvar mapa interativo em HTML
m = folium.Map(
    location=coords[0],
    zoom_start=14,
    tiles="OpenStreetMap"
)

folium.PolyLine(
    coords,
    weight=4,
    opacity=0.9
).add_to(m)

labels = ["Origem", "Parada 1", "Parada 2", "Destino"]

for point, label in zip(leg_start_points, labels):
    folium.Marker(
        location=point,
        popup=label
    ).add_to(m)

html_path = r"itinerary_routes\routes_maps\routes.html"
m.save(html_path)

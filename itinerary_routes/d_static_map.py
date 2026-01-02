from itinerary_routes.b_polyline_designer import coords, leg_start_points
from staticmap import StaticMap, Line, CircleMarker

#TODO Create a class to handle static map creation and route plotting
#TODO Desconsider 'coords' and 'leg_start_points' variables from b_polyline_designer.py

# Salvar como PNG usando staticmap (sem browser)
png_path = r"itinerary_routes\routes_maps\routes.png"

map_image = StaticMap(1200, 800, url_template='http://a.tile.osm.org/{z}/{x}/{y}.png')

# Adicionar linha da rota
line_coords = [(lon, lat) for lat, lon in coords]
map_image.add_line(Line(line_coords, 'blue', 3))

# Adicionar marcadores
colors = ['red', 'orange', 'orange', 'green']
for point, color in zip(leg_start_points, colors):
    lat, lon = point
    map_image.add_marker(CircleMarker((lon, lat), color, 10))

image = map_image.render()
image.save(png_path)

print(f"Imagem PNG salva em: {png_path}")
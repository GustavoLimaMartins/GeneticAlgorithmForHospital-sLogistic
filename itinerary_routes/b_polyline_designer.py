from itinerary_routes.a_google_maps import directions
import polyline

#TODO Create a class to handle Polyline decoding and coordinate extraction
#TODO Desconsider 'directions' variable from a_google_maps.py

coords = []
leg_start_points = []

for leg in directions[0]['legs']:
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
    directions[0]['legs'][-1]['end_location']['lat'],
    directions[0]['legs'][-1]['end_location']['lng']
))

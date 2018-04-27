'''
Software Design Final Project: Trail Blazer
'''
import overpy
import geopy
from geopy.distance import VincentyDistance, vincenty
import geographiclib
from geographiclib.geodesic import Geodesic
import folium
import matplotlib.pyplot as plt
import mplleaflet

api = overpy.Overpass()

def get_nearest_node(lat, lng):
    lat1 = (lat - 0.0015)
    lng1 = (lng - 0.0015)
    lat2 = (lat + 0.0015)
    lng2 = (lng + 0.0015)
    query_str = """
        way({}, {}, {}, {}) ["highway"];
        (._;>;);
        out body;
        """.format(lat1, lng1, lat2, lng2)
    result = api.query(query_str)

    # Gets all of the valid nodes/points that are on roads or paths.
    all_nodes = {}
    all_vertices = []
    for way in result.ways:
        for node in way.nodes:
            all_nodes[node] = all_nodes.get(node, 0) + 1
            all_vertices.append(node)

    # Creates a list of the points that are intersections.
    intersections = []
    for node in all_nodes:
        if all_nodes[node] > 1:
            intersections.append(node)
    position = (lat, lng)
    first_try = (intersections[0].lat, intersections[0].lon)
    closest = [intersections[0], vincenty(first_try, position).km]
    for i in range(1, len(intersections)):
        coord = (intersections[i].lat, intersections[i].lon)
        distance = vincenty(coord, position).km
        if distance < closest[1]:
            closest[0] = intersections[i]
            closest[1] = distance

    return closest[0]

print(get_nearest_node(42.29783, -71.257871))

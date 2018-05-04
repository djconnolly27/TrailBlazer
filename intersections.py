'''
Software Design Final Project: Trail Blazer

Intersections.py takes starting coordinates and a distance and finds and plots a nonoverlapping route of that length that starts at that point.
'''
from geopy.distance import vincenty
from graph import Graph

def get_nearest_node(api, lat, lng):
    ''' Finds and returns the node nearest to a given set of lat-lng coordinates. '''
    small_graph = Graph(api, lat, lng, 0.0015)
    small_graph.get_ways_in_area()
    small_graph.get_vertices()
    small_graph.get_intersections()

    position = (lat, lng)
    first_try = (small_graph.intersections[0].lat, small_graph.intersections[0].lon)
    closest = [small_graph.intersections[0], vincenty(first_try, position).km]
    for i in range(1, len(small_graph.intersections)):
        coord = (small_graph.intersections[i].lat, small_graph.intersections[i].lon)
        distance = vincenty(coord, position).km
        if distance < closest[1]:
            closest[0] = small_graph.intersections[i]
            closest[1] = distance
    return closest[0]

def graph_it(api, lat, lng, radius, distance):
    ''' Finds and graphs a cycle of a given length starting from near a given lat-lng point. '''
    start = get_nearest_node(api, lat, lng)
    full_graph = Graph(api, lat, lng, radius)
    full_graph.get_route_coords(distance, start)
    return full_graph

def find_route_coords(graph):
    ''' Gets a list of tuples containing coordinates along the route. '''
    coords = []
    for i in range(len(graph.lats)):
        coords.append((float(graph.lats[i]), float(graph.lons[i])))
    return coords

def plot_graph(graph):
    ''' Plots a route on a map. '''
    return graph.show_route()

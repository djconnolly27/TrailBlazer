'''
Software Design Final Project: Trail Blazer

Intersections.py takes a bounding area, finds all of the paths in that area, and designates the parts of those paths as nodes and edges.
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

# fetch all ways and nodes
# result = api.query("""
#     way(42.288761, -71.244837, 42.291047, -71.241189) ["highway"];
#     (._;>;);
#     out body;
#     """)
result = api.query("""
    way(42.267275, -71.330775, 42.338246, -71.198266) ["highway"];
    (._;>;);
    out body;
    """)
# Outside West Hall = overpy.Node id=530968968 lat=42.2929279 lon=-71.2630597

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


class Edge():
    ''' Defines edges, which are the parts of roads or paths that connect the nodes (intersections) to one another. An edge contains a start node, an end node, a list of points, and a length. '''

    def __init__(self):
        ''' Initializes the edge with an empty list of points and a length of zero '''
        self.node_list = []
        self.length = 0

    def set_start_node(self, start_node):
        ''' Defines the first end node of an edge '''
        self.start = start_node

    def set_end_node(self, end_node):
        ''' Defines the second end node of an edge '''
        self.end = end_node

    def add_node(self, node):
        ''' Adds a point to the list of points that comprise the edge '''
        self.node_list.append(node)

    def add_multiple_nodes(self, nodes):
        ''' Adds a list of points to the list of points that comprise the edge '''
        self.node_list.extend(nodes)

    def update_distance(self):
        ''' Updates the length of the edge '''
        if len(self.node_list) > 0:
            first_coord = (self.start.lat, self.start.lon)
            last_coord = (self.end.lat, self.end.lon)
            self.length += vincenty((self.node_list[0].lat, self.node_list[0].lon), first_coord).km
            self.length += vincenty((self.node_list[-1].lat, self.node_list[-1].lon), last_coord).km
            for i in range(len(self.node_list) - 1):
                self.length += vincenty((self.node_list[i+1].lat, self.node_list[i+1].lon), (self.node_list[i].lat, self.node_list[i].lon)).km
        else:
            first_coord = (self.start.lat, self.start.lon)
            last_coord = (self.end.lat, self.end.lon)
            self.length += vincenty(first_coord, last_coord).km

    def get_bearing(self):
        bearing = Geodesic.WGS84.Inverse(self.start.lat, self.start.lon, self.end.lat, self.end.lon)['azi1']
        if bearing < 0.0:
            return bearing + 360.0
        else:
            return bearing


def find_nodes_and_edges():
    ''' Taking all of the paths/roads in the given area, this breaks up those paths/roads into edges and stores in a list.'''
    edge_list = []
    for way in result.ways:
        breakpoints = []
        for i in range(len(way.nodes)):
            if way.nodes[i] in intersections:
                breakpoints.append(i)
        if breakpoints == []:
            new_edge = Edge()
            new_edge.set_start_node(way.nodes[0])
            new_edge.set_end_node(way.nodes[-1])
            if len(way.nodes) > 2:
                new_edge.add_multiple_nodes(way.nodes[1:-1])
            new_edge.update_distance()
            edge_list.append(new_edge)
        else:
            new_ways = []
            for x in range(len(breakpoints) - 1):
                new_ways.append(way.nodes[breakpoints[x]:breakpoints[x+1] + 1])
            for y in new_ways:
                new_edge = Edge()
                new_edge.set_start_node(y[0])
                new_edge.set_end_node(y[-1])
                if len(y) > 2:
                    new_edge.add_multiple_nodes(y[1:-1])
                new_edge.update_distance()
                edge_list.append(new_edge)
    return edge_list

def get_neighboring_nodes(edge_list):
    neighboring_nodes = {}
    for new_edge in edge_list:
        # The following section determines which nodes neighbor one another and how far each neighboring node is from the origin node.
        if new_edge.start in neighboring_nodes and new_edge.end in neighboring_nodes:
            neighboring_nodes[new_edge.start].append(new_edge.end)
            neighboring_nodes[new_edge.end].append(new_edge.start)
        elif new_edge.start in neighboring_nodes:
            neighboring_nodes[new_edge.start].append(new_edge.end)
            neighboring_nodes[new_edge.end] = [new_edge.start]
        elif new_edge.end in neighboring_nodes:
            neighboring_nodes[new_edge.end].append(new_edge.start)
            neighboring_nodes[new_edge.start] = [new_edge.end]
        else:
            neighboring_nodes[new_edge.start] = [new_edge.end]
            neighboring_nodes[new_edge.end] = [new_edge.start]
    return neighboring_nodes

edge_list = find_nodes_and_edges()
neighboring_nodes = get_neighboring_nodes(edge_list)

nodes_edges = {}
for edge in edge_list:
    ends = edge.start, edge.end
    nodes_edges[ends] = edge
    reverse_ends = edge.end, edge.start
    nodes_edges[reverse_ends] = edge

#
# nodes_by_id = []
# id_to_node = {}
# for way in result.ways:
#     for node in way.nodes:
#         nodes_by_id.append(node.id)
#         id_to_node[node.id] = node

def find_cycle2(path_length, visited):
    found = []
    if len(visited) < 25:
        for neighbor in neighboring_nodes[visited[len(visited) - 1]]:
            if len(found) < 1:
                if neighbor == visited[0] and len(visited) != 2:
                    new_path_length = path_length - nodes_edges[(visited[len(visited) - 1], neighbor)].length
                    if new_path_length < 0.0:
                        found.append(list(visited + [neighbor]))
                elif neighbor not in visited:
                    new_path_length = path_length - nodes_edges[(visited[len(visited) - 1], neighbor)].length
                    if new_path_length > 0.0:
                        found.extend(find_cycle2(new_path_length, list(visited + [neighbor])))
    return found

for node in neighboring_nodes:
    if node.id == 530968968:
        my_node = node

potential_cycles = find_cycle2(2.0, [my_node])
for cyc in potential_cycles:
    print(cyc)
    print()

lats = []
lons = []
for node in potential_cycles[0]:
    lats.append(node.lat)
    lons.append(node.lon)

plt.hold(True)

plt.plot(lons, lats, 'ro')
plt.plot(lons, lats, 'b')
mplleaflet.show()

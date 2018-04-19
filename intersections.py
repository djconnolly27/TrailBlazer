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
    ''' Taking all of the paths/roads in the given area, this breaks up those paths/roads into nodes and edges, which it stores in a dictionary and list, respectively. '''
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

import networkx as nx
import matplotlib.pyplot as plt
G = nx.Graph()
for vertex in intersections:
    G.add_node(vertex.id, coord=(float(vertex.lat), float(vertex.lon)))
count = 0
for path in edge_list:
    count += 1
    G.add_edge(path.start.id, path.end.id, weight=path.length)

cycle = nx.find_cycle(G, 530968968)

all_cycles=nx.cycle_basis(G)
for cycle in all_cycles:
    if 530968968 in cycle:
        print(cycle)

# G.remove_node(68330106)
# G.remove_node(1934014646)

# nx.draw(G,nx.get_node_attributes(G, 'coord'),node_size=2)
# plt.show()

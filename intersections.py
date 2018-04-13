'''
Software Design Final Project: Trail Blazer

Intersections.py takes a bounding area, finds all of the paths in that area, and designates the parts of those paths as nodes and edges.
'''
import overpy
import geopy
from geopy.distance import VincentyDistance, vincenty

api = overpy.Overpass()

# fetch all ways and nodes
result = api.query("""
    way(42.288761, -71.244837, 42.291047, -71.241189) ["highway"];
    (._;>;);
    out body;
    """)

# Gets all of the valid nodes/points that are on roads or paths.
all_nodes = {}
for way in result.ways:
    for node in way.nodes:
        all_nodes[node] = all_nodes.get(node, 0) + 1

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

    def update_distance(self):
        ''' Updates the length of the edge '''
        if len(self.node_list) > 0:
            first_coord = (self.start.lat, self.start.lon)
            last_coord = (self.end.lat, self.end.lon)
            self.length += vincenty((self.node_list[0].lat, self.node_list[0].lon), first_coord).km
            self.length += vincenty((self.node_list[-1].lat, self.node_list[-1].lon), last_coord).km
            for i in range(len(self.node_list) - 1):
                self.length += vincenty((self.node_list[i+1].lat, self.node_list[i+1].lon), (self.node_list[i].lat, self.node_list[i].lon)).km


def find_nodes_and_edges():
    ''' Taking all of the paths/roads in the given area, this breaks up those paths/roads into nodes and edges, which it stores in a dictionary and list, respectively. '''
    edge_list = []
    neighboring_nodes = {}
    for way in result.ways:
        new_edge = Edge()
        for node in way.nodes:
            length = 0

            #The following breaks the 'ways,' which represent paths/roads, up into edges, which contain only the section of the path/road between two intersections.
            if not hasattr(new_edge, 'start') and new_edge.node_list == []:
                new_edge.set_start_node(node)
            elif node not in intersections:
                new_edge.add_node(node)
            else:
                new_edge.set_end_node(node)
                new_edge.update_distance()
                edge_list.append(new_edge)

                # The following section determines which nodes neighbor one another and how far each neighboring node is from the origin node.
                if new_edge.start in neighboring_nodes and new_edge.end in neighboring_nodes:
                    neighboring_nodes[new_edge.start].append((new_edge.end, new_edge.length))
                    neighboring_nodes[new_edge.end].append((new_edge.start, new_edge.length))
                elif new_edge.start in neighboring_nodes:
                    neighboring_nodes[new_edge.start].append((new_edge.end, new_edge.length))
                    neighboring_nodes[new_edge.end] = [(new_edge.start, new_edge.length)]
                elif new_edge.end in neighboring_nodes:
                    neighboring_nodes[new_edge.end].append((new_edge.start, new_edge.length))
                    neighboring_nodes[new_edge.start] = [(new_edge.end, new_edge.length)]
                else:
                    neighboring_nodes[new_edge.start] = [(new_edge.end, new_edge.length)]
                    neighboring_nodes[new_edge.end] = [(new_edge.start, new_edge.length)]

                new_edge = Edge()
    return edge_list, neighboring_nodes

edge_list, neighboring_nodes = find_nodes_and_edges()

class Node():
    ''' Defines a node, which represents an intersection of two paths/roads. A node contains information regarding its neighboring nodes and how far each neighbor is from the origin node. '''

    def __init__(self, node):
        ''' Initializes a node with itself and an empty list of neighbors. '''
        self.node = node
        self.neighbors = []

    def add_neighbors(self, nodes):
        ''' Adds all of a nodes neighbors and their respective distances from the origin node to a list of tuples. '''
        self.neighbors.extend(nodes)

# Creates a list of Nodes.
node_list = []
for node in neighboring_nodes:
    new_node = Node(node)
    new_node.add_neighbors(neighboring_nodes[node])
    node_list.append(new_node)

# for node in node_list:
#     print(node.node)
#     print(node.neighbors)
#     print()

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
# result = api.query("""
#     way(42.292916, -71.263133, 42.292928, -71.263053) ["highway"];
#     (._;>;);
#     out body;
#     """)
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
        #if way.id == 570834600:
        #print(way.nodes)
        breakpoints = []
        for i in range(len(way.nodes)):
            if way.nodes[i] in intersections:
                # if i != 0 and i != (len(way.nodes) - 1):
                breakpoints.append(i)
        if breakpoints == []:
            new_edge = Edge()
            new_edge.set_start_node(way.nodes[0])
            new_edge.set_end_node(way.nodes[-1])
            if len(way.nodes) > 2:
                new_edge.add_multiple_nodes(way.nodes[1:-1])
            #print(new_edge.node_list)
            new_edge.update_distance()
            edge_list.append(new_edge)
        else:
            new_ways = []
            for x in range(len(breakpoints) - 1):
                new_ways.append(way.nodes[breakpoints[x]:breakpoints[x+1] + 1])
            #print(new_ways)
            for y in new_ways:
                new_edge = Edge()
                new_edge.set_start_node(y[0])
                new_edge.set_end_node(y[-1])
                if len(y) > 2:
                    new_edge.add_multiple_nodes(y[1:-1])
                #print(new_edge.node_list)
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
all_edges = []
for edge in edge_list:
    ends = edge.start, edge.end
    nodes_edges[ends] = edge
    # reverse_edge = Edge()
    # reverse_edge.set_end_node(edge.start)
    # reverse_edge.set_start_node(edge.end)
    # reverse_edge.add_multiple_nodes(edge.node_list[::-1])
    # reverse_edge.update_distance()
    # reverse_ends = edge.end, edge.start
    # nodes_edges[reverse_ends] = reverse_edge
    # all_edges.append(edge)
    # all_edges.append(reverse_edge)
#edge_list, neighboring_nodes, nodes_edges = find_nodes_and_edges()

# for edge in edge_list:
#     print(edge.get_bearing())

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
    if node.id == 530968968:
        my_node = node
        #print(neighboring_nodes[node])
    #elif node.id == 530968968:
    #    first = node
    elif node.id == 531000239:
        last = node

# print(node_list)
# for node in node_list:
#     print(node.node)
#     print(node.neighbors)

# for x in nodes_edges:
#     if x[0].id == 530968968 or x[1].id == 530968968:
#         print(x)
#         print(nodes_edges[x])
#         print()

# combo = my_node, last
# if combo in nodes_edges:
#     print(nodes_edges[combo])

def find_path_one_direction(graph, start, bearing, distance, epsilon=45.0, path=[]):
    path = path + [start]
    if distance < 0.25 and distance > -0.25:
        return path
    if not start in graph:
        return None
    #print(start)
    #print(graph[start])
    for node in graph[start]:
        for other_node in nodes_edges:
            print(other_node)
            print(nodes_edges[other_node].get_bearing())
        # for edge, start_end in nodes_edges.items():
        #     if start_end[0] == start and start_end[1] == node:
        #         print(edge.get_bearing())
        #print(node.id)
        # for edge in edge_list:
        #     #print(edge.start)
        #     #print(edge.end)
        #     #print(edge.get_bearing())
        #     if edge.start == start and edge.end == node:
        #         print('Success')
        #         my_edge = edge
        # start_id = start.id
        # node_id = node.id
        # val = start_id, node_id
        #print(nodes_edges[start_id, node_id])
        if abs(my_edge.get_bearing() - bearing) <= epsilon:
            if node not in path:
                new_distance = distance - my_edge.length
                newpath = find_path_one_direction(graph, node, bearing, new_distance, path)
                if newpath:
                    return newpath
        else:
            epsilon += 10.0
            return find_path_one_direction(graph, start, bearing, distance, epsilon, path)
        # if node not in path:
        #     newpath = find_path(graph, node, end, path)
        #     if newpath:
        #         return newpath
    return None

def find_path_back(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        return path
    if not start in graph:
        return None
    for node in graph[start]:
        if node not in path:
            newpath = find_path_back(graph, node, end, path)
            if newpath: return newpath
    return None

def find_path(graph, start, distance, path=[]):
    path = path + [start]
    for i in range(3):
        new_part = find_path_one_direction(graph, start, i*90.0, distance/4)
        if new_part != None:
            path = path + new_part
            start = new_part[-1]
    rest_of_path = find_path_back(graph, path[-1], start)
    if rest_of_path != None:
        path = path + rest_of_path
    return path

neighboring_nodes = {}
nodes_by_id = []
id_to_node = {}
for way in result.ways:
    for node in way.nodes:
        nodes_by_id.append(node.id)
        id_to_node[node.id] = node

def merge_sort(array):
    length = len(array)
    if length > 1:
        mp = int(length / 2)
        left = merge_sort(array[:mp])
        right = merge_sort(array[mp:])
        left_len = len(left)
        right_len = len(right)
        i = 0
        j = 0
        k = 0
        while i < left_len and j < right_len:
            if left[i] < right[j]:
                array[k] = left[i]
                i += 1
            else:
                array[k] = right[j]
                j += 1
            k += 1

        while i < left_len:
            array[k] = left[i]
            i += 1
            k += 1

        while j < right_len:
            array[k] = right[j]
            j += 1
            k += 1

    return array

# i = 0
# for edge in all_edges:
#     print(edge.start, edge.end)
#     print(edge.get_bearing())
#     print()
#     i += 1
# print(i)

# print(find_path_one_direction(neighboring_nodes, my_node, 0, 4.0))

import networkx as nx
G = nx.Graph()
for vertex in intersections:
    G.add_node(vertex.id, coord=(vertex.lat, vertex.lon))
for path in edge_list:
    G.add_edge(path.start.id, path.end.id, weight=path.length)
#print(G.__getitem__(530968968))
cycle = nx.find_cycle(G, 530968968)
cycle_coords = []
for i in range(len(cycle)):
    cycle_coords.append((id_to_node[cycle[i][0]].lat, id_to_node[cycle[i][0]].lon))
    if cycle[i] == cycle[-1]:
        cycle_coords.append((id_to_node[cycle[i][1]].lat, id_to_node[cycle[i][1]].lon))
print(cycle_coords)

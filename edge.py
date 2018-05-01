'''
Software Design Final Project: Trail Blazer
'''

from geopy.distance import vincenty
from geographiclib.geodesic import Geodesic

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
        ''' Gets the direction of the edge, calculated from its start node to its end node '''
        bearing = Geodesic.WGS84.Inverse(self.start.lat, self.start.lon, self.end.lat, self.end.lon)['azi1']
        if bearing < 0.0:
            return bearing + 360.0
        else:
            return bearing

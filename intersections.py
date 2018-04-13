import overpy

import geopy
from geopy.distance import VincentyDistance, vincenty

def find_new_lat_lng_geopy(lat, lng, b, dist): #b in degrees (0 is north, 90 is east), dist=distance in kilometers
    origin = geopy.Point(lat, lng)
    destination = VincentyDistance(kilometers=dist).destination(origin, b)
    return (destination.latitude, destination.longitude)

def get_bounding_box(lat, lng, dist):
    bearing = 0
    bearing_increase = 360/4
    points_on_circumference = []
    for i in range(4):
        points_on_circumference.append(find_new_lat_lng_geopy(lat, lng, bearing, dist))
        bearing += bearing_increase
    return points_on_circumference

end_locations = get_bounding_box(42.29295,-71.26304, 3)

# point1 = 42.293015, -71.260973
# point2 = 42.292158, -71.260845
# print(vincenty((42.293015, -71.260973), (42.292158, -71.260845)).km)

# for coord in get_bounding_box
#print(get_bounding_box(42.29295,-71.26304, 3))
api = overpy.Overpass()



# fetch all ways and nodes
result = api.query("""
    way(42.288761, -71.244837, 42.291047, -71.241189) ["highway"];
    (._;>;);
    out body;
    """)

all_nodes = {}
intersections = []

for way in result.ways:
    #print("Name: %s" % way.tags.get("name", "n/a"))
    #print("  Highway: %s" % way.tags.get("highway", "n/a"))
    #print("  Nodes:")
    for node in way.nodes:
        all_nodes[node] = all_nodes.get(node, 0) + 1
        #if node.id == 68312720:
            #print(node)
        #    print("Name: %s" % way.tags.get("name", "n/a"))
        #    print("  Highway: %s" % way.tags.get("highway", "n/a"))
        #    print("    Lat: %f, Lon: %f" % (node.lat, node.lon))

for node in all_nodes:
    if all_nodes[node] > 1:
        intersections.append(node)
        #print("Lat: %f, Lon: %f" % (node.lat, node.lon))

# ways_and_intersections = {}
# for way in result.ways:
#     for node in way.nodes:
#         if node in intersections:
#         #for node in intersections:
#         #if node in way.nodes:
#             if way in ways_and_intersections:
#                 ways_and_intersections[way].append(node)
#             else:
#                 ways_and_intersections[way] = [node]

class Edge():

    def __init__(self):
        self.node_list = []
        self.length = 0

    def set_start_node(self, start_node):
        self.start = start_node

    def set_end_node(self, end_node):
        self.end = end_node

    def add_node(self, node):
        self.node_list.append(node)

    def update_distance(self):
        if len(self.node_list) > 0:
            first_coord = (self.start.lat, self.start.lon)
            last_coord = (self.end.lat, self.end.lon)
            self.length += vincenty((self.node_list[0].lat, self.node_list[0].lon), first_coord).km
            self.length += vincenty((self.node_list[-1].lat, self.node_list[-1].lon), last_coord).km
            for i in range(len(self.node_list) - 1):
                self.length += vincenty((self.node_list[i+1].lat, self.node_list[i+1].lon), (self.node_list[i].lat, self.node_list[i].lon)).km

# for node in all_nodes:
#     print(node.lat, node.lon)


#find edges
edge_list = []
# for i in range(10):
#     edge_list.append(Edge())
# print(edge_list)
for way in result.ways:
    new_edge = Edge()
    #print(way.nodes[0])
    #for i in range(way.nodes):
    #i = 0
    #while i < len(way.nodes):
    for node in way.nodes:
        #new_edge.set_start_node(node)
        length = 0
        if not hasattr(new_edge, 'start') and new_edge.node_list == []:
            new_edge.set_start_node(node)
        elif node not in intersections:
            new_edge.add_node(node)
        else:
            new_edge.set_end_node(node)
            new_edge.update_distance()
            edge_list.append(new_edge)
            new_edge = Edge()
            #new_edge.
            #new_edge.node_list == [] and
        # elif new_edge.node_list == [] and :
        #     new_edge.node_list.append(node)
        # else
    # if hasattr(new_edge, 'start'):
    # edge_list.append(new_edge)

# class Node():
#
#     def __init__(self):
#         self.neighbors = []
#
#     def add_neighbors(self, node, distance):
#         self.neighbors.append((node, distance))

# for edge in edge_list
# for edge in edge_list:
#     print(edge.start, edge.end, edge.length)
#print(edge_list)
#
#         if node in intersections:


# for way in ways_and_intersections:
#     for node in way.nodes:
#         if
#         print(node.lat)
    #waypoints = way.nodes


#print(ways_and_intersections)
# print(intersections[0], intersections[1])
# print(result.ways)

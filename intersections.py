import overpy

api = overpy.Overpass()

# fetch all ways and nodes
result = api.query("""
    way(42.270198, -71.279754, 42.301566, -71.224651) ["highway"];
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

    def set_start_node(self, start_node):
        self.start = start_node

    def set_end_node(self, end_node):
        self.end = end_node

    def add_node(self, node):
        self.node_list.append(node)

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
        if not hasattr(new_edge, 'start') and new_edge.node_list == []:
            new_edge.set_start_node(node)
        elif node not in intersections:
            new_edge.add_node(node)
        else:
            new_edge.set_end_node(node)
            edge_list.append(new_edge)
            new_edge = Edge()
            #new_edge.
            #new_edge.node_list == [] and
        # elif new_edge.node_list == [] and :
        #     new_edge.node_list.append(node)
        # else
    # if hasattr(new_edge, 'start'):
    # edge_list.append(new_edge)

for edge in edge_list:
    print(edge.end)
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

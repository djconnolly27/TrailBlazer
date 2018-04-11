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
        print("Lat: %f, Lon: %f" % (node.lat, node.lon))
print(intersections)

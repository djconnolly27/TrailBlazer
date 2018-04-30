'''
Software Design Final Project: Trail Blazer

'''
import overpy
from geopy.distance import vincenty
from edge import Edge

class Graph():

    def __init__(self, api, lat, lng, rad):
        self.api = api
        self.home_lat = lat
        self.home_lng = lng
        self.size = rad
        self.ways = []
        self.node_appearances = {}
        self.intersections = []
        self.edge_list = []
        self.neighboring_nodes = {}
        self.nodes_edges = {}
        self.plottable_cycle = []
        self.epsilon = 0.25

    def get_ways_in_area(self):
        ''' Gets all ways and nodes in a given area. '''
        lat1 = self.home_lat - self.size
        lng1 = self.home_lng - self.size
        lat2 = self.home_lat + self.size
        lng2 = self.home_lng + self.size
        query_str = """
            way({}, {}, {}, {}) ["highway"];
            (._;>;);
            out body;
            """.format(lat1, lng1, lat2, lng2)
        self.ways = self.api.query(query_str).ways

    def get_vertices(self):
        ''' Gets all of the valid nodes/points that are on roads or paths. '''
        self.node_appearances = {}
        for way in self.ways:
            for node in way.nodes:
                self.node_appearances[node] = self.node_appearances.get(node, 0) + 1
        self.node_appearances

    def get_intersections(self):
        ''' Creates a list of the points that are intersections. '''
        self.intersections = []
        for node in self.node_appearances:
            if self.node_appearances[node] > 1:
                self.intersections.append(node)
        self.intersections

    def find_nodes_and_edges(self):
        ''' Taking all of the paths/roads in the given area, this breaks up those paths/roads into edges and stores in a list.'''
        self.edge_list = []
        for way in self.ways:
            breakpoints = []
            for i in range(len(way.nodes)):
                if way.nodes[i] in self.intersections:
                    breakpoints.append(i)
            if breakpoints == []:
                new_edge = Edge()
                new_edge.set_start_node(way.nodes[0])
                new_edge.set_end_node(way.nodes[-1])
                if len(way.nodes) > 2:
                    new_edge.add_multiple_nodes(way.nodes[1:-1])
                new_edge.update_distance()
                self.edge_list.append(new_edge)
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
                    self.edge_list.append(new_edge)
        # return edge_list

    def get_neighboring_nodes(self):
        self.neighboring_nodes = {}
        for new_edge in self.edge_list:
            # The following section determines which nodes neighbor one another and how far each neighboring node is from the origin node.
            if new_edge.start in self.neighboring_nodes and new_edge.end in self.neighboring_nodes:
                self.neighboring_nodes[new_edge.start].append(new_edge.end)
                self.neighboring_nodes[new_edge.end].append(new_edge.start)
            elif new_edge.start in self.neighboring_nodes:
                self.neighboring_nodes[new_edge.start].append(new_edge.end)
                self.neighboring_nodes[new_edge.end] = [new_edge.start]
            elif new_edge.end in self.neighboring_nodes:
                self.neighboring_nodes[new_edge.end].append(new_edge.start)
                self.neighboring_nodes[new_edge.start] = [new_edge.end]
            else:
                self.neighboring_nodes[new_edge.start] = [new_edge.end]
                self.neighboring_nodes[new_edge.end] = [new_edge.start]
        # return self.neighboring_nodes
        # return neighboring_nodes

    def create_graph(self):
        self.nodes_edges = {}
        for edge in self.edge_list:
            ends = edge.start, edge.end
            self.nodes_edges[ends] = edge
            reverse_ends = edge.end, edge.start
            reverse_edge = Edge()
            reverse_edge.start = edge.end
            reverse_edge.end = edge.start
            reverse_edge.add_multiple_nodes(edge.node_list[::-1])
            reverse_edge.update_distance()
            self.nodes_edges[reverse_ends] = reverse_edge
        # return nodes_edges

    def find_cycle(self, path_length, visited):
        found = []
        if len(visited) < 25:
            for neighbor in self.neighboring_nodes[visited[len(visited) -1]]:
                # print(neighbor)
                # print(visited)
                if len(found) >= 1:
                    break
                else:
                    if neighbor == visited[0] and len(visited) != 2:
                        new_path_length = path_length - self.nodes_edges[(visited[len(visited) - 1], neighbor)].length
                        if abs(new_path_length) < self.epsilon: #epsilon = 0.25
                            found.append(list(visited + [neighbor]))
                            # print(found)
                    elif neighbor not in visited:
                        new_path_length = path_length - self.nodes_edges[(visited[len(visited) - 1], neighbor)].length
                        if new_path_length > 0.0:
                            found.extend(self.find_cycle(new_path_length, list(visited + [neighbor])))
        return found

    def find_edges_in_path(self, distance, start):
        self.get_ways_in_area()
        self.get_vertices()
        self.get_intersections()
        self.find_nodes_and_edges()
        self.get_neighboring_nodes()
        self.create_graph()
        for x in self.neighboring_nodes:
            if x.id == start.id:
                start_node = x
        potential_cycles = self.find_cycle(distance, [start_node])
        for i in range(len(potential_cycles[0]) - 1):
            potential_cycles[0][i] = (potential_cycles[0][i], potential_cycles[0][i+1])
        potential_cycles[0].remove(potential_cycles[0][-1])

        self.plottable_cycle = []
        for connection in potential_cycles[0]:
            edge = self.nodes_edges[connection[0], connection[1]]
            self.plottable_cycle.append(edge)
        self.plottable_cycle

    def show_route(self, start):
        import matplotlib.pyplot as plt
        import mplleaflet
        lats = []
        lons = []
        self.find_edges_in_path(1.1, start)
        for edge in self.plottable_cycle:
            lats.append(edge.start.lat)
            lons.append(edge.start.lon)
            for node in edge.node_list:
                lats.append(node.lat)
                lons.append(node.lon)
            lats.append(edge.end.lat)
            lons.append(edge.end.lon)

        plt.hold(True)
        plt.plot(start.lon, start.lat, 'ro')
        plt.plot(lons, lats, 'b')
        return mplleaflet.show()

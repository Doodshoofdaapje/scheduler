import sys

class GraphAlgorithms:

    @staticmethod
    def dijkstras_algorithm(graph):
        unvisted_vertices = graph.get_vertex_labels()
        start_vertex = graph.get_vertex("source").get_label()

        shortest_path = {}
        previous_nodes = {}

        max_value = sys.maxsize
        for vertex in unvisted_vertices:
            shortest_path[vertex] = max_value

        shortest_path[start_vertex] = 0

        # The algorithm executes until we visit all nodes
        while unvisted_vertices:

            current_vertex = unvisted_vertices[0]
            for vertex in unvisted_vertices:
                if shortest_path[vertex] < shortest_path[current_vertex]:
                    current_vertex = vertex

            # The code block below retrieves the current node's neighbors and updates their distances
            outgoing_edges = graph.get_reachable_edges(current_vertex)

            for edge in outgoing_edges:
                neighbour = edge.sink_vertex.get_label()
                tentative_value = shortest_path[current_vertex] + 1
                #print("tentative value to " + neighbour + " is " + str(tentative_value))
                if tentative_value < shortest_path[neighbour]:
                    shortest_path[neighbour] = tentative_value
                    previous_nodes[neighbour] = current_vertex

            # After visiting its neighbors, we mark the node as "visited"
            unvisted_vertices.remove(current_vertex)

        return previous_nodes, shortest_path

    @staticmethod
    def get_augmenting_path(graph, previous_vertices):
        path = []
        next_vertex = "sink"
        while next_vertex != "source":
            source = graph.get_vertex(previous_vertices[next_vertex])
            sink = graph.get_vertex(next_vertex)
            edge = graph.get_edge(source, sink)
            path.append(edge)
            next_vertex = previous_vertices[next_vertex]
        return path

    @staticmethod
    def ford_fulkerson(graph):
        while True:
            residual_network = graph.get_residual_network()
            
            previous_vertices, shortest_path = GraphAlgorithms.dijkstras_algorithm(residual_network)
            if "sink" not in previous_vertices:
                #print(" --------- FINAL GRAPH --------- ")
                #graph.print()
                break
            augmenting_path = GraphAlgorithms.get_augmenting_path(residual_network, previous_vertices)
            graph.increase_flow(augmenting_path)
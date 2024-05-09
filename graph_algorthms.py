import sys

class GraphAlgorithms:

    @staticmethod
    def dijkstras_algorithm(graph):
        """
        Applies Dijkstra's algorithm to find the shortest paths from the source vertex to all other vertices.

        Parameters
        ----------
        graph : FlowGraph
            The flow graph on which to apply Dijkstra's algorithm.

        Returns
        -------
        dict, dict
            Two dictionaries:
            - The first dictionary contains the previous node for each vertex in the shortest path.
            - The second dictionary contains the shortest distance from the source to each vertex.

        Notes
        -----
        This method finds the shortest paths from the source vertex to all other vertices in the graph
        using Dijkstra's algorithm. It iterates over each vertex in the graph, updating the shortest path
        to each vertex by considering its neighbors and their distances.
        """
        unvisted_vertices = graph.get_vertex_labels()
        start_vertex = graph.get_vertex("source").label

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
                neighbour = edge.sink_vertex.label
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
        """
        Converts the shortest path dictionary into a list representing the augmenting path.

        Parameters
        ----------
        graph : FlowGraph
            The flow graph.
        previous_vertices : dict
            Dictionary mapping vertices to their previous vertices in the shortest path.

        Returns
        -------
        list of Edge
            A list representing the augmenting path in the flow graph.

        Notes
        -----
        This method traverses the shortest path found by an algorithm (e.g., Dijkstra's algorithm) in the residual
        network of the graph and constructs the augmenting path represented as a list of edges.
        """
        path = []
        next_vertex = "sink"
        while next_vertex != "source":
            edge = graph.get_edge(previous_vertices[next_vertex], next_vertex)
            path.append(edge)
            next_vertex = previous_vertices[next_vertex]
        return path

    @staticmethod
    def ford_fulkerson(graph):
        """
        Applies the Ford-Fulkerson algorithm to find the maximum flow in the given graph.

        Parameters
        ----------
        graph : FlowGraph
            The flow graph on which to apply the algorithm.

        Notes
        -----
        This method iteratively computes augmenting paths in the residual network of the graph using Dijkstra's algorithm
        and increases the flow along these paths until no augmenting path exists. It terminates when no augmenting path
        is found in the residual network, indicating that the maximum flow has been reached.
        """
        while True:
            residual_network = graph.get_residual_network()
            
            previous_vertices, shortest_path = GraphAlgorithms.dijkstras_algorithm(residual_network)
            if "sink" not in previous_vertices:
                break
            augmenting_path = GraphAlgorithms.get_augmenting_path(residual_network, previous_vertices)
            graph.increase_flow(augmenting_path)
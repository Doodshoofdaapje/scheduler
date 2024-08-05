from edge import Edge
from vertex import Vertex

class FlowGraph:

    def __init__(self):
        # Vertices are stored in a dictionary, using their labels as the key
        self._vertices = {}
        # Edges are stored as an adjacency list, this reduces search spaces to |V| rather than |E|
        self._edges = {}

    def add_vertex(self, label):
        """
        Adds a vertex with the specified label to the graph.

        Parameters
        ----------
        label : str
        Label of the vertex to add.
        """
        vertex = Vertex(label)
        self._vertices[label] = vertex
        self._edges[label] = []

    def get_vertex(self, label):
        """
        Retrieves the vertex with the specified label, if it exists.

        Parameters
        ----------
        label : str
            Label of the vertex to retrieve.

        Returns
        -------
        Vertex or None
        The vertex with the specified label, if found; otherwise, returns None.
        """
        return self._vertices.get(label, None)
    
    def get_vertex_labels(self):
        """
        Retrieves the labels of all vertices in the graph.

        Returns
        -------
        list of str
            A list containing the labels of all vertices in the graph.
        """
        return list(self._vertices.keys())

    def add_edge(self, vertex_label1, vertex_label2, capacity, flow):
        """
        Adds an edge between the specified vertices with the given capacity and flow.

        Parameters
        ----------
        vertex_label1 : str
            Label of the first vertex of the edge.
        vertex_label2 : str
            Label of the second vertex of the edge.
        capacity : int
            Capacity of the edge.
        flow : int
            Flow through the edge.

        Returns
        -------
        bool
            True if the edge is successfully added, False otherwise.

        Notes
        -----
        This method adds an edge between the vertices with the specified labels to the flow graph.
        If either of the vertices does not exist in the graph, the edge is not added, and the method returns False.
        The flow through the edge is adjusted to be within the range [0, capacity].
        """
        v1 = self.get_vertex(vertex_label1)
        v2 = self.get_vertex(vertex_label2)

        if (v1 is None or v2 is None):
            return False

        flow = max(flow, 0)
        flow = min(flow, capacity)

        edge = Edge(v1, v2, capacity, flow)
        self._edges[v1.label].append(edge)
        return True
    
    def get_edge(self, vertex_label1, vertex_label2):
        """
        Retrieves the edge between the specified vertices, if it exists.

        Parameters
        ----------
        vertex_label1 : str
            Label of the first vertex of the edge.
        vertex_label2 : str
            Label of the second vertex of the edge.

        Returns
        -------
        Edge or None
            The edge between the specified vertices, if found; otherwise, returns None.
        """
        possible_edges = self.get_outgoing_edges(vertex_label1)
        edges = [edge for edge in possible_edges if edge.sink_vertex.label == vertex_label2]
        return next(iter(edges), None)
    
    def get_outgoing_edges(self, vertex_label):
        return self._edges[vertex_label]

    def get_reachable_edges(self, vertex_label):
        """
        Retrieves the non zero outgoing edges from the specified vertex.

        Parameters
        ----------
        vertex_label : str
            Label of the vertex for which outgoing edges are to be retrieved.

        Returns
        -------
        list of Edge
            A list of outgoing edges from the specified vertex, excluding edges with zero capacity.
        """
        outgoing_edges = [edge for edge in self.get_outgoing_edges(vertex_label) if edge.capacity != 0]
        return outgoing_edges

    def delete_edge(self, vertex_label1, vertex_label2):
        """
        Deletes the edge between the specified vertices.

        Parameters
        ----------
        vertex_label1 : str
            Label of the first vertex of the edge.
        vertex_label2 : str
            Label of the second vertex of the edge.

        Returns
        -------
        bool
            True if the edge is successfully deleted, False otherwise.
        """
        edge = self.get_edge(vertex_label1, vertex_label2)
        if edge is None:
            return False
        
        self._edges[vertex_label1].remove(edge)
        return True

    def is_max_flow(self):
        outgoing_edges = [edge for edge in self.get_reachable_edges("source")]
        completed_edges = [edge for edge in self.get_reachable_edges("source") if edge.flow == edge.capacity]
        return len(outgoing_edges) == len(completed_edges)

    def increase_flow(self, path):
        """
        Increases flow along the path by the bottleneck amount.

        Parameters
        ----------
        path : list of Edge
            The path along which to increase flow.

        Notes
        -----
        This method increases the flow along the given path by the amount of the bottleneck edge's capacity.
        It iterates through the edges in the path and increases the flow of each corresponding edge in the flow graph.
        If an edge in the residual graph is not found in the flow graph, it searches for its reverse edge and decreases
        its flow by the same amount.
        """
        bottleneck_edge = min(path, key=lambda x: x.capacity)
        for residual_edge in path:
            edge = self.get_edge(residual_edge.source_vertex.label, residual_edge.sink_vertex.label)
            if edge is not None:
                edge.increase_flow(bottleneck_edge.capacity)
            else:
                edge = self.get_edge(residual_edge.sink_vertex.label, residual_edge.source_vertex.label)
                edge.increase_flow(-abs(bottleneck_edge.capacity))

    def get_residual_network(self):
        """
        Computes the residual graph.

        Returns
        -------
        FlowGraph
            The computed residual graph.

        Notes
        -----
        This function computes the residual graph based on the current flow graph. 
        It calculates the residual capacity of each edge and constructs the residual graph accordingly.
        """
        residual_graph = FlowGraph()
        for vertex in self.get_vertex_labels():
            residual_graph.add_vertex(vertex)

        print(self._edges)

        # We need to iterate over every edge in the graph
        for vertex, edges in self._edges.items():
            for edge in edges:
                source = edge.source_vertex
                sink = edge.sink_vertex
                residual_graph.add_edge(source.label, sink.label, edge.capacity - edge.flow, 0)
                residual_graph.add_edge(sink.label, source.label, edge.flow, 0)

        return residual_graph
    
    def print(self):
        for edge in self.get_edges():
            edge.print()
        return
from edge import Edge

class Graph:

    def __init__(self, vertices, edges):
        self.vertices = vertices
        self.connections = {}

        for vertex in self.vertices:
            self.connections[vertex.get_label()] = []

        for edge in edges:
            self.connections[edge.source_vertex.get_label()].append(edge)
    
    # Gets edge if it exists
    def get_edge(self, source, sink):
        for edge in self.get_reachable_edges(source.get_label()):
            if edge.sink_vertex.get_label() == sink.get_label():
                return edge
        return None

    def get_edges(self):
        edges = []
        for connection in self.connections.values():
            edges += connection
        return edges

    def add_edge(self, source, sink, capacity, flow):
        v1 = self.get_vertex(source)
        v2 = self.get_vertex(sink)
        edge = Edge(v1, v2, capacity, flow)
        self.connections[source].append(edge)

    def remove_edge(self, edge):
        self.connections[edge.source_vertex.get_label()].remove(edge)

    # Gets vertex if it exists
    def get_vertex(self, label):
        for vertex in self.vertices:
            if vertex.get_label() == label:
                return vertex
        return None

    def get_vertex_labels(self):
        labels = [vertex.get_label() for vertex in self.vertices]
        return labels

    # Gets the all outgoing edges from a vertex
    def get_reachable_edges(self, label):
        outgoing_edges = [edge for edge in self.connections[label] if edge.capacity != 0]
        return outgoing_edges

    def get_outgoing_edges(self, label):
        return self.connections[label]

    # Increases flow along a path
    def increase_flow(self, path):
        bottleneck_edge = min(path, key=lambda x: x.capacity)
        for residual_edge in path:
            edge = self.get_edge(residual_edge.source_vertex, residual_edge.sink_vertex)
            if edge is not None:
                edge.increase_flow(bottleneck_edge.capacity)
            else:
                edge = self.get_edge(residual_edge.sink_vertex, residual_edge.source_vertex)
                edge.increase_flow(-abs(bottleneck_edge.capacity))
        return

    # computes the residual flow network of the graph.
    def get_residual_network(self):
        residual_vertices = self.vertices
        residual_edges = []

        for edge in self.get_edges():
            source = edge.source_vertex
            sink = edge.sink_vertex
            residual_edges.append(Edge(source, sink, edge.capacity - edge.flow, 0))
            residual_edges.append(Edge(sink, source, edge.flow, 0))

        return Graph(residual_vertices, residual_edges)
    
    def print(self):
        for edge in self.get_edges():
            edge.print()
        return
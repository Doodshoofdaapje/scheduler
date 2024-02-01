from edge import Edge

class Graph:

    def __init__(self, vertices, edges):
        self.vertices = vertices
        self.edges = edges
    
    # computes the residual flow network of the graph.
    def get_residual_network(self):
        residual_vertices = self.vertices
        residual_edges = []

        for edge in self.edges:
            vertex1 = edge.vertex1
            vertex2 = edge.vertex2
            residual_edges.append(Edge(vertex1, vertex2, edge.capacity - edge.flow, 0))
            residual_edges.append(Edge(vertex2, vertex1, edge.flow, 0))

        return
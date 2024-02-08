class Edge:

    def __init__(self, v1, v2, c, f):
        self.source_vertex = v1
        self.sink_vertex = v2
        self.capacity = c
        self.flow = f

    def increase_flow(self, amount):
        self.flow += amount
        self.flow = max(self.flow, 0)
        self.flow = min(self.flow, self.capacity)

    def print(self):
        print("edge from " + self.source_vertex.label + " to " + self.sink_vertex.label + " with capacity " + str(self.capacity) + " and flow " + str(self.flow))
class Edge:

    def __init__(self, v1, v2, c, f):
        self.vertex1 = v1
        self.vertex2 = v2
        self.capacity = c
        self.flow = f

    def increase_flow(self, amount):
        self.flow += amount
        self.flow = max(self.flow, 0)
        self.flow = min(self.flow, self.capacity)
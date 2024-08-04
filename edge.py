class Edge:

    def __init__(self, v1, v2, c, f):
        self._source_vertex = v1
        self._sink_vertex = v2
        self._capacity = c
        self._flow = f

    @property
    def source_vertex(self):
        return self._source_vertex
    
    @property
    def sink_vertex(self):
        return self._sink_vertex
    
    @property
    def capacity(self):
        return self._capacity
    
    @property
    def flow(self):
        return self._flow

    def increase_flow(self, amount):
        self._flow += amount
        self._flow = max(self._flow, 0)
        self._flow = min(self._flow, self._capacity)

    def print(self):
        print("edge from " + self._source_vertex.label + " to " + self._sink_vertex.label + " with capacity " + str(self._capacity) + " and flow " + str(self._flow))
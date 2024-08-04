class Vertex:
       
    def __init__(self, label):
        self._label = label
    
    @property
    def label(self):
        return self._label
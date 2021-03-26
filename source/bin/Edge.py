
class Edge(object):
    def __init__(self, connectors, **kwargs):
        self.name = kwargs.get("name", "E")
        #+-1 is connectors[0] --(+-)--> connectors[1]
        self.dir = kwargs.get("dir", 0)
        #edge or spring
        self.type = kwargs.get("type", "")
        #connectors is a duple of IDs of vertices to which the edge is Connected
        #(12,-1) means edge is connected to vertex 12 and stray on other end
        self.conns = connectors


#an edge equivalent in an IllustratedGraph object
class Spring(Edge):
    def __init__(self, connectors, **kwargs):
        self.name = kwargs.get("name", "H")
        self.dir = kwargs.get("dir", 0)
        self.conns = connectors

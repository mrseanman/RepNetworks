class Vertex(object):
    def __init__(self, **kwargs):
        self.name = str(kwargs.get("name", ""))
        #either "hinge" or "vert"
        self.type = kwargs.get("type", "")
        self.connVerts = kwargs.get("connectedVerts", [])

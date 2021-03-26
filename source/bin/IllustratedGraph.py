from BirdGraph import BirdGraph
import copy
class IllustratedGraph(BirdGraph):
    def __init__(self, birdgraph):
        #must be /geq 2
        self.edgeSplit = 3
        self = copy.deepcopy(BirdGraph)
        self.og = copy.deepcopy(BirdGraph)

    def makeIllusGraph():
        #points
        self.p = []
        for i, v in enumerate(self.ogGraph.v):
            self.p.append(Point("vert", ogGraph.connectedVerts(i), name=v.name))



    #makes an edge split in to self.edgeSplit parts with hinges in the middle
    def makeSplitEdge(self, eID):
        startingVert, endingVert = self.e[eID].conns
        newVerts = dict()
        newEdges = {0:Edge([-1,0], type="spring")}
        for i in range(self.edgeSplit-2):
            newVerts.update({i:Vertex(type="hinge")})
            #if the spring is in the middle it will be labelled differently
            if i+2==(self.edgeSplit+1.)/2.:
                type = "centralSpring"
            else:
                type = "spring"
            newEdges.update({i+1:Edge([i,i+1], type=type)})
        newVerts.update({self.edgeSplit-2:Vertex(type="hinge")})
        newEdges.update({self.edgeSplit-1:Edge([1,-1], type="spring")})

        splitEdge = BirdGraph(verts=newVerts, edges=newEdges, name=self.e[eID].name)
        splitEdge.report()

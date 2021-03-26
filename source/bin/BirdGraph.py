
from Vertex import Vertex
from Edge import Edge
import copy

class BirdGraph(object):
    def __init__(self, **kwargs):
        self.name = kwargs.get("name", "")
        if "verts" in kwargs.keys():
            self.v = kwargs["verts"]
        if "edges" in kwargs.keys():
            self.e = kwargs["edges"]

        graphFile = kwargs.get("graphFile", None)
        if graphFile:
            self.form(graphFile)


    def report(self):
        print("###############--- " + self.name + " ---###############")
        print("~~~~Connected verts~~~~")
        for pair in self.pairsOfConnVerts():
            v1, v2 = pair
            print("\t" + str(v1) + "______" + str(v2) +
                "\t via edges: " + str(self.edgesConnectingVerts(v1,v2)))
        print("\n~~~~Vertex Detail~~~~")
        for vID, v in self.v.items():
            print("" + str(vID) + ":  connected to these verts:\t"
                + str(self.vConnectedVerts(vID)))
            print("and these edges:\t\t" + str(self.connectedEdges(vID)))
            print("---------")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")


    #------------Graph Forming --------------------
    def form(self, graphFile):
        if graphFile=="demo1":
            self.formDemo1()
        if graphFile=="TDemo2":
            self.formTDemo2()

    def formDemo1(self):
        #form verteces
        self.v = dict()
        for i in range(3):
            self.addVertex(Vertex(name = str(i)))

        #form edges
        self.e = dict()
        self.addEdge(Edge([0,1], name="E1"))
        self.addEdge(Edge([1,2], name="E2"))
        self.addEdge(Edge([2,-1], name="E3"))
        self.addEdge(Edge([2,-1], name="E4"))


    def formTDemo2(self):
        #form verts
        self.v = dict()
        for i in range(2):
            self.addVertex(Vertex(name="T points"))

        #form edges
        self.e = dict()
        self.addEdge(Edge([0,-1]))
        self.addEdge(Edge([0,-1]))
        self.addEdge(Edge([0,1]))

    def addVertex(self, v):
        if not(self.v):
            self.v[0]=v
        else:
            self.v[max(self.v.keys())+1] = v

    def addEdge(self, e):
        if not(self.e):
            self.e[0]=e
        else:
            self.e[max(self.e.keys())+1] = e

    #------------------------------------------------
    #re-map the IDs
    def mapVerts(self, func):
        freshVerts = dict()
        for vID, v in self.v.items():
            freshVerts.update({func(vID): v})
        self.v = freshVerts

        for vID, v in self.v.items():
            v.connVerts = map(func, v.connVerts)

        for eID, e in self.e.items():
            if e.conns[0] >= 0:
                e.conns[0] = func(e.conns[0])
            if e.conns[1] >= 0:
                e.conns[1] = func(e.conns[1])

    def mapEdges(self, func):
        freshEdges = dict()
        for eID, e in self.e.items():
            freshEdges.update({func(eID): e})
        self.e = freshEdges

    #-------- Important Algorithms ------------------
    #takes vertexID, returns IDs of connected edges
    def connectedEdges(self, v):
        connectedEdges = []
        for eID, e in self.e.items():
            if v in e.conns:
                connectedEdges.append(eID)
        return connectedEdges

    #takes vertexID, returns IDs of connected verts
    def vConnectedVerts(self,v):
        vConnectedVerts = set()
        connectedEdgeIndexes = self.connectedEdges(v)
        connectedEdges = [self.e[i] for i in connectedEdgeIndexes]

        for e in connectedEdges:
            #value of vertID which isnt equal to v
            otherVert = e.conns[int(not(e.conns.index(v)))]
            vConnectedVerts.add(otherVert)
        return list(vConnectedVerts)


    #returns list of sets of pairs of connected vert's IDs
    def pairsOfConnVerts(self):
        connVerts = []
        #vi = vert index
        for vID in self.v.keys():
            for connectedVID in self.vConnectedVerts(vID):
                if not( {vID, connectedVID} in connVerts):
                    connVerts.append({vID,connectedVID})
        return list(connVerts)

    #returns list of edges that connect v1 and v2
    def edgesConnectingVerts(self, v1, v2):
        connectingEdges = []
        for eID, e in self.e.items():
            #print(e.conns)
            if (v1 in e.conns) and (v2 in e.conns):
                connectingEdges.append(eID)
        return connectingEdges

    #returns a BirdGraphObject where subgraph has been replaced
    #map defines a stitching from old vertices to new
    #in the form of a dictionary
    #removeGraph is just a list of edgeIds and vertexIds to be deleted
    def replaceSubGraph(self, fReplaceGraph, **kwargs):
        vMap = kwargs.get("vMap", dict())
        eMap = kwargs.get("eMap", dict())
        removeV = kwargs.get("removeV", [])
        removeE = kwargs.get("removeE", [])
        replaceGraph = copy.deepcopy(fReplaceGraph)

        maxV = max(self.v.keys())
        maxE = max(self.e.keys())
        #make sure theres no ID clashes
        replaceGraph.mapVerts(lambda x: x+maxV+1)
        replaceGraph.mapEdges(lambda x: x+maxE+1)

        currGraphCopy = copy.deepcopy(self)

        #add the new graph to the existing
        currGraphCopy.v.update(replaceGraph.v)
        currGraphCopy.e.update(replaceGraph.e)

        #stitching
        for oldV, newV in vMap.items():
            #when stitching in a vertex we must connect the new vertex
            #to all the edges the old vertex was attached to

            #since we did this above
            newV += maxV + 1
            for e in currGraphCopy.connectedEdges(oldV):
                connectedEnd = e.conns.index(oldV)
                e.conns[connectedEnd] = newV

        for oldEdgeDetail, newEdgeDetail in eMap.items():
            #when stitching an edge we must define a map between edge ends.
            #eMap looks like {(12,0):(13,1) ... } meaning end 0 of edge 12 maps
            #to end 1 of edge 13
            oldEdge, oldEdgeEnd = oldEdgeDetail
            newEdge, newEdgeEnd = newEdgeDetail
            #since we did this above
            newEdge += maxE + 1
            currGraphCopy.e[newEdge].conns[newEdgeEnd] = currGraphCopy.e[oldEdge].conns[oldEdgeEnd]

        #remove the old graph
        for eID in removeE:
            del currGraphCopy.e[eID]
        for vID in removeV:
            del currGraphCopy.v[vID]

        return currGraphCopy

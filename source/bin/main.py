from BirdGraph import BirdGraph
from IllustratedGraph import IllustratedGraph

def main():
    G = BirdGraph(graphFile = "demo1", name="G")
    G.report()

    T = BirdGraph(graphFile = "TDemo2", name="T")
    T.report()
    eMap = {(0,0):(0,1), (0,1):(1,1)}
    G = G.replaceSubGraph(T, eMap=eMap, removeE=[0])

    G.report()
    GIllus = IllustratedGraph(G)
    GIllus.makeSplitEdge(0)

main()

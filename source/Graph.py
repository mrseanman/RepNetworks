import networkx as nx
from Tableau import Tableau
from Diagram import Diagram
import copy
import json
import sympy as sym
import matplotlib.pyplot as plt

class Graph(object):
    def __init__():
        print("yo")

    @staticmethod
    def makeEdgeLabels(graph):
        labels = {}
        for data in graph.edges.data('dia'):
            labels[(data[0], data[1])] = data[2].printStr()
        return labels

    @staticmethod
    def makeCompletenessSubgraph(e1, e2, sumTermDia):
        #e1, e2 are just dictionaries corr to the old edges

        G = nx.MultiDiGraph()
        G.add_nodes_from([1,2])
        G.add_edge(1,2,
            prt0 = 0,
            prt1 = 0,
            dia = copy.deepcopy(sumTermDia),
            typ = 'internal'
            )
        return G

    @staticmethod
    def completenessTerm(graph, eId1, eId2, sumTermDia):
        oldGraph = copy.deepcopy(graph)

        e1 = graph.edges[eId1]
        e2 = graph.edges[eId2]
        subgraph = Graph.makeCompletenessSubgraph(e1, e2, sumTermDia)

        joinGraph  = nx.algorithms.operators.binary.union(
            oldGraph, subgraph, rename=('A', 'B')
            )
        #oldgraph nodes become 'A-_____' etc

        Graph.drawGraph(joinGraph)
        edgesToRemove = [('A'+str(eId1[0]), 'A'+str(eId1[1]), str(eId1[2])),
                        ('A'+str(eId2[0]), 'A'+str(eId2[1]), str(eId2[2]))]
        for edgeId in edgesToRemove:
            print(joinGraph.edges)
            n0, n1, key = edgeId
            joinGraph.remove_edge(n0, n1, key=int(key))

        #new edges
        #----left---------
        joinGraph.add_edge('A'+str(eId1[0]), 'B1',
            prt0 = e1['prt0'],
            prt1 = 1,
            dia = copy.deepcopy(e1['dia']),
            typ = e1['typ'])

        joinGraph.add_edge('A'+str(eId2[0]), 'B1',
            prt0 = e2['prt0'],
            prt1 = 2,
            dia = copy.deepcopy(e2['dia']),
            typ = e2['typ'])

        #---right---------------
        joinGraph.add_edge('B2', 'A'+str(eId1[1]),
            prt0 = 1,
            prt1 = e1['prt1'],
            dia = copy.deepcopy(e1['dia']),
            typ = e1['typ'])

        joinGraph.add_edge('B2', 'A'+str(eId2[1]),
            prt0 = 2,
            prt1 = e2['prt1'],
            dia = copy.deepcopy(e2['dia']),
            typ = e2['typ'])

        joinGraph = nx.relabel.convert_node_labels_to_integers(joinGraph)
        return joinGraph

    @staticmethod
    def drawGraph_spectral(graph):
        nx.draw_spectral(graph)
        nx.draw_networkx_edge_labels(graph, pos=nx.spectral_layout(graph),
         edge_labels = Graph.makeEdgeLabels(graph), horizontalalignment='left')
        nx.draw_networkx_labels(graph, pos=nx.spectral_layout(graph))
        plt.show()

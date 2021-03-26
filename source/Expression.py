import networkx as nx
from Tableau import Tableau
from Diagram import Diagram
from Graph import Graph

import copy
import json
import sympy as sym
import matplotlib.pyplot as plt

class Expression(object):

    def __init__(self, terms):
        self.terms = terms

    @staticmethod
    def load(file):
        with open(file,'r') as f:
            data = f.read()

        terms = []
        obj = json.loads(data)
        for term in obj["terms"]:
            newGraph = nx.MultiDiGraph()
            newCoeff = sym.sympify(term["coef"])

            for v in term["graph"]["verts"]:
                id = v["idx"]
                newGraph.add_node(id,
                    tbl = Tableau(v["tbl"]),
                    ort = v["ort"]
                    )

            for e in term["graph"]["edges"]:
                c0, c1 = e["con"]
                newGraph.add_edge(c0, c1,
                    prt0 = e["prt0"],
                    prt1 = e["prt1"],
                    dia = Diagram(e["dia"]),
                    typ = "internal"
                    )

            for e in term["graph"]["strayEdges"]:
                c0,c1 = e["con"]
                #which end isn't stray
                connectedEnd = [i for i in e["con"] if i>0][0]
                prt0 = e["prt"] * (connectedEnd==0) + -1* (connectedEnd!=0)
                prt1 = e["prt"] * (connectedEnd==1) + -1* (connectedEnd!=1)


                newGraph.add_edge(c0,c1,
                    prt0=prt0,
                    prt1=prt1,
                    dia = Diagram(e["dia"]),
                    typ = "stray"
                    )

            newTerm = {"coeff": copy.deepcopy(newCoeff),
                            "graph": copy.deepcopy(newGraph)}
            terms.append(newTerm)
        return Expression(terms)

    def completeness(self, term, eId1, eId2):
        oldGraph = self.terms[term]["graph"]
        newGraph = copy.deepcopy(oldGraph)

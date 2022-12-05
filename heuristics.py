import networkx as nx
from matplotlib import pyplot as plt
import random


def MaximalLeafyForest(g):
    F = nx.Graph()
    # F.add_nodes_from(list(range(0, g.number_of_nodes())))
    S = [None]*g.number_of_nodes()
    d = [None]*g.number_of_nodes()
    for v in g:
        S[v] = {v}
        d[v] = 0
    for v in g:
        P = []
        Q = 0
        for u in g.adj[v]:
            if ((not (u in S[v])) and (not (S[u] in P))):
                Q = Q+1
                P.append((S[u]))
        if (d[v]+Q >= 3):
            for i in P:
                if (g.has_edge(list(i)[0], v)):
                    F.add_edge(list(i)[0], v)
                    S[v] = S[v].union(S[list(i)[0]])
                    S[list(i)[0]] = S[list(i)[0]].union((S[v]))
                    d[list(i)[0]] += 1
                    d[v] += 1
    return F


# g = nx.Graph()
# g.add_nodes_from(list(range(0, 14)))
# g.add_edge(0, 1)
# g.add_edge(0, 2)
# g.add_edge(0, 3)
# g.add_edge(1, 4)
# g.add_edge(4, 5)
# g.add_edge(4, 6)
# g.add_edge(0, 4)
# g.add_edge(5, 6)
# g.add_edge(1, 12)
# g.add_edge(2, 3)
# g.add_edge(3, 11)
# g.add_edge(7, 8)
# g.add_edge(7, 9)
# g.add_edge(7, 10)
# g.add_edge(7, 11)
# g.add_edge(8, 11)
# g.add_edge(10, 13)
# g.add_edge(11, 12)
# g.add_edge(11, 13)
# print(g)
# # print(list(g.nodes))
# # print(list(g.edges))
# F = MaximalLeafyForest(g)
# print(F)
# print(list(F.nodes))
# print(list(F.edges))

def MaximumLeafSpanningTree(g):
    F = MaximalLeafyForest(g)

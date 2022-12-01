from helper import *
import pysat
from pysat.examples.rc2 import RC2
from pysat.formula import WCNF


def get_sat(g):
    l = []
    for lst in g:
        l.append([-(x + 1) for x in lst])
    # print(l)
    return l


def get_wcnf(g):
    s = get_sat(g)
    # These are required
    hard = pysat.formula.CNF(from_clauses=s)
    # We want to maximize the number of true variables
    soft = pysat.formula.CNF(from_clauses=[[x] for x in range(1, size + 1)])
    wcnf = WCNF()
    # print(hard.clauses)
    # print(soft.clauses)
    for clause in hard.clauses:
        wcnf.append(clause)
    for clause in soft.clauses:
        wcnf.append(clause, weight=1)

    return wcnf


def output(wcnf):
    out = 0
    with RC2(wcnf) as rc2:
        out = rc2.compute()
        print("computed in", rc2.oracle_time(), end=" seconds, output = ")
    return sum(x > 0 for x in out)


size = 100
p = 0.1
m = 300

total = []
n = 100
for i in range(n):
    # g = networkx_to_adj(random_graph_prob_edges(size, p))
    g = networkx_to_adj(random_graph_num_edges(size, m))

    # print(g)
    wcnf = get_wcnf(g)
    total.append(output(wcnf))
    print(total[-1])

print(sum(total) / (i + 1))

from helper import *
import itertools
from pysat.formula import CNF, WCNF
from pysat.examples.rc2 import RC2Stratified

"""from pysat.examples.rc2 import RC2
from pysat.formula import CNF, WCNF"""


def is_two_disjoint_sets(G):
    # Find the connected components
    components = list(nx.connected_components(G))

    # Check if the graph has exactly two components, each of size 1
    return len(components) == 2 and all(len(component) > 1 for component in components)


def get_length_n_cuts(g, n, all=0):
    print("here", n, all)
    cuts = set()

    g = adj_to_networkx(g)
    for cut_size in range(1, n + 1):
        possible_cuts = []
        if all:
            possible_cuts = list(itertools.combinations(g.edges(), cut_size))
        else:
            for node in g:
                if g.degree(node) > cut_size:
                    for cut in itertools.combinations(g.neighbors(node), cut_size):
                        possible_cut = []
                        for cut_node in cut:
                            possible_cut.append((node, cut_node))
                        possible_cuts.append(possible_cut)
        for possible_cut in possible_cuts:
            possible_cut_sorted = set(
                tuple(sorted(cut_edge)) for cut_edge in possible_cut
            )

            # This has already been dealt with
            if any(set(cut).issubset(possible_cut_sorted) for cut in cuts):
                continue

            for node1, node2 in possible_cut_sorted:
                g.remove_edge(node1, node2)
            if is_two_disjoint_sets(g):
                cuts.add(tuple(possible_cut_sorted))
            for node1, node2 in possible_cut_sorted:
                g.add_edge(node1, node2)
    # print("length_n_cuts: ", cuts)
    return cuts


def get_cnf(dnf, nextNum):
    clauses = []
    pks = []
    for c1, c2 in dnf:
        c1, c2 = c1 + 1, c2 + 1
        pk = nextNum
        nextNum += 1
        c1, c2 = -(c1), -(c2)
        clauses.append([pk, -c1, -c2])
        clauses.append([-pk, c1])
        clauses.append([-pk, c2])
        pks.append(pk)
    clauses.append(pks)
    # print("cnf: ", clauses)
    return clauses, nextNum


def get_sat(g, mod=0, dist=0):
    l = []
    for lst in g:
        l.append([-(x + 1) for x in lst])
    # l.append([-1])
    # Find any nodes that are necessary for the connectivity of the graph
    g_nx = adj_to_networkx(g)
    if dist:
        for thisDist in range(2, dist + 1):
            shortest_paths = dict(nx.all_pairs_shortest_path_length(g_nx))
            for node1 in g_nx.nodes():
                # Get all node2 that are exactly dist away from node1
                l.append(
                    [
                        -(node + 1)
                        for node in g_nx
                        if shortest_paths[node1][node] == thisDist
                    ]
                )
                if not l[-1]:
                    # print("ERROR: ", node1, thisDist)
                    l.pop()

    for node in g_nx.nodes():
        g_prime = g_nx.copy()
        g_prime.remove_node(node)
        if not nx.is_connected(g_prime):
            l.append([-(node + 1)])
            # print(" ", node, "is necessary for connectivity")

    if mod:
        nextNum = len(g) + 1
        cuts = get_length_n_cuts(g, mod, 1)
        for cut in cuts:
            cnf, nextNum = get_cnf(cut, nextNum)
            l.extend(cnf)
    return l


def get_wcnf(g, mod=0):
    # Determine the required clauses
    required = get_sat(g, mod)
    # These are required
    hard = CNF(from_clauses=required)
    # We want to maximize the number of true variables
    size = len(g)
    soft = CNF(from_clauses=[[x] for x in range(1, size + 1)])

    wcnf = WCNF()
    for clause in hard.clauses:
        wcnf.append(clause)
    for clause in soft.clauses:
        wcnf.append(clause, weight=1)

    return wcnf


def tseitin_transform(dnf, nextNum):
    dnf = [[-(x + 1) for x in clause] for clause in dnf]
    clauses = []
    new = []
    for clause in dnf:
        clauses.append([nextNum] + [-x for x in clause])
        for var in clause:
            clauses.append([-nextNum, var])
        new.append(nextNum)
        nextNum += 1
    clauses.append(new)
    return clauses, nextNum


def output(wcnf, g, n):
    g = adj_to_networkx(g)
    out = 0
    outputs = []
    c = 0
    k = 0
    best = 0
    nextNum = len(g) + 1
    with RC2Stratified(wcnf, solver="g4") as rc2:
        for out in rc2.enumerate():
            out = list(out)
            # print(out)
            inner = [-x - 1 for x in out if -len(g) - 1 < x < 0]
            # print(inner)
            sol = get_sol_from_inner_vertices(g, inner)
            comp = list(nx.connected_components(sol))
            num_connected = len(comp)

            # if nx.is_connected(g.subgraph(inner)):
            # if is_spanning_tree(g, sol):
            if num_connected == 1:
                # print("SOLVED: ", inner, g.edges())
                # print(num_leaves(sol), len(inncocer))
                # print(len(g)-len(inner))
                outputs.append(get_sol_from_inner_vertices(g, inner))
                k += 1
                if k == n:
                    return outputs
            else:
                # Attempt at adding all the paths between the components
                # for i in range(num_connected - 1):
                #     # Choose random node from each component
                #     node1 = random.choice(list(comp[i]))
                #     node2 = random.choice(list(comp[i + 1]))

                #     # Get all paths between the two nodes
                #     paths = list(nx.all_simple_paths(g, node1, node2))
                #     print(paths)
                #     paths = [path[1:-1] for path in paths if len(path) > 2]
                #     print(paths)

                #     clauses, nextNum = tseitin_transform(paths, nextNum)
                #     for clause in clauses:
                #         rc2.add_clause(clause)
                #     print(clauses, nextNum)

                if (c % 1000) == 0:
                    print(
                        f"{c} iterations on graph with {len(g)} nodes and {len(g.edges())} edges"
                    )
                c += 1
                # pass
                if c > 1e11:
                    if k == 0:
                        return False
                    else:
                        # Pad output with last solution
                        # while k < n:
                        #     sol = outputs[-1]
                        #     outputs.append(sol)
                        #     k += 1
                        return outputs
    # print(c)
    return outputs


def get_first_solution(g):

    g = networkx_to_adj(g)
    wcnf = get_wcnf(g, 1)
    # print(wcnf.hard)
    with RC2Stratified(wcnf, solver="g4") as rc2:
        print("computing")
        out = rc2.compute()
        if not out:
            visualize_graph(g)
        print(out)
        inner = [-x - 1 for x in out if -len(g) - 1 < x < 0]
        sol = get_sol_from_inner_vertices(g, inner)
        return sol


def sat_solve(g, mod=0, n=1):
    g = networkx_to_adj(g)
    wcnf = get_wcnf(g, mod)
    # print(wcnf.hard)
    sol = output(wcnf, g, n)

    if n == 1 and sol:
        sol = sol[0]
        print(sol.edges())
        return sol
    return sol


import time

if __name__ == "__main__":

    # for i in range(1):
    #     al = [[1, 5], [0, 2], [1, 3], [2, 4], [3, 5], [4, 0]]
    #     g = adj_to_networkx(al)
    #     # get_length_n_cuts(g, 2)
    #     # get_length_n_cuts(g, 2, all=True)
    #     sat_solve(g)
    #     visualize_graph(g)
    #     sat_solve(g, 2)
    #     print()
    # err

    n = 50
    p = 0.1
    m = 120

    k = 100000
    total = []

    for _ in range(k):
        start1 = time.time_ns()
        g = random_graph_num_edges(n, m)
        # print(networkx_to_adj(g))
        # print(g)
        # print(min([g.degree(x) for x in g]))
        # print("basic solve")
        s = sat_solve(g)
        # end1 = time.time_ns()
        # start2 = time.time_ns()
        # # print("cut solve")
        # s2 = sat_solve(g, 2)
        # end2 = time.time_ns()
        # print(
        #     "Time difference: ",
        #     (end1 - start1) / 1000000000,
        #     (end2 - start2) / 1000000000,
        #     (end2 - start2) / (end1 - start1),
        # )
        # if num_leaves(s) != num_leaves(s2):
        #     print("Error")
        if _ % 100 == 0:
            print(_)

    # print((time.time_ns() - start) / k / 1e9)
    # print(sum(total) / (k))

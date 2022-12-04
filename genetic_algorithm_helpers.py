from helper import *
from heuristics import *


def combine1(g, trees, M=4, sigma=1, omega=0.25):
    """
    Trying to implement combination from
    https://www.sciencedirect.com/science/article/pii/S0377221713006103

    May be incorrect
    """
    # initialize weighted graph
    G = nx.Graph()

    for u in range(len(g)):
        for v in g[u]:
            G.add_edge(u, v, weight=1)

    # for v in G:
    #     print(v)

    for tree in trees:
        for edge in tree.edges:
            # Decrease the weight of the edge in g by sigma
            G[edge[0]][edge[1]]["weight"] -= sigma

            # Decrease the weight of all other edges in g by omega
            for u in range(len(G)):
                for v in G[u]:
                    if u != edge[0] and v != edge[1]:
                        G[u][v]["weight"] -= omega

    # Create a forest by removing all edges adjacent to vertices of degree at least 3
    forest = G.copy()
    removed = set()

    for u in range(len(G)):
        if len(G[u]) >= 3:
            for v in G[u]:
                if (u, v) not in removed and (v, u) not in removed:
                    forest.remove_edge(u, v)
                    removed.add((u, v))

    for u in range(len(G)):
        for v in G[u]:
            # DFS to find the length of the chain
            length = 0
            visited = set()
            stack = [v, u]
            while stack:
                w = stack.pop()
                if w not in visited:
                    visited.add(w)
                    length += 1
                    for x in forest[w]:
                        stack.append(x)

            G[u][v]["weight"] -= M * length

    for edge in forest.edges:
        # Increase the weight of all edges not in g by 2*omega
        for u in range(len(G)):
            for v in G[u]:
                if u != edge[0] and v != edge[1]:
                    G[u][v]["weight"] += 2 * omega

    # Get MST of g
    mst = nx.minimum_spanning_tree(G)

    g_new = nx.Graph()

    for edge in mst.edges:
        g_new.add_edge(edge[0], edge[1])

    return g_new


def get_graph(tree, i, j):
    # Get graph of shortest path between i and j
    path = nx.shortest_path(tree, i, j)
    path_graph = nx.Graph()
    path_graph.add_nodes_from(path)
    for k in range(len(path) - 1):
        path_graph.add_edge(path[k], path[k + 1])

    return path_graph


def generate_child(g, path_tree, spanning_tree):
    # Get set of vertices in the path
    pv = set(path_tree.nodes())

    # print(spanning_tree, path_tree, g)
    flag = True
    while flag:
        flag = False
        v_prime = set(g.nodes()) - pv
        removed = set()
        for v in v_prime.copy():
            if v not in removed:
                if pv.intersection(set(spanning_tree[v])) != set():
                    # Find vertex with min degree in the intersection of the path and the tree
                    u = min(
                        pv.intersection(set(spanning_tree[v])),
                        key=lambda x: len(spanning_tree[x]),
                    )
                    path_tree.add_edge(u, v)
                    pv.add(v)
                    v_prime.remove(v)
                    removed.add(u)
                    flag = True

    # print(path_tree)

    return path_tree


def combine2(g, tree1, tree2):
    # Generate two random vertices
    i = random.randint(0, len(tree1) - 1)
    j = random.randint(0, len(tree1) - 1)

    pt1 = get_graph(tree1, i, j)
    pt2 = get_graph(tree2, i, j)

    st1 = generate_child(g, pt1, tree1)
    st2 = generate_child(g, pt2, tree2)

    return st1, st2


def mutate(g, tree, n):
    # Add n edges to the tree
    i = 0
    while i < n:
        # Choose random vertices
        u = random.randint(0, len(g) - 1)
        v = random.randint(0, len(g) - 1)

        if u != v and v not in tree[u]:
            tree.add_edge(u, v)
            i += 1

    # Remove edges to eliminate cycles
    while nx.cycle_basis(tree):
        # Choose random edge in the cycle
        cycle = nx.cycle_basis(tree)[0]
        u = cycle[0]
        v = cycle[1]

        tree.remove_edge(u, v)

    return tree


if __name__ == "__main__":
    g = random_graph_num_edges(10, 30)
    s1 = generate_random_spanning_tree(g)
    s2 = generate_random_spanning_tree(g)
    # print(is_spanning_tree(g, s1))
    # print(is_spanning_tree(g, s2))
    # print()

    for i in range(10):
        # s1, s2 = combine2(g, s1, s2)
        # print(is_spanning_tree(g, s1))
        # print(is_spanning_tree(g, s2))

        # visualize_sol(g, s1)
        # visualize_sol(g, s2)

        # print()

        s1new = combine1(g, [s1, s2])

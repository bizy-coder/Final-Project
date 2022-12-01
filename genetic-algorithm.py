from helper import *


def combine1(g, trees, M=4, sigma=1, omega=0.25):
    """
    Trying to implement combination from
    https://www.sciencedirect.com/science/article/pii/S0377221713006103

    May be incorrect
    """

    for tree in trees:
        for edge in tree.edges:
            # Decrease the weight of the edge in g by sigma
            g[edge[0]][edge[1]] -= sigma

            # Decrease the weight of all other edges in g by omega
            for u in range(len(g)):
                for v in g[u]:
                    if u != edge[0] and v != edge[1]:
                        g[u][v] -= omega

    # Create a forest by removing all edges adjacent to vertices of degree at least 3
    forest = g.copy()
    for u in range(len(g)):
        if len(g[u]) >= 3:
            for v in g[u]:
                forest.remove_edge(u, v)

    for u in range(len(g)):
        for v in g[u]:
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

            g[u][v] -= M * length

    for edge in forest.edges:
        # Increase the weight of all edges not in g by 2*omega
        for u in range(len(g)):
            for v in g[u]:
                if u != edge[0] and v != edge[1]:
                    g[u][v] += 2 * omega

    # Get MST of g
    mst = nx.minimum_spanning_tree(g)

    return mst


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
    pv = set(path_tree.vertices)
    v_prime = set(g.vertices) - pv
    for v in v_prime:
        if pv.intersection(set(spanning_tree[v])):
            # Find vertex with min degree in the intersection of the path and the tree
            u = min(
                pv.intersection(set(spanning_tree[v])),
                key=lambda x: len(spanning_tree[x]),
            )
            pv.add(v)
            path_tree.add_edge(u, v)
            v_prime.remove(v)
    return path_tree


def combine2(g, tree1, tree2):
    # Generate two random vertices
    i = random.randint(0, len(tree1) - 1)
    j = random.randint(0, len(tree1) - 1)

    pt1 = get_graph(tree1, i, j)
    pt2 = get_graph(tree2, i, j)

    st1 = generate_child(pt1, tree1)
    st2 = generate_child(pt2, tree2)

    return st1, st2

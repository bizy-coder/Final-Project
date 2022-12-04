import networkx as nx
from matplotlib import pyplot as plt
import random


def yield_graphs(file):
    with open(file, "r") as f:
        # Get the number of instances
        k = int(f.readline())

        # For each instance
        for _ in range(k):
            # Get the number of vertices and edges
            n, m = map(int, f.readline().split())

            # Create the adjacency list
            adj = [[] for _ in range(n)]

            # For each edge
            for _ in range(m):
                # Get the vertices
                u, v = map(int, f.readline().split())

                # Add the edge
                adj[u].append(v)
                adj[v].append(u)

            # Yield the graph
            yield adj


def random_graph_num_edges(n, m):
    # Erdos-Renyi random graph from networkx
    G = nx.gnm_random_graph(n, m)

    # Repeat until the graph is connected
    while not nx.is_connected(G):
        G = nx.gnm_random_graph(n, m)

    return G


def random_graph_prob_edges(n, p):
    # Create simple graph
    G = nx.Graph()

    # Add the vertices
    G.add_nodes_from(range(n))

    # Add the edges
    for u in range(n):
        for v in range(u + 1, n):
            if random.random() < p:
                G.add_edge(u, v)

    # Repeat until the graph is connected
    while not nx.is_connected(G):
        # Create the graph
        G = nx.Graph()

        # Add the vertices
        G.add_nodes_from(range(n))
        # Add the edges
        for u in range(n):
            for v in range(u + 1, n):
                if random.random() < p:
                    G.add_edge(u, v)

    return G


def networkx_to_adj(g):
    # Create the adjacency list
    adj = [[] for _ in range(len(g))]

    # For each edge
    for u, v in g.edges:
        # Add the edge
        adj[u].append(v)
        adj[v].append(u)

    return adj


def adj_to_networkx(g):
    # Create the graph
    G = nx.Graph()

    # Add the vertices
    G.add_nodes_from(range(len(g)))

    # Add the edges
    for u in range(len(g)):
        for v in g[u]:
            G.add_edge(u, v)

    return G


def valid(g, leaves, inner, debug=False):
    if debug:
        print("leaves: ", leaves)
        print("inner: ", inner)

    # check if inner is connected
    if not nx.is_connected(g.subgraph(inner)):
        # print("inner is not connected")
        # print(g.subgraph(inner).edges)
        # err
        return False

    # All leaves must be connected to inner
    for v in leaves:
        if debug:
            print(v, set(g.neighbors(v)), set(g.neighbors(v)).intersection(inner))
        if not set(g.neighbors(v)).intersection(inner):
            return False
    return True


def output_graph(g, file):
    # Write the graph to a file
    nx.write_edgelist(G, file, data=False)


def visualize_graph(g):
    if isinstance(g, list):
        G = adj_to_networkx(g)
    else:
        G = g

    # Visualize the graph
    nx.draw(G, with_labels=True)
    plt.show()


def get_sol_from_inner_vertices(g, sol):
    # Create networkx graph
    G = nx.Graph()

    # Add the vertices
    G.add_nodes_from(range(len(g)))

    # Add the edges connecting the vertices in the solution
    for u in sol:
        for v in g[u]:
            if v in sol:
                G.add_edge(u, v)

    # Remove edges until there are no cycles
    while nx.cycle_basis(G):
        # Get the cycle
        cycle = nx.cycle_basis(G)[0]

        # Remove the edge with the highest degree
        G.remove_edge(cycle[0], cycle[1])

    # For all vertices not in the solution add an edge between it and one vertex in the solution
    for u in range(len(g)):
        if u not in sol:
            for v in g[u]:
                if v in sol:
                    G.add_edge(u, v)
                    break

    return G


def visualize_sol(g, sol_graph, display_unused_edges=False):
    if isinstance(g, list):
        G = adj_to_networkx(g)
    else:
        G = g

    # Visualize the graph, coloring leaves red and inner vertices green
    node_colors = ["red" if sol_graph.degree(u) == 1 else "green" for u in G.nodes]
    # print(node_colors)
    if display_unused_edges:
        # Give edges in the solution a solid color and unused edges a dashed color
        edge_colors = [
            "black" if (sol_graph.has_edge(u, v) or sol_graph.has_edge(v, u)) else "red"
            for u, v in G.edges
        ]
        nx.draw(G, node_color=node_colors, edge_color=edge_colors)
    else:
        # Draw the solution
        nx.draw(sol_graph, node_color=node_colors)

    plt.show()


def is_spanning_tree(g, tree):
    # Check if the tree is a spanning tree of g
    return len(tree) == len(g) and nx.is_connected(tree)


def num_leaves(G):
    return sum(1 for u in G.nodes if G.degree(u) == 1)

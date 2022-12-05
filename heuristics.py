from helper import *


def generate_random_spanning_tree(g):
    # Initialize weighted graph
    G = nx.Graph()

    for u in range(len(g)):
        for v in g[u]:
            G.add_edge(u, v, weight=random.random())

    # Use Prim's algorithm to generate a spanning tree
    tree = nx.minimum_spanning_tree(G)

    return tree


def solis_oba(G):
    F = nx.Graph()

    # Phase 1
    while True:
        # Case 1
        for v in F.nodes:
            ng_v = set(G.neighbors(v)) - set(F.nodes)
            if len(ng_v) >= 2:
                F_prime = nx.Graph(F.copy())
                F_prime.add_nodes_from(ng_v)
                for u in ng_v:
                    F_prime.add_edge(v, u)
                F = F_prime
                break
        else:
            # Case 2
            for v in F.nodes:
                ng_v = set(G.neighbors(v)) - set(F.nodes)
                if len(ng_v) == 1:
                    w = list(ng_v)[0]
                    ng_w = set(G.neighbors(w)) - set(F.nodes)
                    if len(ng_w) >= 3:
                        F_prime = nx.Graph(F.copy())
                        F_prime.add_nodes_from([w] + list(ng_w))
                        F_prime.add_edge(v, w)
                        for u in ng_w:
                            F_prime.add_edge(w, u)
                        F = F_prime
                        break
            else:
                # Case 3
                for v in F.nodes:
                    ng_v = set(G.neighbors(v)) - set(F.nodes)
                    if len(ng_v) == 1:
                        w = list(ng_v)[0]
                        ng_w = set(G.neighbors(w)) - set(F.nodes)
                        if len(ng_w) == 2:
                            F_prime = nx.Graph(F.copy())
                            F_prime.add_nodes_from([w] + list(ng_w))
                            F_prime.add_edge(v, w)
                            for u in ng_w:
                                F_prime.add_edge(w, u)
                            F = F_prime
                            break
                else:
                    # Case 4
                    for v in set(G.nodes) - set(F.nodes):
                        ng_v = set(G.neighbors(v)) - set(F.nodes)
                        if len(ng_v) >= 3:
                            F_prime = nx.Graph(F.copy())
                            F_prime.add_nodes_from([v] + list(ng_v))
                            for u in ng_v:
                                F_prime.add_edge(v, u)
                            F = F_prime
                            break
                    else:
                        break

    # Phase 2
    while set(F.nodes) != set(G.nodes):
        for v in F.nodes:
            ng_v = set(G.neighbors(v)) - set(F.nodes)
            if len(ng_v) >= 1:
                F_prime = nx.Graph(F.copy())
                F_prime.add_nodes_from(ng_v)
                for u in ng_v:
                    F_prime.add_edge(v, u)
                F = F_prime
                break

    # Phase 3
    while not nx.is_connected(F):
        for e in F.edges:
            if not nx.is_connected(F.remove_edge(*e)):
                F.add_edge(*e)

    return F


def pure_greedy(g, start=None):
    leaves = set([v for v in g])
    inner = set()

    if start is None:
        # Get vertex with highest degree
        start = max(g, key=lambda x: len(g[x]))

    # Remove start from S
    leaves.remove(start)

    # Add start to S'
    inner.add(start)

    candidates = set(g.neighbors(start))

    while not valid(g, leaves, inner):
        # Get the vertex with the highest greedy value
        v = select_greedy(candidates, g, leaves, inner)

        # Remove v from S
        leaves.remove(v)

        # Add v to S'
        inner.add(v)

        # Update candidates
        candidates = candidates.union(set(g.neighbors(v))) - inner

    return get_sol_from_inner_vertices(g, inner)


def select_greedy(candidates, g, leaves, inner):
    v = max(candidates, key=lambda x: greedy_value(x, g, leaves, inner))
    return v


def greedy_value(v, g, leaves, inner):
    return len(set(g.neighbors(v)).intersection(leaves)) - len(
        set(g.neighbors(v)).intersection(inner)
    )


def greedy_distance_based(
    g, start_node, distance_modifier=lambda x: 1 if x > 0 else 0, shortest_paths=None
):
    inner = set()
    if shortest_paths is None:
        shortest_paths = dict(nx.shortest_path_length(g))

    if start_node is None:
        min_distance = float("inf")
        min_distance_node = None
        for node in g.nodes():
            dist = 0
            for target_node in g.nodes():
                x = min(
                    shortest_paths[source_node][target_node]
                    for source_node in set(g.neighbors(node))
                )
                dist += x

            if dist < min_distance:
                min_distance = dist
                min_distance_node = node

    leaves = set([start_node])

    while len(inner) + len(leaves) < g.number_of_nodes():
        # print(len(inner), len(leaves))
        min_distance = float("inf")
        min_distance_node = None
        for node in leaves:
            updated_nodes = inner.union(set(g.neighbors(node))).union(leaves)
            # print(updated_nodes)
            dist = 0
            for target_node in g.nodes():
                x = min(
                    shortest_paths[source_node][target_node]
                    for source_node in updated_nodes
                )
                dist += x

            if dist < min_distance:
                min_distance = dist
                min_distance_node = node

        # Add one edge connecting the new node to the tree
        # print(min_distance_node, set(g.neighbors(min_distance_node)) - set(t.nodes()))
        for neighbor in set(g.neighbors(min_distance_node)) - inner:
            leaves.add(neighbor)
        leaves.remove(min_distance_node)
        inner.add(min_distance_node)

    return get_sol_from_inner_vertices(g, inner)


def greedy_distance_based2(g, start_node, distance_modifier=None, shortest_paths=None):
    inner = set()
    if shortest_paths is None:
        shortest_paths = dict(nx.shortest_path_length(g))

    if start_node is None:
        min_distance = float("inf")
        min_distance_node = None
        for node in g.nodes():
            dist = 0
            for target_node in g.nodes():
                x = min(
                    shortest_paths[source_node][target_node]
                    for source_node in set(g.neighbors(node))
                )

                dist += x

            if dist < min_distance or dist == min_distance and node < min_distance_node:
                min_distance = dist
                min_distance_node = node

    leaves = set([start_node])

    min_distance_to_tree = {}
    for node in g.nodes():
        min_distance_to_tree[node] = shortest_paths[start_node][node]

    while len(inner) + len(leaves) < g.number_of_nodes():
        # print(len(inner), len(leaves))
        max_distance_reduction = float("inf")
        max_reduction_node = None

        for leaf in leaves:
            neighbors = set(g.neighbors(leaf)) - inner - leaves
            distance_reduction = -len(neighbors)
            if neighbors:
                for node in g.nodes() - inner - leaves:
                    reduction = (
                        min(shortest_paths[neighbor][node] for neighbor in neighbors)
                        - min_distance_to_tree[node]
                    )
                    distance_reduction += min(0, reduction)

            if (
                distance_reduction < max_distance_reduction
                or distance_reduction == max_distance_reduction
                and leaf < max_reduction_node
            ):
                max_distance_reduction = distance_reduction
                max_reduction_node = leaf

        for neighbor in set(g.neighbors(max_reduction_node)) - leaves - inner:
            min_distance_to_tree[neighbor] = 0
            for node in g.nodes() - leaves - inner:
                min_distance_to_tree[neighbor] = min(
                    min_distance_to_tree[neighbor], shortest_paths[neighbor][node]
                )

        leaves = leaves.union(set(g.neighbors(max_reduction_node)) - leaves - inner)
        leaves.remove(max_reduction_node)
        inner.add(max_reduction_node)

    return get_sol_from_inner_vertices(g, inner)


# Create a function to generate a spanning tree of a graph
def random_bfs_order(g, tree, neighbors):
    # Randomize neighbors order, don't modify
    neighbors = list(neighbors)
    random.shuffle(neighbors)
    return neighbors


def greedy_bfs_order(g, tree, neighbors):
    # Get the node with the most neighbors not yet in the tree
    neighbors = list(neighbors)
    neighbors.sort(
        key=lambda x: len(set(g.neighbors(x)) - set(tree.nodes)), reverse=True
    )
    return neighbors


def bfs_spanning_tree(g, root, bfs_order=random_bfs_order):
    T = nx.Graph()
    queue = [root]
    visited = set()

    while queue:
        current_node = queue.pop(0)
        visited.add(current_node)
        neighbors = g.neighbors(current_node)

        for neighbor in bfs_order(g, T, neighbors):
            if neighbor not in visited:
                visited.add(neighbor)
                T.add_edge(current_node, neighbor)
                queue.append(neighbor)

    return T


# if __name__ == "__main__":
#     g = random_graph_num_edges(10, 20)

#     print(type(g), len(g.nodes()), len(g.edges()))
#     # st = solis_oba(g)
#     # st = greedy_distance_based(g, 1)
#     st = bfs_spanning_tree(g, 1, greedy_bfs_order)

#     print(type(st), len(st.nodes()), len(st.edges()))
#     # st = g
#     visualize_sol(g, st, True)

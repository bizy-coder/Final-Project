from helper import *

"""
Algorithm from:
https://link.springer.com/chapter/10.1007/978-3-319-24598-0_29#Sec4
"""


def construct(g):
    leaves = set([v for v in g])
    inner = set()

    # Get vertex with highest degree
    v = max(g, key=lambda x: len(g[x]))

    # Remove v from S
    leaves.remove(v)

    # Add v to S'
    inner.add(v)

    candidates = set(g.neighbors(v))

    while not valid(g, leaves, inner):
        # Get the vertex with the highest greedy value
        v = select_greedy(candidates, g, leaves, inner)

        # Remove v from S
        leaves.remove(v)

        # Add v to S'
        inner.add(v)

        # Update candidates
        candidates = candidates.union(set(g.neighbors(v))) - inner

    return leaves, inner


def select_greedy(candidates, g, leaves, inner):
    v = max(candidates, key=lambda x: greedy_value(x, g, leaves, inner))
    return v


def greedy_value(v, g, leaves, inner):
    return len(set(g.neighbors(v)).intersection(leaves)) - len(
        set(g.neighbors(v)).intersection(inner)
    )


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


def drop(v, leaves, inner):
    # Add v to S'
    inner.add(v)

    # Remove v from S
    leaves.remove(v)


def add(v, leaves, inner):
    # Remove v from S'
    inner.remove(v)

    # Add v to S
    leaves.add(v)


def strategic_oscilation(g, k_step=0.01, k_max=1):
    leaves, inner = construct(g)
    k = k_step

    # print(valid(g, leaves, inner, debug=True))

    last_leaves = leaves.copy()
    last_inner = inner.copy()

    while k <= k_max:
        delta_plus = set()
        delta_minus = set()
        for _ in range(int(k * len(inner))):
            v = random.choice(list(inner))
            add(v, leaves, inner)
            delta_plus.add(v)

        while not valid(g, leaves, inner):
            v = select_greedy(leaves, g, leaves, inner)
            drop(v, leaves, inner)
            delta_minus.add(v)

        if len(leaves) > len(last_leaves):
            k = k_step
            last_inner = inner.copy()
            last_leaves = leaves.copy()
        else:
            k = k + k_step
            # print(leaves)
            leaves = last_leaves.copy()
            # print(len(leaves))
            inner = last_inner.copy()

    return leaves, inner


n, m = 100, 1000

g = random_graph_num_edges(n, m)

for _ in range(100):
    sol_init, _ = construct(g)
    leaves, inner = strategic_oscilation(g, 0.001, 1)
    # print("Construction solution size:", n - len(sol_init))
    print("Solution size:", len(leaves))
    # visualize_graph(g)
    sol = get_sol_from_inner_vertices(g, inner)
    print(nx.is_connected(sol))
    # visualize_sol(g, sol)
